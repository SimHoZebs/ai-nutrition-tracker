import requests
from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.base_tool import BaseTool
from google.genai import types
from typing import Any, Optional
import json
from pydantic import BaseModel, RootModel


class Qna(BaseModel):
    question: str
    type: str  # e.g., "slider" or "multiple_choice"
    mcqOptions: list[str]
    sliderValue: int


class FoodItem(BaseModel):
    name: str
    quantity: float = 1.0
    unit: str = "serving"


class ParsedFoods(BaseModel):
    foods: list[FoodItem]
    questions: list[Qna]


class Nutrition(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float

    class Config:
        extra = "allow"


class FoodResult(BaseModel):
    name: str
    nutrition: Nutrition
    serving_size: str


class FoodSearchOutput(BaseModel):
    questions: list[Qna]
    foods: list[FoodResult]


class TotalNutrition(BaseModel):
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float

    class Config:
        extra = "allow"


GEMINI_MODEL = "gemini-2.5-flash"


# Define API tools
def search_usda(query: str) -> dict:
    """Search USDA FoodData Central for foods matching the query."""
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={query}"
    response = requests.get(url)
    print(f"USDA api response status: {response.status_code}")
    return (
        response.json() if response.status_code == 200 else {"error": "USDA API failed"}
    )


def search_off(query: str) -> dict:
    """Search OpenFoodFacts for products matching the query."""
    headers = {
        "User-Agent": "NutritionTracker/1.0 (contact@example.com)"
    }  # Custom User-Agent
    url = f"https://world.openfoodfacts.org/api/v2/search?q={query}"
    response = requests.get(url, headers=headers)
    return (
        response.json() if response.status_code == 200 else {"error": "OFF API failed"}
    )


# Helper function to remove condition line from request
def remove_condition_line(llm_request: LlmRequest):
    if not llm_request.contents or not llm_request.contents[0].parts:
        return
    text = llm_request.contents[0].parts[0].text
    if not text:
        return
    lines = text.split("\n")
    new_lines = [line for line in lines if not line.startswith("Condition: ")]
    llm_request.contents[0].parts[0].text = "\n".join(new_lines)


# Callback functions for conditional skipping
def before_food_search_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    parsed_foods = tool_context.state.get("parsed_foods", {})
    print(f"Parsed foods for food search: {parsed_foods}")

    questions = parsed_foods.get("questions", [])
    if questions:
        return {"questions": questions, "foods": []}
    return None


def before_calculator_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Parse the condition from the request text
    if not llm_request.contents or not llm_request.contents[0].parts:
        return None
    text = llm_request.contents[0].parts[0].text
    if not text:
        return None
    start = text.find("Condition: ")
    if start == -1:
        return None
    json_str = text[start + len("Condition: ") :].split("\n", 1)[0]
    try:
        search_result = json.loads(json_str)
        if "questions" in search_result:
            content = types.Content(
                role="model", parts=[types.Part(text=json.dumps(search_result))]
            )
            return LlmResponse(content=content)
        else:
            remove_condition_line(llm_request)
    except:
        pass
    return None


# Sub-Agent 1: Parse input description
input_parser_agent = LlmAgent(
    name="InputParserAgent",
    model=GEMINI_MODEL,
    instruction="""Parse the user's food description into a JSON object with "foods" list and "questions" list.
    Extract name, quantity (default 1), and unit (default 'serving').
    Check if any food name is too vague (e.g., "chicken" without specifying type or preparation). If vague, add clarifying questions with type "multiple_choice" and up to three educated guess options for the user to choose from before providing their own input. Do not question reasonable assumptions like salt on fries.
    Example output: {"foods": [{"name": "apple", "quantity": 2, "unit": "pieces"}], "questions": []} or {"foods": [{"name": "chicken", "quantity": 1, "unit": "serving"}], "questions": [{"question": "What type of chicken?", "type": "multiple_choice", "mcqOptions": ["breast", "thigh", "whole"]}, {"question": "How was it prepared?", "type": "multiple_choice", "mcqOptions": ["grilled", "fried", "baked"]}]}.
    Do not return in codeblock. Only return valid JSON.""",
    output_schema=ParsedFoods,
    output_key="parsed_foods",
)

# Sub-Agent 2: Search APIs and merge results
food_search_agent = LlmAgent(
    name="FoodSearchAgent",
    model=GEMINI_MODEL,
    instruction="""Condition: {parsed_foods}
For each food in {parsed_foods}['foods'], call search_usda and search_off with the food name.
For each food, select the best matching result from combined API data (prioritize USDA for accuracy if duplicates).
Extract nutrition per serving (e.g., calories, protein, carbs, fat) and serving size.
Output {"questions": [], "foods": [{"name": "apple", "nutrition": {"calories": 95, "protein_g": 0.5, ...}, "serving_size": "1 medium"}, ...]}.
Handle missing data gracefully.
Do not return in codeblock. Only return valid JSON.""",
    tools=[search_usda, search_off],
    output_key="search_result",
    output_schema=FoodSearchOutput,
    before_tool_callback=before_food_search_callback,
)

# Sub-Agent 3: Calculate total nutrition
nutrition_calculator_agent = LlmAgent(
    name="NutritionCalculatorAgent",
    model=GEMINI_MODEL,
    instruction="""Condition: {search_result}
Take {search_result} as the list of food data and scale each food's nutrition by its quantity (approximate units if needed, e.g., 1 piece ≈ 1 serving).
Sum nutrition values across all foods.
Output total nutrition as a dict: {"total_calories": 200, "total_protein_g": 5, ...}.
Do not return in codeblock. Only return valid JSON.""",
    output_key="final_result",
    output_schema=TotalNutrition,
    before_model_callback=before_calculator_callback,
)

# Root SequentialAgent
root_agent = SequentialAgent(
    name="NutritionTrackerAgent",
    sub_agents=[input_parser_agent, food_search_agent, nutrition_calculator_agent],
    description="Sequentially parses food descriptions, searches APIs, merges data, and calculates total nutrition.",
)
