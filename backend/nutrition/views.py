import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
from foods.models import Food
from foods.serializers import FoodSerializer
from nutrition.utils import transcribe_audio_content


@api_view(["POST"])
def process_request(request):
    food_description = request.data.get("food_description")

    # Handle audio input
    if not food_description and "audio" in request.FILES:
        audio_file = request.FILES["audio"]
        audio_content = audio_file.read()
        food_description = transcribe_audio_content(audio_content)

        if not food_description:
            return Response(
                {"error": "Failed to transcribe audio"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    if not food_description:
        return Response(
            {"error": "food_description or audio file required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if user is authenticated before saving
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required to save foods"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    user_id = str(request.user.id)
    agent_base_url = os.environ.get("AGENT_BASE_URL", "http://adk:8080")
    session_id = str(uuid.uuid4())

    # Create or update session
    session_url = (
        f"{agent_base_url}/apps/food_text/users/{user_id}/sessions/{session_id}"
    )
    session_response = requests.post(session_url, json={"state": {}})
    if session_response.status_code not in [200, 201]:
        return Response(
            {"error": "Failed to create session"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Now call the agent
    agent_response = requests.post(
        f"{agent_base_url}/run",
        json={
            "app_name": "food_text",
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {"role": "user", "parts": [{"text": food_description}]},
        },
    )

    content = agent_response.json()[-1].get("content", {})
    print(f"Agent response content: {content}")
    questions = content.get("questions", [])
    foods = content.get("foods", [])
    if questions:
        print(f"Questions detected: {questions}")

    # Handle the case when no questions exist - save foods to database
    if not questions and foods:
        print(f"No questions - saving {len(foods)} foods to database")

        try:
            created_foods = []
            for food in foods:
                # Save each food item to the database
                food_obj = Food.objects.create(
                    name=food.get("name", ""),
                    meal_type=food.get("meal_type"),
                    serving_size=food.get("serving_size", 100),
                    calories=food.get("calories", 0.0),
                    protein=food.get("protein", 0.0),
                    carbohydrates=food.get("carbohydrates", 0.0),
                    trans_fat=food.get("trans_fat", 0.0),
                    saturated_fat=food.get("saturated_fat", 0.0),
                    unsaturated_fat=food.get("unsaturated_fat", 0.0),
                    others=food.get("others", {}),
                    user=request.user,
                )
                created_foods.append(food_obj)
                print(f"Created food entry: {food_obj.name} (ID: {food_obj.id})")

            # Serialize the created food objects
            serialized_foods = FoodSerializer(created_foods, many=True).data

            # Add database info to response
            response_content = content.copy()
            response_content["response"] = serialized_foods

        except Exception as e:
            print(f"Error creating food entries: {e}")
            response_content = content.copy()
            response_content["error"] = str(e)
    elif questions:
        print(f"Questions detected: {questions}")
        response_content = content
    else:
        print("No foods or questions detected in agent response")
        response_content = content

    if agent_response.status_code == 200:
        return Response(response_content)
    else:
        return Response(
            {"error": "Agent call failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def resubmit():
    pass
