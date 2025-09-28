import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.cloud import speech
import uuid


@api_view(["POST"])
def transcribe_audio(request):
    if "audio" not in request.FILES:
        return Response(
            {"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    audio_file = request.FILES["audio"]
    audio_content = audio_file.read()

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        use_enhanced=True,
        sample_rate_hertz=44100,
    )

    response = client.recognize(config=config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript

    print(f"Results: {len(response.results)}")
    print(f"Transcription: '{transcription}'")

    return Response({"transcription": transcription})


@api_view(["POST"])
def analyze_food(request):
    food_description = request.data.get("food_description")
    if not food_description:
        return Response(
            {"error": "food_description required"}, status=status.HTTP_400_BAD_REQUEST
        )

    user_id = str(request.user.id) if request.user.is_authenticated else "anonymous"
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

    content = agent_response.json()[0].get("content", {})
    print(f"Agent response content: {content}")

    if agent_response.status_code == 200:
        return Response(agent_response.json()[0].get("content", {}))
    else:
        return Response(
            {"error": "Agent call failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
