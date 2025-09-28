import json
from google.adk.agents import SequentialAgent, LlmAgent, ParallelAgent, BaseAgent
from google.adk.events import Event
from typing import AsyncGenerator
from google.genai import types
from google.adk.tools import google_search
from food_text.models import *
from food_text.tools import (
    strip_code_blocks,
    before_food_search_callback,
)

GEMINI_MODEL = "gemini-2.5-flash"


class ParallelFoodProcessorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ParallelMealProcessorAgent")

    async def run_async(self, invocation_context) -> AsyncGenerator[Event, None]:
        # Check callback before processing - manually check for questions
        parsed_foods = invocation_context.session.state.get("parsed_foods", {})

        # Check if there are any questions in the parsed foods
        if parsed_foods.get("questions", []):
            # Set flag in session state to indicate questions are pending
            invocation_context.session.state["questions_pending"] = True
            # Return the questions as the final response, skipping this agent
            content = types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text=json.dumps(
                            {
                                "questions": parsed_foods["questions"],
                                "status": "questions_pending",
                            }
                        )
                    )
                ],
            )
            yield Event(author=self.name, content=content)
            return

        parsed_foods = invocation_context.session.state.get("parsed_foods", {})
        sub_agents = []
        print("Parsed foods for parallel processing:", parsed_foods)
        foods = parsed_foods.get("foods", [])
        for food in foods:
            food_name = food["name"].replace(" ", "_").replace("-", "_")
            # Sub-agent for searching foods in this meal
            food_search_agent = LlmAgent(
                name=f"FoodSearchAgent_{food_name}",
                model=GEMINI_MODEL,
                instruction=f"""Output ONLY a JSON array conforming to the RequestResponse schema: a list of FoodSearchResult objects, each with "name" string, "meal_type" string or null, "serving_size" int default 1, "calories" float default 0.0, "protein_g" float default 0.0, "carbs_g" float default 0.0, "trans_fat_g" float default 0.0, "saturated_fat_g" float default 0.0, "unsaturated_fat_g" float default 0.0, "others" dict default empty.
                Use google search to verify the nutrition value based on usda and openfoodfoundation.
                Select the best matching result from the search results.
                Output {{"name": "McDonald's cheeseburger", "meal_type": null, "serving_size": 1, "calories": 540.0, "protein_g": 25.0, "carbs_g": 45.0, "trans_fat_g": 1.5, "saturated_fat_g": 12.0, "unsaturated_fat_g": 8.0, "others": {{"sodium_mg": 1040}}}}, ....
                Handle missing data gracefully.
                IMPORTANT: Return ONLY the JSON array. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
                tools=[google_search],
                output_key=f"search_result_{food_name}",
                before_tool_callback=before_food_search_callback,
            )
            sub_agents.append(food_search_agent)
        # Run parallel processing for all meals
        parallel_agent = ParallelAgent(
            name="ParallelMealProcessor",
            sub_agents=sub_agents,
            description="Runs meal processors concurrently for speed.",
        )
        async for event in parallel_agent.run_async(invocation_context):
            print(f"Parallel agent event: {event}")
            yield event
        # Collect results into state for merging
        meal_nutritions = []
        print("Collecting meal nutritions for merging.")
        for food in parsed_foods.get("foods", []):
            food_name = food["name"].replace(" ", "_")
            # Parse the search_result text
            search_result_text = invocation_context.session.state.get(
                f"search_result_{food_name}", "{}"
            )
            search_result_json = strip_code_blocks(search_result_text)
            search_result = json.loads(search_result_json)
            invocation_context.session.state[f"search_result_{food_name}"] = (
                search_result
            )
            nutrition = invocation_context.session.state.get(
                f"meal_nutrition_{food_name}", {}
            )
            meal_nutritions.append({"meal_name": food_name, "nutrition": nutrition})
        invocation_context.session.state["meal_nutritions"] = meal_nutritions
