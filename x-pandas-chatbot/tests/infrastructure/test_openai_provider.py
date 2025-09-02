#tests/infrastructure/test_openai_provider.py

import pytest
import assistant.infrastructure.openai_provider as oai_mod

def test_complete_invokes_openai(monkeypatch):
    calls = {}

    class DummyChoice:
        def __init__(self):
            self.message = {"content": "fake-answer"}
    class DummyResponse:
        choices = [DummyChoice()]

    def fake_create(model, messages, max_tokens):
        calls["model"] = model
        calls["messages"] = messages
        calls["max_tokens"] = max_tokens
        return DummyResponse()

    monkeypatch.setattr(
        oai_mod.openai.ChatCompletion,
        "create",
        staticmethod(fake_create)
    )

    provider = oai_mod.OpenAIProvider()
    answer = provider.complete("QUESTION", model="mymodel")

    assert answer == "fake-answer"
    assert calls["model"] == "mymodel"
    assert calls["messages"] == [{"role": "user", "content": "QUESTION"}]
    assert calls["max_tokens"] == 256
