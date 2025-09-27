import json
from google.adk.agents import SequentialAgent, LlmAgent, ParallelAgent, BaseAgent
from google.adk.events import Event
from typing import AsyncGenerator
from google.genai import types
from food_text.models import *
from food_text.tools import *


GEMINI_MODEL = "gemini-2.5-flash"


class ParallelMealProcessorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ParallelMealProcessorAgent")

    async def run_async(self, invocation_context) -> AsyncGenerator[Event, None]:
        # Check callback before processing - manually check for questions
        parsed_meals = invocation_context.session.state.get("parsed_meals", {})

        # Check if any meal has questions
        for meal in parsed_meals.get("meals", []):
            if meal.get("questions", []):
                # Set flag in session state to indicate questions are pending
                invocation_context.session.state["questions_pending"] = True
                # Return the questions as the final response, skipping this agent
                content = types.Content(
                    role="assistant",
                    parts=[
                        types.Part(
                            text=json.dumps(
                                {
                                    "questions": meal["questions"],
                                    "status": "questions_pending",
                                }
                            )
                        )
                    ],
                )
                yield Event(author=self.name, content=content)
                return

        parsed_meals = invocation_context.session.state.get("parsed_meals", {})
        sub_agents = []
        for meal in parsed_meals.get("meals", []):
            meal_name = meal["name"].replace(" ", "_")
            # Sub-agent for searching foods in this meal
            food_search_agent = LlmAgent(
                name=f"FoodSearchAgent_{meal_name}",
                model=GEMINI_MODEL,
                instruction=f"""Output ONLY a JSON object conforming to the FoodSearchOutput schema: a JSON object with "questions" (list of question objects, each with "question" string, "type" string, "mcqOptions" list of strings, "sliderValue" int), "foods" (list of food result objects, each with "name" string, "nutrition" object with "calories" float, "protein_g" float, "carbs_g" float, "fat_g" float, "serving_size" string).
                For each food in {meal['foods']}, call search_usda and search_off with the food name.
                Select the best matching result from combined API data (prioritize USDA for accuracy if duplicates).
                Extract nutrition per serving (calories, protein_g, carbs_g, fat_g) and serving_size.
                Output {{"questions": [], "foods": [{{"name": "apple", "nutrition": {{"calories": 95, "protein_g": 0.5, ...}}, "serving_size": "1 medium"}}, ...]}}.
                Handle missing data gracefully.
                IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
                tools=[search_usda, search_off],
                output_key=f"search_result_{meal_name}",
                output_schema=None,
                before_tool_callback=before_food_search_callback,
            )
            # Sub-agent for calculating nutrition for this meal
            nutrition_calculator_agent = LlmAgent(
                name=f"NutritionCalculatorAgent_{meal_name}",
                model=GEMINI_MODEL,
                instruction=f"""Output a JSON object conforming to the TotalNutrition schema: a JSON object with "total_calories" float, "total_protein_g" float, "total_carbs_g" float, "total_fat_g" float.
                Take {f"search_result_{meal_name}"} as the list of food data and scale each food's nutrition by its quantity (approximate units if needed, e.g., 1 piece ≈ 1 serving).
                Sum nutrition values across all foods in this meal.
                Output total nutrition as a dict: {{"total_calories": 200, "total_protein_g": 5, ...}}.
                IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
                output_key=f"meal_nutrition_{meal_name}",
                output_schema=TotalNutrition,
                before_model_callback=before_calculator_callback,
            )
            # Sequential agent for this meal
            meal_processor = SequentialAgent(
                name=f"MealProcessor_{meal_name}",
                sub_agents=[food_search_agent, nutrition_calculator_agent],
                description=f"Sequentially searches APIs and calculates nutrition for {meal_name}.",
            )
            sub_agents.append(meal_processor)
        # Run parallel processing for all meals
        parallel_agent = ParallelAgent(
            name="ParallelMealProcessor",
            sub_agents=sub_agents,
            description="Runs meal processors concurrently for speed.",
        )
        async for event in parallel_agent.run_async(invocation_context):
            yield event
        # Collect results into state for merging
        meal_nutritions = []
        for meal in parsed_meals.get("meals", []):
            meal_name = meal["name"].replace(" ", "_")
            # Parse the search_result text
            search_result_text = invocation_context.session.state.get(
                f"search_result_{meal_name}", "{}"
            )
            search_result_json = strip_code_blocks(search_result_text)
            search_result = json.loads(search_result_json)
            # Validate with FoodSearchOutput
            search_result = FoodSearchOutput(**search_result)
            invocation_context.session.state[f"search_result_{meal_name}"] = (
                search_result
            )
            nutrition = invocation_context.session.state.get(
                f"meal_nutrition_{meal_name}", {}
            )
            meal_nutritions.append({"meal_name": meal_name, "nutrition": nutrition})
        invocation_context.session.state["meal_nutritions"] = meal_nutritions


