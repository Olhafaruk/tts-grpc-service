from abc import ABC, abstractmethod
class SynthesisRequest:
    def __init__(self, text: str):
        self.text = text

class SynthesisResponse:
    def __init__(self, audio_bytes: bytes):
        self.audio_bytes = audio_bytes

class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Возвращает аудио-байты по входному тексту."""
        ...
