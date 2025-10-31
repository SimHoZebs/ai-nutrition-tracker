from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Any, Optional


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
