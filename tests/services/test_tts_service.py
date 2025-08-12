# tests/services/test_tts_service.py

from tts_grpc_service.domain.tts import SynthesisRequest
from tts_grpc_service.services.tts_service import TTSService


class DummyProv:
    def synthesize(self, text):
        return b"DUMMY" + text.encode()


def test_service_delegates_to_provider():
    svc = TTSService(provider=DummyProv())
    res = svc.synthesize(SynthesisRequest("ok"))
    assert res.audio_bytes == b"DUMMYok"
