import io
import os

from dotenv import load_dotenv
from gtts import gTTS

from tts_grpc_service.domain.tts import TTSProvider


load_dotenv()


class GTTSProvider(TTSProvider):
    def __init__(self):
        self.lang = os.getenv("TTS_LANG", "en")

    def synthesize(self, text: str) -> bytes:
        buf = io.BytesIO()
        gTTS(text=text, lang=self.lang).write_to_fp(buf)
        buf.seek(0)
        return buf.read()
