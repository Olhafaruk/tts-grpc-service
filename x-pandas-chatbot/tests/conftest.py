# x-pandas-chatbot/tests/conftest.py

import os, sys, pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):

    monkeypatch.setenv("WEAVIATE_URL", "http://weaviate:8080")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
