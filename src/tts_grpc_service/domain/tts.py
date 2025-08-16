from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SynthesisRequest:
    text: str


@dataclass
class SynthesisResponse:
    audio_bytes: bytes


class SpeechSynthesizer(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        pass
