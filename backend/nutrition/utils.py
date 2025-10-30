from google.cloud import speech
from rest_framework.response import Response
from rest_framework import status


def transcribe_audio_content(audio_content):
    """
    Transcribe audio content using Google Cloud Speech-to-Text.

    Args:
        audio_content (bytes): The audio file content as bytes

    Returns:
        str: The transcribed text, or empty string if transcription fails
    """
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            language_code="en-US",
            use_enhanced=True,
        )

        response = client.recognize(config=config, audio=audio)

        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript

        return transcription.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""


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


def create_error_response(message, status_code):
    return Response({"error": message}, status=status_code)


def validate_authentication(user):
    if not user.is_authenticated:
        return create_error_response(
            "Authentication required", status.HTTP_401_UNAUTHORIZED
        )
    return None

