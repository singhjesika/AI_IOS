"""Voice Service – speech-to-text and text-to-speech."""
import base64
from app.utils.logger import logger


class VoiceService:
    async def transcribe(self, audio_bytes: bytes) -> str:
        """
        Convert audio bytes to text.
        Extend with Whisper API or Google Speech-to-Text for production.
        """
        try:
            import speech_recognition as sr
            import io
            recognizer = sr.Recognizer()
            audio_file = io.BytesIO(audio_bytes)
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""

    async def synthesize(self, text: str) -> str:
        """
        Convert text to speech audio, return base64 string.
        Extend with ElevenLabs / Google TTS for production.
        """
        try:
            import pyttsx3
            import tempfile, os
            engine = pyttsx3.init()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                path = f.name
            engine.save_to_file(text, path)
            engine.runAndWait()
            with open(path, "rb") as f:
                audio_bytes = f.read()
            os.unlink(path)
            return base64.b64encode(audio_bytes).decode()
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return ""