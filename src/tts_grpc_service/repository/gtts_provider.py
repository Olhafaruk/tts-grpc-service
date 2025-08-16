# src/tts-grpc_service/repository/gtts_provider.py
import io
import os

from dotenv import load_dotenv
from gtts import gTTS

from tts_grpc_service.domain.tts import SpeechSynthesizer

load_dotenv()


class GTTSProvider(SpeechSynthesizer):
    def __init__(self, lang=None):
        self.lang = lang or os.getenv("TTS_LANG", "en")

    def synthesize(self, text: str) -> bytes:
        buf = io.BytesIO()
        gTTS(text=text, lang=self.lang).write_to_fp(buf)
        buf.seek(0)
        return buf.read()
