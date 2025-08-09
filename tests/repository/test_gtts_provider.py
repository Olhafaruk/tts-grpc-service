# tests/repository/test_gtts_provider.py


from repository.gtts_provider import GTTSProvider


def test_gtts_returns_bytes(monkeypatch):
    monkeypatch.setenv("TTS_LANG", "en")
    prov = GTTSProvider()
    audio = prov.synthesize("hi")
    assert isinstance(audio, (bytes, bytearray))
    assert len(audio) > 0
