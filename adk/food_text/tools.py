import requests
import os
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.base_tool import BaseTool
from google.genai import types
from typing import Any, Optional
import json


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


# Callback functions for conditional skipping
def before_food_search_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    parsed_foods = tool_context.state.get("parsed_foods", {})

    questions = parsed_foods.get("questions", [])
    if len(questions) > 0:
        return {"questions": questions, "foods": []}
    return None


def before_calculator_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Parse the condition from the request text
    if not llm_request.contents or not llm_request.contents[0].parts:
        return None
    text = llm_request.contents[0].parts[0].text
    if not text:
        return None
    start = text.find("Condition: ")
    if start == -1:
        return None
    json_str = text[start + len("Condition: ") :].split("\n", 1)[0]
    try:
        search_result = json.loads(json_str)
        if "questions" in search_result:
            content = types.Content(
                role="model", parts=[types.Part(text=json.dumps(search_result))]
            )
            return LlmResponse(content=content)
        else:
            remove_condition_line(llm_request)
    except:
        pass
    return None
