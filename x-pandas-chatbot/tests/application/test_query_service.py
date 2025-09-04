#tests/application/test_query_service.py

import pytest
from assistant.application.query_service import QueryService
from assistant.application.table_store import TableService


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


def test_convert_currency(query_service, table_service):
    csv_data = b"Currency,Rate to USD\nEUR,1.1\nGBP,1.25"
    table_id = table_service.upload("rates.csv", csv_data)
    args = {"table_id": table_id, "column": "Rate to USD", "exchange_rate": 2}
    result = query_service._execute("convert_currency", args)
    df = table_service.get_any(result["table_id"])
    assert df["Rate to USD"].iloc[0] == 2.2

def test_merge_tables(query_service, table_service):
    data1 = b"Currency,Rate\nEUR,1.1\nGBP,1.25"
    data2 = b"Currency,Country\nEUR,Germany\nGBP,UK"
    id1 = table_service.upload("rates.csv", data1)
    id2 = table_service.upload("meta.csv", data2)
    args = {"table1_id": id1, "table2_id": id2, "on": "Currency", "how": "inner"}
    result = query_service._execute("merge_tables", args)
    df = table_service.get_any(result["table_id"])
    assert "Country" in df.columns
