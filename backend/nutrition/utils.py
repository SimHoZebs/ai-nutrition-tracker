from google.cloud import speech


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
            sample_rate_hertz=44100,
        )

        response = client.recognize(config=config, audio=audio)

        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript

        return transcription.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

