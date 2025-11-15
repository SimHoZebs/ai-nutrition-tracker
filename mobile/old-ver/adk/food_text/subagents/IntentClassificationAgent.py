from google.adk.agents import LlmAgent
from food_text.models import Intent
from food_text.tools import pass_to_next_agent

GEMINI_MODEL = "gemini-2.5-flash"


# Sub-Agent: Intent Classification
intent_classification_agent = LlmAgent(
    name="IntentClassificationAgent",
    model=GEMINI_MODEL,
    instruction="""Analyze the user's input to determine their intent. This application is a nutrition tracker, so all inputs are food-related. Return a JSON object conforming to the Intent schema.

**IMAGE HANDLING:**
When the user provides an image:
- Images are ALWAYS food-related in this nutrition tracking application
- Default to "new_meal" intent unless explicit keywords suggest otherwise
- Images may show meals, individual food items, restaurant dishes, or home-cooked food
- Treat images as equivalent to describing food for logging purposes

**TEXT + IMAGE COMBINATIONS:**
When both text and image are provided, use the text to refine the intent while treating the image as food content.

Consider the user's memory for personalization when classifying intent. User memory contains their past preferences, dietary habits, and context that can help interpret their current request.

Intent types:
1. "new_meal" - User is logging a new meal or food item
    - Examples: "I had pizza for lunch", "ate an apple", "breakfast was oatmeal"
    - **Images of food (default assumption for all food images)**


2. "answer_question" - User is responding to clarification questions from a previous meal logging attempt
    - Responses like "option 1", "grilled", "medium size", "breast meat"
    - Usually short answers or selections from provided options

4. "needs_clarification" - User input is ambiguous and requires clarification questions
    - Examples: "chicken" (which cut), "pasta" (needs sauce/type), "sandwich" (needs filling)
    - Single vague food items that need more details for accurate nutrition calculation
    - **Note: Images typically provide enough visual context to avoid this**

**IMPORTANT:** In a nutrition tracking app, assume ALL inputs are for food logging unless explicitly stated otherwise.

Provide brief reasoning for your classification.

After determining the intent, call pass_to_next_agent() to continue to the next step.

Example output: {"type": "new_meal", "reasoning": "User provided an image of food for logging in nutrition tracker"}

IMPORTANT: Return ONLY the JSON object. No markdown, code blocks, or extra text.""",
    output_schema=Intent,
    output_key="intent",
    tools=[pass_to_next_agent],
)
