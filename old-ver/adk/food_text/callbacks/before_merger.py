from google.genai import types
import json


def skip_merger_if_questions_pending(callback_context):
    """Skip merger if questions are pending"""
    if callback_context.state.get("questions_pending", False):
        # Questions are pending, skip merger execution
        parsed_foods = callback_context.state.get("parsed_foods", {})
        return types.Content(
            role="assistant",
            parts=[types.Part(text=json.dumps(parsed_foods))],
        )
    return None
