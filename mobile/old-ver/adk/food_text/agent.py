from google.adk.agents import SequentialAgent
from food_text.models import *
from food_text.subagents.IntentClassificationAgent import intent_classification_agent
from food_text.subagents.InputParserAgent import input_parser_agent
from food_text.subagents.ParallelFoodProcessorAgent import ParallelFoodProcessorAgent
from food_text.subagents.MergerAgent import merger_agent

# Root SequentialAgent
root_agent = SequentialAgent(
    name="NutritionTrackerAgent",
    sub_agents=[
        intent_classification_agent,
        input_parser_agent,
        ParallelFoodProcessorAgent(),
        merger_agent,
    ],
    description="Classifies user intent, then parses meals, processes them in parallel, and merges total nutrition.",
)
