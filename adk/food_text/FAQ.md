# Nutrition Tracker Agent FAQ

## How does the agent handle vague food inputs?
The agent detects vagueness (e.g., "chicken" without type/preparation details) during input parsing. If vague, it returns clarifying questions instead of proceeding with API searches or nutrition calculations, while making reasonable assumptions (e.g., no questions for salt on fries).

## How is vagueness detected?
The InputParserAgent LLM analyzes the description and outputs JSON with a "questions" array if ambiguity is found. Clear inputs have an empty array.

## How are conditional skips implemented?
`before_model_callback`s on FoodSearchAgent and NutritionCalculatorAgent parse embedded input JSON from the request, check for non-empty questions, and return an `LlmResponse` to skip the LLM call if questions exist. If clear, the condition line is removed from the instruction before proceeding.

## Why before_model_callback over after_model_callback?
`before_model_callback` skips unnecessary LLM calls entirely. `after_model_callback` only modifies responses post-call, which doesn't prevent execution and is less efficient for this use case.