def skip_merger_if_questions_pending(callback_context):
    """Skip merger if questions are pending"""
    if callback_context.state.get("questions_pending", False):
        # Questions are pending, skip merger execution
        return types.Content(
            role="assistant",
            parts=[
                types.Part(
                    text=json.dumps(
                        {
                            "questions": callback_context.state.get("parsed_meals", {})
                            .get("meals", [])[0]
                            .get("questions", []),
                            "status": "questions_pending",
                        }
                    )
                )
            ],
        )
    return None


# Sub-Agent 1: Parse input description
input_parser_agent = LlmAgent(
    name="InputParserAgent",
    model=GEMINI_MODEL,
    instruction="""Parse the user's food description into a JSON object conforming to the ParsedMeals schema: a JSON object with a "meals" key containing a list of meal objects. Each meal object has "name" (string, e.g., "Breakfast"), "foods" (list of food item objects, each with "name" string, "quantity" float default 1.0, "unit" string default "serving"), and "questions" (list of question objects, each with "question" string, "type" string e.g. "multiple_choice", "mcqOptions" list of strings, "sliderValue" int).
Extract name, quantity (default 1), and unit (default 'serving').
Check if any food name is too vague (e.g., "chicken" without specifying type or preparation). If vague, add clarifying questions with type "multiple_choice" and up to three educated guess options for the user to choose from before providing their own input. Do not question reasonable assumptions like salt on fries.
Example output: {"meals": [{"name": "Breakfast", "foods": [{"name": "apple", "quantity": 2, "unit": "pieces"}], "questions": []}, {"name": "Lunch", "foods": [{"name": "chicken", "quantity": 1, "unit": "serving"}], "questions": [{"question": "What type of chicken?", "type": "multiple_choice", "mcqOptions": ["breast", "thigh", "whole"]}, {"question": "How was it prepared?", "type": "multiple_choice", "mcqOptions": ["grilled", "fried", "baked"]}]}]}.
IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_schema=ParsedMeals,
    output_key="parsed_meals",
)


merger_agent = LlmAgent(
    name="NutritionMergerAgent",
    model=GEMINI_MODEL,
    instruction="""Output a JSON object conforming to the TotalNutrition schema: a JSON object with "total_calories" float, "total_protein_g" float, "total_carbs_g" float, "total_fat_g" float.
    Take {meal_nutritions} as the list of meal nutritions.
    Sum the nutrition values across all meals to get the total.
    Output total nutrition as a dict: {"total_calories": 400, "total_protein_g": 10, ...}.
    IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_key="final_result",
    output_schema=TotalNutrition,
    before_agent_callback=skip_merger_if_questions_pending,
)

# Root SequentialAgent
root_agent = SequentialAgent(
    name="NutritionTrackerAgent",
    sub_agents=[input_parser_agent, ParallelMealProcessorAgent(), merger_agent],
    description="Sequentially parses meals, processes them in parallel, and merges total nutrition.",
)
