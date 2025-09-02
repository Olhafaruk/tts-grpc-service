#tests/application/test_query_service.py

import pytest
from assistant.application.query_service import QueryService

class DummyQuery:
    def __init__(self, data):
        self._data = data
        self.calls = []
    def get(self, class_name, attrs):
        self.calls.append(("get", class_name, attrs))
        return self
    def with_near_text(self, arg):
        self.calls.append(("near_text", arg))
        return self
    def with_additional(self, attrs):
        self.calls.append(("additional", attrs))
        return self
    def do(self):
        return {"data": {"Get": {"TableDoc": self._data}}}

class DummyClient:
    def __init__(self, data):
        self.query = DummyQuery(data)

class DummyVDB:
    def __init__(self, data):
        self.client = DummyClient(data)

def test_find_tables_returns_tuples():
    sample = [
        {"table_id": "id1", "text": "t1", "_additional": {"certainty": 0.9}},
        {"table_id": "id2", "text": "t2", "_additional": {"certainty": 0.8}}
    ]
    vdb = DummyVDB(sample)
    service = QueryService(vdb=vdb)

    result = service.find_tables("any query", certainty=0.5)

    assert result == [
        ("id1", "t1", 0.9),
        ("id2", "t2", 0.8)
    ]
