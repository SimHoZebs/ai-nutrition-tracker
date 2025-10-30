from datetime import datetime
from google.adk.agents import LlmAgent
from google.genai import types
from food_text.models import ParsedFoods
from food_text.tools import (
    lookup_existing_meal,
    process_question_answers,
    pass_to_next_agent,
)

GEMINI_MODEL = "gemini-2.5-flash"


def provide_previous_context_for_answers(callback_context):
    """Provide previous context when answering questions"""
    intent = callback_context.state.get("intent", {})

    # Always provide personalization context
    personalization = callback_context.state.get("personalization", {})
    user_memory = personalization.get("memory", [])
    if user_memory:
        callback_context.state["user_memory"] = user_memory

    if intent.get("type") == "answer_question":
        # Add previous parsed_foods context to the agent's instructions
        previous_foods = callback_context.state.get("parsed_foods", {})
        non_ambiguous_foods = [
            f for f in previous_foods.get("foods", []) if not f.get("ambiguous", False)
        ]
        ambiguous_foods = [
            f for f in previous_foods.get("foods", []) if f.get("ambiguous", False)
        ]
        questions = previous_foods.get("questions", [])

        # Store context for the agent to use
        callback_context.state["previous_non_ambiguous_foods"] = non_ambiguous_foods
        callback_context.state["previous_ambiguous_foods"] = ambiguous_foods
        callback_context.state["previous_questions"] = questions

    elif intent.get("type") == "update_meal":
        # Add looked up meal context for updates
        # The agent framework stores tool results in state
        looked_up_meal = callback_context.state.get("lookup_existing_meal", {})
        callback_context.state["existing_meal"] = looked_up_meal

    return None


# Sub-Agent: Parse input description
input_parser_agent = LlmAgent(
    name="InputParserAgent",
    model=GEMINI_MODEL,
    instruction=f"""It is currently {datetime.now().isoformat()}.

Consider the user's memory for personalization when parsing food descriptions. User memory contains their past preferences, dietary habits, and context that can help interpret quantities, meal types, and food choices.

CONDITIONAL BEHAVIOR BASED ON INTENT:

If intent.type == "new_meal":
Parse the user's food description into a JSON object conforming to the ParsedFoods schema: a JSON object with "foods" (list of UnknownFood objects, each with "name" string, "description" string, "eaten_at" string, "meal_type" string, "quantity" float default 1.0, "unit" string default "serving", "ambiguous" bool default false) and "questions" (list of question objects, each with "question" string, "type" string, "mcqOptions" list of strings, "sliderValue" int).

For each food, provide ALL fields: name, description, eaten_at, meal_type, quantity, unit, ambiguous.

If intent.type == "needs_clarification":
Parse the ambiguous food input and generate clarification questions. Set ambiguous=true for foods that need clarification, and provide appropriate questions.

For eaten_at, parse time references from user input:
- If no time mentioned: use current datetime
- "yesterday": subtract 1 day from current datetime
- "this morning": today at 8:00 AM
- "this afternoon": today at 2:00 PM
- "this evening": today at 7:00 PM
- "last night": yesterday at 9:00 PM
- "lunch": today at 12:00 PM
- "dinner": today at 7:00 PM
- "breakfast": today at 8:00 AM
- Specific times like "2 hours ago": subtract from current datetime
- Always return eaten_at as ISO datetime string (YYYY-MM-DDTHH:MM:SS format)

If ambiguous, add clarifying questions. For multiple_choice questions, provide: question, type="multiple_choice", mcqOptions (list of options), sliderValue=0. For slider questions, provide: question, type="slider", mcqOptions=[], sliderValue (default value).

If intent.type == "answer_question":
1. Access the previous parsed_foods context from the callback state
2. Take the non-ambiguous foods from the original request (foods where ambiguous=false)
3. Parse the user's answers to resolve the ambiguous foods (foods where ambiguous=true)
4. Combine the resolved ambiguous foods with the original non-ambiguous foods
5. Return ParsedFoods format with ALL foods (both resolved and non-ambiguous) ready for processing
6. Set questions=[] since all ambiguity has been resolved

Example new_meal output: {{"foods": [{{"name": "apple", "description": "red apple", "eaten_at": "2025-09-28T08:00:00", "meal_type": "Breakfast", "quantity": 2.0, "unit": "pieces"}}], "questions": []}}.

IMPORTANT: Return ONLY the JSON object. Do not wrap in markdown, code blocks, backticks, or any formatting. No ```json or extra text.""",
    output_schema=ParsedFoods,
    output_key="parsed_foods",
    before_agent_callback=provide_previous_context_for_answers,
    tools=[process_question_answers, pass_to_next_agent],
)
