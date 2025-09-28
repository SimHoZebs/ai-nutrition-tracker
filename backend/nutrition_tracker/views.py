from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.cloud import speech


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

    try:
        response = client.recognize(config=config, audio=audio)

        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript

        print(f"Results: {len(response.results)}")
        print(f"Transcription: '{transcription}'")

        return Response({"transcription": transcription})
        
    except Exception as e:
        error_msg = str(e)
        if "Invalid recognition 'config'" in error_msg or "bad encoding" in error_msg:
            return Response(
                {"error": "Invalid audio format. Please upload a valid audio file."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Audio transcription failed. Please try again."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
