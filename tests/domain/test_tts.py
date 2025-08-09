# tests/domain/test_tts.py
from domain.tts import SynthesisRequest, SynthesisResponse


def test_models_hold_values():
    req = SynthesisRequest("hello")
    assert req.text == "hello"
    res = SynthesisResponse(b"\x00\x01")
    assert res.audio_bytes == b"\x00\x01"
