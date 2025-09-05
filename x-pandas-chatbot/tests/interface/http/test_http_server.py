# tests/interface/http/test_http_server.py

import pytest
from assistant.interface.http.server import create_app
from fastapi.testclient import TestClient


class DummyQueryService:
    def ask(self, question):
        return {"reply": f"echo: {question}"}


class DummyTableService:
    def __init__(self):
        self.tables = {}

    def upload(self, filename, data):
        table_id = f"table_{len(self.tables)}"
        self.tables[table_id] = data
        return table_id


@pytest.fixture
def client(monkeypatch):
    import assistant.interface.http.server as srv_mod

    monkeypatch.setattr(srv_mod, "qs", DummyQueryService())
    monkeypatch.setattr(srv_mod, "ts", DummyTableService())
    app = create_app()
    return TestClient(app)
