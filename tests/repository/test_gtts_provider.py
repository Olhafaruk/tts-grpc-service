# tests/repository/test_gtts_provider.py


from tts_grpc_service.domain.tts import SpeechSynthesizer
from tts_grpc_service.repository.gtts_provider import GTTSProvider


def test_gtts_provider_implements_interface():
    prov = GTTSProvider()
    assert isinstance(prov, SpeechSynthesizer)


def test_gtts_returns_bytes(monkeypatch):
    monkeypatch.setenv("TTS_LANG", "en")
    prov = GTTSProvider()
    audio = prov.synthesize("hi")
    assert isinstance(audio, (bytes, bytearray))
    assert len(audio) > 0
