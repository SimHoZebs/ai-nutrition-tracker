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
