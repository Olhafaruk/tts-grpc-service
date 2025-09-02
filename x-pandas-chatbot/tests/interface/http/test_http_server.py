# tests/interface/http/test_http_server.py

import pytest
from fastapi.testclient import TestClient


from assistant.interface.http.server import app


class DummyQueryService:
    def answer_question(self, q):
        return "it works!"

@pytest.fixture(autouse=True)
def patch_query_service(monkeypatch):

    import assistant.interface.http.server as srv_mod
    monkeypatch.setattr(srv_mod, "qs", DummyQueryService())

def test_ask_endpoint_returns_answer():
    client = TestClient(app)
    response = client.post("/ask", json={"question": "hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "it works!"}
