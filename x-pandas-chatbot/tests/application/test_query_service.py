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


@pytest.fixture
def table_service():
    return TableService()


@pytest.fixture
def query_service(table_service):
    return QueryService(ts=table_service, vdb=DummyVDB([]))


def test_merge_tables(query_service, table_service):
    data1 = b"Currency,Rate\nEUR,1.1\nGBP,1.25"
    data2 = b"Currency,Country\nEUR,Germany\nGBP,UK"
    id1 = table_service.upload("rates.csv", data1)
    id2 = table_service.upload("meta.csv", data2)
    args = {"table1_id": id1, "table2_id": id2, "on": ["Currency"], "how": "inner"}
    result = query_service._execute("merge_tables", args)
    df = table_service.get_any(result["table_id"])
    assert "Country" in df.columns
    assert len(df) == 2


def test_rename_column(query_service, table_service):
    csv_data = b"Currency,Rate to USD\nEUR,1.1\nGBP,1.25"
    table_id = table_service.upload("rates.csv", csv_data)
    args = {"table_id": table_id, "old_name": "Rate to USD", "new_name": "Exchange Rate"}
    result = query_service._execute("rename_column", args)
    df = table_service.get_any(result["table_id"])
    assert "Exchange Rate" in df.columns
    assert "Rate to USD" not in df.columns


def test_aggregate_column(query_service, table_service):
    csv_data = b"Country,Rate to USD\nGermany,1.1\nGermany,1.2\nUK,1.25"
    table_id = table_service.upload("rates.csv", csv_data)
    args = {"table_id": table_id, "column": "Rate to USD", "agg": "mean", "group_by": "Country"}
    result = query_service._execute("aggregate_column", args)
    assert "Germany" in result["summary"]
    assert "UK" in result["summary"]
    assert round(result["summary"]["Germany"], 2) == 1.15


def test_convert_currency(query_service, table_service):
    csv_data = b"Currency,Rate to USD,Date\nEUR,1.1,2025-01-01\nGBP,1.25,2025-01-01"
    table_id = table_service.upload("rates.csv", csv_data)
    args = {"table_id": table_id, "currency": "EUR", "amount": 100, "date": "2025-01-01"}
    result = query_service._execute("convert_currency", args)
    assert "text" in result
    assert "EUR" in result["text"]
    assert "100" in result["text"]
