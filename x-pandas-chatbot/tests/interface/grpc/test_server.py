#tests/interface/grpc/test_server.py

import pytest
import pandas as pd
from assistant.interface.grpc.server import AssistantServicer
from assistant.interface.grpc import assistant_pb2


class DummyQueryService:
    def ask(self, tables, question):
        return [{"text": f"echo: {question.text}"}]


@pytest.fixture
def servicer(monkeypatch):
    # Подменяем глобальный qs внутри сервера
    monkeypatch.setattr("assistant.interface.grpc.server.qs", DummyQueryService())
    return AssistantServicer()







