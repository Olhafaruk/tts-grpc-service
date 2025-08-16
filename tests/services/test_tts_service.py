# tests/services/test_tts_service.py

from tts_grpc_service.domain.tts import SpeechSynthesizer, SynthesisRequest
from tts_grpc_service.services.tts_service import TTSService


class DummySynthesizer(SpeechSynthesizer):
    def __init__(self):
        self.last_text = None
        self.output_bytes = b"FAKE_AUDIO"

    def synthesize(self, text: str) -> bytes:
        self.last_text = text
        return self.output_bytes


def test_service_delegates_to_synthesizer():
    # Arrange
    synth = DummySynthesizer()
    service = TTSService(synthesizer=synth)

    # Act
    result = service.synthesize(SynthesisRequest("ok"))

    # Assert
    assert result.audio_bytes == b"FAKE_AUDIO"
    assert synth.last_text == "ok"
