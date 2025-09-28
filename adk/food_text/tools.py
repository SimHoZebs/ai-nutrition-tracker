import requests
import os
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.base_tool import BaseTool
from google.genai import types
from typing import Any, Optional
import json


def strip_code_blocks(text: str) -> str:
    """Strip markdown code blocks from text if present."""
    if text.startswith("```") and text.endswith("```"):
        lines = text.split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1] == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


# Define API tools
def search_usda(query: str) -> dict:
    """Search USDA FoodData Central for foods matching the query."""
    api_key = os.getenv("USDA_API_KEY", "DEMO_KEY")
    print(f"query: {query}")
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={query}&dataType=Branded,Foundation,Survey%20%28FNDDS%29&pageSize=5&pageNumber=1"
    response = requests.get(url)

    foods = response.json().get("foods", [])
    print("USDA results", foods)
    return foods[0:5] if response.status_code == 200 else {"error": "USDA API failed"}


def search_off(query: str) -> dict:
    """Search OpenFoodFacts for products matching the query."""
    headers = {
        "User-Agent": "NutritionTracker/1.0 (contact@example.com)"
    }  # Custom User-Agent
    print(f"query: {query}")
    url = f"https://world.openfoodfacts.org/api/v2/search?q={query}&page_size=5&page=1"
    response = requests.get(url, headers=headers)
    products = response.json().get("products", [])
    print("off results", products)
    return products[0:5] if response.status_code == 200 else {"error": "OFF API failed"}


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
    if len(questions) > 0:
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

