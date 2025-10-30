import base64
import os

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
from nutrition.utils import (
    transcribe_audio_content,
    create_error_response,
    validate_authentication,
)
from nutrition.agent import (
    build_agent_payload,
    send_agent_request,
    process_agent_response,
)
from users.utils import get_user_memory


@api_view(["POST"])
def process_request(request):
    food_description = request.data.get("food_description")
    image_data = None

    if not food_description and "audio" in request.FILES:
        audio_file = request.FILES["audio"]
        audio_content = audio_file.read()
        food_description = transcribe_audio_content(audio_content)

        if not food_description:
            return create_error_response(
                "Failed to transcribe audio", status.HTTP_400_BAD_REQUEST
            )

    # Handle photo uploads (can be combined with text)
    if "photo" in request.FILES:
        photo = request.FILES["photo"]
        photo_content = photo.read()
        photo_base64 = base64.b64encode(photo_content).decode("utf-8")
        image_data = {
            "mimeType": photo.content_type,
            "data": photo_base64
        }

    if not food_description and not image_data:
        return create_error_response(
            "food_description, audio file, or photo required",
            status.HTTP_400_BAD_REQUEST,
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

    # Get user memory for personalization
    user_memory = get_user_memory(request.user)
    personalization = {"memory": user_memory} if user_memory else None

    # Call the agent
    payload = build_agent_payload(
        user_id,
        session_id,
        food_description,
        image_data,
        personalization,
    )
    agent_response = send_agent_request(agent_base_url, payload)

    if agent_response.status_code != 200:
        return create_error_response(
            "Agent call failed", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    content = agent_response.json()[-1].get("content", {})
    print("agent response", content)
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

    # Get user memory for personalization
    user_memory = get_user_memory(request.user)
    personalization = {"memory": user_memory} if user_memory else None

    # Call the agent with the answers using the stored session_id
    payload = build_agent_payload(
        user_id, session_id, answer_text, None, personalization
    )
    agent_response = send_agent_request(agent_base_url, payload)

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
