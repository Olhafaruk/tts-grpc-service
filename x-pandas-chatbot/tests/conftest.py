# x-pandas-chatbot/tests/conftest.py

import os
import sys

import pytest
from assistant.application.query_service import QueryService
from assistant.application.table_store import TableService
from assistant.interface.http.server import create_app
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


@pytest.fixture(autouse=True)
def mock_weaviate(monkeypatch):
    class DummyWeaviateClient:
        def index_table(self, *args, **kwargs):
            pass

        def query(self):
            return self

        def get(self, *args, **kwargs):
            return self

        def with_near_text(self, *args, **kwargs):
            return self

        def with_additional(self, *args, **kwargs):
            return self

        def do(self):
            return {"data": {"Get": {"TableDoc": []}}}

    monkeypatch.setattr(
        "assistant.application.table_store.WeaviateClient", DummyWeaviateClient
    )


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("WEAVIATE_URL", "http://weaviate:8080")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")


@pytest.fixture
def table_service():
    return TableService()


@pytest.fixture
def query_service(table_service):
    return QueryService(ts=table_service)


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
