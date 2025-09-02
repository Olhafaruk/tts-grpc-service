#tests/infrastructure/test_weaviate_client.py

import pytest
from weaviate.exceptions import UnexpectedStatusCodeException
import assistant.infrastructure.weaviate_client as wc_mod

class DummySchema:
    def __init__(self, classes):
        self._classes = classes
        self.created = False
    def get(self):
        return {"classes": [{"class": name} for name in self._classes]}
    def create_class(self, schema):
        self.created = True

class DummyClient:
    def __init__(self, url, startup_period):

        self.schema = DummySchema([])

def test_ensure_schema_creates_when_missing(monkeypatch):

    monkeypatch.setattr(
        wc_mod, "Client",
        lambda url, startup_period: DummyClient(url, startup_period)
    )
    wc = wc_mod.WeaviateClient()
    assert wc.client.schema.created is True

def test_ensure_schema_skips_when_exists(monkeypatch):

    class ClientWithClass(DummyClient):
        def __init__(self, url, startup_period):
            super().__init__(url, startup_period)
            self.schema = DummySchema(["TableDoc"])

    monkeypatch.setattr(
        wc_mod, "Client",
        lambda url, startup_period: ClientWithClass(url, startup_period)
    )
    wc = wc_mod.WeaviateClient()
    assert wc.client.schema.created is False
