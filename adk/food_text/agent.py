from google.adk.agents import SequentialAgent, LlmAgent, ParallelAgent, BaseAgent
from food_text.models import *
from food_text.callbacks.before_merger import skip_merger_if_questions_pending
from food_text.subagents.ParallelFoodProcessorAgent import ParallelFoodProcessorAgent


GEMINI_MODEL = "gemini-2.5-flash"


# Sub-Agent 1: Parse input description
input_parser_agent = LlmAgent(
    name="InputParserAgent",
    model=GEMINI_MODEL,
    instruction="""Parse the user's food description into a JSON object conforming to the ParsedFoods schema: a JSON object with "foods" (list of UnknownFood objects, each with "name" string, "description" string, "meal_type" string, "quantity" float default 1.0, "unit" string default "serving",) and "questions" (list of question objects, each with "question" string, "type" string e.g. "multiple_choice", "mcqOptions" list of strings, "sliderValue" int).
Extract name, quantity (default 1.0), unit (default 'serving'), meal_type, and description. If ambiguous, add clarifying questions with type "multiple_choice" and up to three educated guess options for the user to choose from. Do not question reasonable assumptions! For example, assume chicken is lean unless expliciltly mentioned fried. Assume french fries are salted and steaks are seasoned. Take branded food as they are unless specified otherwise.
Example output: {"foods": [{"name": "apple", "description": "red apple", "meal_type": "Breakfast", "quantity": 2.0, "unit": "pieces" }, {"name": "chicken", "description": "chicken meat", "meal_type": "Lunch", "quantity": 1.0, "unit": "serving" }], "questions": [{"question": "What type of chicken?", "type": "multiple_choice", "mcqOptions": ["breast", "thigh", "whole"], "sliderValue": 0}, {"question": "How was it prepared?", "type": "multiple_choice", "mcqOptions": ["grilled", "fried", "baked"], "sliderValue": 0}]}.
IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_schema=ParsedFoods,
    output_key="parsed_foods",
)


merger_agent = LlmAgent(
    name="NutritionMergerAgent",
    model=GEMINI_MODEL,
    instruction="""Output a JSON array conforming to the RequestResponse schema: a list of FoodSearchResult objects.
    Take the search results from all food searches and combine them into a single list.
    Do NOT sum or aggregate values. Output each individual food item as found.
    Output format: [{"name": "McDonald's cheeseburger", "meal_type": "lunch", "serving_size": 1, "calories": 540.0, "protein_g": 25.0, "carbs_g": 45.0, "trans_fat_g": 1.5, "saturated_fat_g": 12.0, "unsaturated_fat_g": 8.0, "others": {"sodium_mg": 1040}}, {"name": "apple", "meal_type": "snack", "serving_size": 2, "calories": 160.0, "protein_g": 0.6, "carbs_g": 42.0, "trans_fat_g": 0.0, "saturated_fat_g": 0.1, "unsaturated_fat_g": 0.2, "others": {}}].
    IMPORTANT: Return ONLY the JSON array. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_key="final_result",
    output_schema=RequestResponse,
    before_agent_callback=skip_merger_if_questions_pending,
)

# Root SequentialAgent
root_agent = SequentialAgent(
    name="NutritionTrackerAgent",
    sub_agents=[input_parser_agent, ParallelFoodProcessorAgent(), merger_agent],
    description="Sequentially parses meals, processes them in parallel, and merges total nutrition.",
)
