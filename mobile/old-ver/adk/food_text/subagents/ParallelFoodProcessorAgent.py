import json
from google.adk.agents import LlmAgent, ParallelAgent, BaseAgent
from google.adk.events import Event
from typing import AsyncGenerator
from google.genai import types
from google.adk.tools import google_search
from food_text.models import *
from food_text.tools import strip_code_blocks

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
                parts=[types.Part(text=json.dumps(parsed_foods))],
            )
            yield Event(author=self.name, content=content)
            return

        parsed_foods = invocation_context.session.state.get("parsed_foods", {})
        sub_agents = []
        foods = parsed_foods.get("foods", [])

        # Get user memory for personalization
        personalization = invocation_context.session.state.get("personalization", {})
        user_memory = personalization.get("memory", [])
        memory_context = f"User memory for personalization: {json.dumps(user_memory)}" if user_memory else "No user memory available."

        for food in foods:
            food_name = food["name"].replace(" ", "_").replace("-", "_")
            # Inject food data directly into instruction to avoid context contamination
            food_data = json.dumps(food)

            # Sub-agent for searching foods in this meal
            food_search_agent = LlmAgent(
                name=f"FoodSearchAgent_{food_name}",
                model=GEMINI_MODEL,
                instruction=f"""You are processing this specific food item: {food_data}

                {memory_context}

                Consider the user's memory for personalization when selecting nutrition data. User memory contains their past preferences and dietary habits that can help choose the most appropriate nutrition values.

                Output ONLY a JSON array conforming to the RequestResponse schema: a list of FoodSearchResult objects, each with "id" (int or null), "name" string, "eaten_at" string, "meal_type" string or null, "serving_size" int default 1, "calories" float default 0.0, "protein_g" float default 0.0, "carbs_g" float default 0.0, "trans_fat_g" float default 0.0, "saturated_fat_g" float default 0.0, "unsaturated_fat_g" float default 0.0, "others" dict default empty.

                Use google search to verify the nutrition value based on usda and openfoodfoundation.
                Select the best matching result from the search results.
                IMPORTANT: Preserve the eaten_at timestamp from the input food data exactly as provided.
                IMPORTANT: If the input food data has an "id" field, include it in the output FoodSearchResult.
                Output {{"id": null, "name": "McDonald's cheeseburger", "eaten_at": "2025-09-28T19:00:00", "meal_type": "Dinner", "serving_size": 1, "calories": 540.0, "protein_g": 25.0, "carbs_g": 45.0, "trans_fat_g": 1.5, "saturated_fat_g": 12.0, "unsaturated_fat_g": 8.0, "others": {{"sodium_mg": 1040}}}}, ....
                Handle missing data gracefully.
                IMPORTANT: Return ONLY the JSON array. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
                tools=[google_search],
                output_key=f"search_result_{food_name}",
                # Removed before_tool_callback since each agent has its own food data
            )
            sub_agents.append(food_search_agent)
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
