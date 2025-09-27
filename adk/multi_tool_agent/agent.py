import requests
from google.adk.agents import SequentialAgent, LlmAgent

GEMINI_MODEL = "gemini-2.5-flash"


# Define API tools
def search_usda(query: str) -> dict:
    """Search USDA FoodData Central for foods matching the query."""
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={query}"
    response = requests.get(url)
    print(f"USDA api response status: {response.status_code}")
    return (
        response.json() if response.status_code == 200 else {"error": "USDA API failed"}
    )


def search_off(query: str) -> dict:
    """Search OpenFoodFacts for products matching the query."""
    headers = {
        "User-Agent": "NutritionTracker/1.0 (contact@example.com)"
    }  # Custom User-Agent
    url = f"https://world.openfoodfacts.org/api/v2/search?q={query}"
    response = requests.get(url, headers=headers)
    return (
        response.json() if response.status_code == 200 else {"error": "OFF API failed"}
    )


# Sub-Agent 1: Parse input description
input_parser_agent = LlmAgent(
    name="InputParserAgent",
    model=GEMINI_MODEL,
    instruction="""Parse the user's food description into a JSON list of food items.
    Extract name, quantity (default 1), and unit (default 'serving').
    Example output: {"foods": [{"name": "apple", "quantity": 2, "unit": "pieces"}, {"name": "banana", "quantity": 1, "unit": "serving"}]}.
    Output only valid JSON.""",
    output_key="parsed_foods",
)

# Sub-Agent 2: Search APIs and merge results
food_search_agent = LlmAgent(
    name="FoodSearchAgent",
    model=GEMINI_MODEL,
    instruction="""For each food in {parsed_foods}['foods'], call search_usda and search_off with the food name.
    For each food, select the best matching result from combined API data (prioritize USDA for accuracy if duplicates).
    Extract nutrition per serving (e.g., calories, protein, carbs, fat) and serving size.
    Output a list of dicts: [{"name": "apple", "nutrition": {"calories": 95, "protein_g": 0.5, ...}, "serving_size": "1 medium"}, ...].
    Handle missing data gracefully.""",
    tools=[search_usda, search_off],
    output_key="food_data_list",
)

# Sub-Agent 3: Calculate total nutrition
nutrition_calculator_agent = LlmAgent(
    name="NutritionCalculatorAgent",
    model=GEMINI_MODEL,
    instruction="""Take {food_data_list} and scale each food's nutrition by its quantity (approximate units if needed, e.g., 1 piece ≈ 1 serving).
    Sum nutrition values across all foods.
    Output total nutrition as a dict: {"total_calories": 200, "total_protein_g": 5, ...}.""",
    output_key="total_nutrition",
)

# Root SequentialAgent
root_agent = SequentialAgent(
    name="NutritionTrackerAgent",
    sub_agents=[input_parser_agent, food_search_agent, nutrition_calculator_agent],
    description="Sequentially parses food descriptions, searches APIs, merges data, and calculates total nutrition.",
)
