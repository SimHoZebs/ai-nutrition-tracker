import base64
import os
from datetime import timezone, datetime

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
from foods.serializers import FoodSerializer, AgentFoodResponseSerializer
from nutrition.utils import transcribe_audio_content
from django.core.files.uploadedfile import InMemoryUploadedFile


def create_error_response(message, status_code):
    return Response({"error": message}, status=status_code)


def validate_authentication(user):
    if not user.is_authenticated:
        return create_error_response(
            "Authentication required", status.HTTP_401_UNAUTHORIZED
        )
    return None


def create_foods_from_data(foods_data, user):
    """Create Food objects using the AgentFoodResponseSerializer"""
    created_foods = []
    for food_data in foods_data:
        serializer = AgentFoodResponseSerializer(data=food_data, context={"user": user})
        if serializer.is_valid():
            food_obj = serializer.save()
            created_foods.append(food_obj)
            print(f"Created food entry: {food_obj.name} (ID: {food_obj.id})")
        else:
            print(f"Invalid food data: {serializer.errors}")
            print(f"Food data was: {food_data}")
    return created_foods


def update_existing_foods(foods_data, user):
    """Update existing Food objects based on agent response data"""
    updated_foods = []
    for food_data in foods_data:
        if 'id' in food_data:
            try:
                food = Food.objects.get(id=food_data['id'], user=user)
                serializer = AgentFoodResponseSerializer(food, data=food_data, partial=True, context={"user": user})
                if serializer.is_valid():
                    food_obj = serializer.save()
                    updated_foods.append(food_obj)
                    print(f"Updated food entry: {food_obj.name} (ID: {food_obj.id})")
                else:
                    print(f"Invalid update data: {serializer.errors}")
                    print(f"Food data was: {food_data}")
            except Food.DoesNotExist:
                print(f"Food with id {food_data['id']} not found for user {user}")
    return updated_foods


def call_agent_api(agent_base_url, user_id, session_id, message_text):
    agent_response = requests.post(
        f"{agent_base_url}/run",
        json={
            "app_name": "food_text",
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {"role": "user", "parts": [{"text": message_text}]},
        },
    )
    return agent_response


def process_agent_response(content, user, clear_session_callback=None):
    print(f"Agent response content: {content}")
    questions = content.get("questions", [])
    foods = content.get("foods", [])
    request_type = content.get("request_type", "new")

    # Check for questions/foods in parts structure
    if "parts" in content and content["parts"]:
        for part in content["parts"]:
            if "text" in part:
                try:
                    import json

                    text_content = json.loads(part["text"])

                    # Check if this part contains questions
                    if isinstance(text_content, dict) and "questions" in text_content:
                        questions.extend(text_content["questions"])

                    # Check if this part contains foods (as JSON array)
                    elif isinstance(text_content, list) and len(text_content) > 0:
                        # Assume this is a list of foods if it has typical food fields
                        if all(
                            isinstance(item, dict) and "name" in item
                            for item in text_content
                        ):
                            foods.extend(text_content)

                except (json.JSONDecodeError, TypeError):
                    continue

    if questions:
        print(f"Questions detected: {questions}")
        return content
    elif foods:
        print(f"No questions - saving {len(foods)} foods to database")
        try:
            if request_type == "update":
                update_existing_foods(foods, user)

            # Use the serializer to handle field mapping and validation
            created_foods = create_foods_from_data(foods, user)
            serialized_foods = FoodSerializer(created_foods, many=True).data

            response_content = content.copy()
            response_content["response"] = serialized_foods

            if clear_session_callback:
                clear_session_callback()

            return response_content
        except Exception as e:
            print(f"Error creating food entries: {e}")
            response_content = content.copy()
            response_content["error"] = str(e)
            return response_content
    else:
        print("No foods or questions detected in agent response")
        if clear_session_callback:
            clear_session_callback()
        return content


@api_view(["POST"])
def process_request(request):
    food_description = request.data.get("food_description")

    if not food_description and "audio" in request.FILES:
        audio_file = request.FILES["audio"]
        audio_content = audio_file.read()
        food_description = transcribe_audio_content(audio_content)

        if not food_description:
            return create_error_response(
                "Failed to transcribe audio", status.HTTP_400_BAD_REQUEST
            )
    elif not food_description and "photo" in request.FILES:
        # TODO the photo is received here. image/jpeg mime type
        photo = request.FILES["photo"]

    if not food_description:
        return create_error_response(
            "food_description or audio file required", status.HTTP_400_BAD_REQUEST
        )

    # Check authentication
    auth_error = validate_authentication(request.user)
    if auth_error:
        return auth_error

    user_id = str(request.user.id)
    agent_base_url = os.environ.get("AGENT_BASE_URL", "http://adk:8080")
    session_id = str(uuid.uuid4())

    # Store session_id in Django HTTP session for resubmit functionality
    request.session["chat_session_id"] = session_id

    # Create or update session
    session_url = (
        f"{agent_base_url}/apps/food_text/users/{user_id}/sessions/{session_id}"
    )
    session_response = requests.post(session_url, json={"state": {}})
    if session_response.status_code not in [200, 201]:
        return create_error_response(
            "Failed to create session", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Call the agent
    agent_response = call_agent_api(
        agent_base_url, user_id, session_id, food_description
    )

    if agent_response.status_code != 200:
        return create_error_response(
            "Agent call failed", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    content = agent_response.json()[-1].get("content", {})
    response_content = process_agent_response(content, request.user)

    return Response(response_content)


@api_view(["POST"])
def resubmit(request):
    # Get the stored session_id from Django HTTP session
    session_id = request.session.get("chat_session_id")

    if not session_id:
        return create_error_response(
            "No active chat session found. Please start a new conversation.",
            status.HTTP_400_BAD_REQUEST,
        )

    # Check authentication
    auth_error = validate_authentication(request.user)
    if auth_error:
        return auth_error

    # Get user answers from request
    answers = request.data.get("answers", [])

    if not answers:
        return create_error_response(
            "Answers are required for resubmission", status.HTTP_400_BAD_REQUEST
        )

    user_id = str(request.user.id)
    agent_base_url = os.environ.get("AGENT_BASE_URL", "http://adk:8080")

    # Format answers as a message for the agent
    answer_text = " ".join(
        [f"Answer {i+1}: {answer}" for i, answer in enumerate(answers)]
    )

    # Call the agent with the answers using the stored session_id
    agent_response = call_agent_api(agent_base_url, user_id, session_id, answer_text)

    if agent_response.status_code != 200:
        return create_error_response(
            "Agent call failed", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    content = agent_response.json()[-1].get("content", {})

    def clear_session():
        if "chat_session_id" in request.session:
            del request.session["chat_session_id"]

    response_content = process_agent_response(content, request.user, clear_session)

    return Response(response_content)
