from google.adk.agents import LlmAgent
from food_text.models import Intent

GEMINI_MODEL = "gemini-2.5-flash"

# Sub-Agent: Intent Classification
intent_classification_agent = LlmAgent(
    name="IntentClassificationAgent",
    model=GEMINI_MODEL,
    instruction="""Analyze the user's input to determine their intent. Return a JSON object conforming to the Intent schema.

Intent types:
1. "new_meal" - User is logging a new meal or food item
   - Examples: "I had pizza for lunch", "ate an apple", "breakfast was oatmeal"
   
2. "update_meal" - User wants to modify a previously logged meal
   - Keywords: "change", "update", "modify", "remove", "add to", "replace"
   - Time references to past meals: "my breakfast", "lunch from yesterday", "dinner I logged"
   - Examples: "change my lunch apple to 2 apples", "remove fries from my dinner", "add cookie to yesterday's lunch"
   
3. "answer_question" - User is responding to clarification questions from a previous meal logging attempt
   - Responses like "option 1", "grilled", "medium size", "breast meat"
   - Usually short answers or selections from provided options

Provide brief reasoning for your classification.

Example output: {"type": "update_meal", "reasoning": "User wants to change quantity of existing meal item using 'change my lunch' pattern"}

IMPORTANT: Return ONLY the JSON object. No markdown, code blocks, or extra text.""",
    output_schema=Intent,
    output_key="intent",
)