# tests/interface/grpc/test_server.py

import pandas as pd
import pytest
from assistant.interface.grpc import assistant_pb2
from assistant.interface.grpc.server import AssistantServicer


class DummyQueryService:
    def ask(self, tables, question):
        return [{"text": f"echo: {question.text}"}]


@pytest.fixture
def servicer(monkeypatch):
    # Подменяем глобальный qs внутри сервера
    monkeypatch.setattr("assistant.interface.grpc.server.qs", DummyQueryService())
    return AssistantServicer()
