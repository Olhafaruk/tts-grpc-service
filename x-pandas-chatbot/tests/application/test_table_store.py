import pytest
from assistant.application.table_store import TableService


@pytest.fixture
def table_service():
    return TableService()


def test_upload_csv_and_get_any(table_service):
    csv_data = b"Date,Currency,Rate\n2025-01-01,EUR,1.1"
    table_id = table_service.upload("test.csv", csv_data)
    df = table_service.get_any(table_id)
    assert df.shape == (1, 3)
    assert "Currency" in df.columns


def test_get_by_filename(table_service):
    csv_data = b"Currency,Rate\nEUR,1.1"
    _ = table_service.upload("rates.csv", csv_data)
    df = table_service.get_by_filename("rates.csv")
    assert df.loc[0, "Currency"] == "EUR"
