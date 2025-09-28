import json
from google.adk.agents import LlmAgent
from google.genai import types
from food_text.models import RequestResponse

GEMINI_MODEL = "gemini-2.5-flash"


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
                            "questions": callback_context.state.get(
                                "parsed_foods", {}
                            ).get("questions", []),
                            "status": "questions_pending",
                        }
                    )
                )
            ],
        )
    return None


# Sub-Agent: Nutrition Merger
merger_agent = LlmAgent(
    name="NutritionMergerAgent",
    model=GEMINI_MODEL,
    instruction="""CONDITIONAL BEHAVIOR BASED ON INTENT:

If intent.type == "new_meal":
Output a JSON array conforming to the RequestResponse schema: a list of FoodSearchResult objects.
Take the search results from all food searches and combine them into a single list.
Do NOT sum or aggregate values. Output each individual food item as found.
Preserve the eaten_at timestamp from the original parsed foods for each item.

If intent.type == "update_meal":
1. Use the update_existing_meal tool to apply the parsed update operations
2. Return the updated meal data in RequestResponse format
3. Preserve original timestamps and metadata where not modified

If intent.type == "answer_question":
Continue with normal merging behavior using the resolved foods from question answers.

Output format: [{"name": "McDonald's cheeseburger", "eaten_at": "2025-09-28T12:00:00", "meal_type": "lunch", "serving_size": 1, "calories": 540.0, "protein_g": 25.0, "carbs_g": 45.0, "trans_fat_g": 1.5, "saturated_fat_g": 12.0, "unsaturated_fat_g": 8.0, "others": {"sodium_mg": 1040}}, {"name": "apple", "eaten_at": "2025-09-27T15:00:00", "meal_type": "snack", "serving_size": 2, "calories": 160.0, "protein_g": 0.6, "carbs_g": 42.0, "trans_fat_g": 0.0, "saturated_fat_g": 0.1, "unsaturated_fat_g": 0.2, "others": {}}].

IMPORTANT: Return ONLY the JSON array. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_key="final_result",
    output_schema=RequestResponse,
    before_agent_callback=skip_merger_if_questions_pending,
)