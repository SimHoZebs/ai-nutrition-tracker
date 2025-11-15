from google.adk.models.llm_request import LlmRequest
import requests
from typing import Optional
from datetime import datetime


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


API_BASE_URL = "http://api"


def lookup_existing_meal(
    meal_reference: str, user_id: int, context_date: Optional[str] = None
) -> dict:
    """
    Tool to find existing meals based on natural language references.

    Args:
        meal_reference: Natural language reference like "my breakfast", "yesterday's lunch", "the pizza I logged"
        user_id: ID of the user making the request
        context_date: ISO datetime string for context (defaults to now)

    Returns:
        Dict with meal data if found, empty dict if not found
    """
    if not context_date:
        context_date = datetime.now().isoformat()

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/foods/lookup/",
            params={
                "meal_reference": meal_reference,
                "user_id": user_id,
                "context_date": context_date,
            },
            timeout=10,
        )

        if response.ok:
            return response.json()
        else:
            return {"found": False, "error": f"API error: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"found": False, "error": f"Request failed: {str(e)}"}


def process_question_answers() -> None:
    """
    Tool to process answers to clarification questions and resolve ambiguous foods.

    Args:
        answers: User's answers to questions {"question_1": "option_2", "question_2": "grilled"}
        previous_context: Previous parsing context with ambiguous foods

    Returns:
        None - processing happens through the normal agent flow
    """
    # Answer processing is handled by the agent flow, not through API calls
    return None


def pass_to_next_agent() -> None:
    """
    Tool to signal completion and pass control to the next agent.
    Returns None to continue normal agent flow.
    """
    return None
