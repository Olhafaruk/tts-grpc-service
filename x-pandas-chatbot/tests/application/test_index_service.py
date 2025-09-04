#x-pandas-chatbot/tests/application/test_index_service.py

import uuid
import pandas as pd
import pytest
from assistant.application.index_service import IndexService

class DummyDataObject:
    def __init__(self):
        self.created = []
    def create(self, props, class_name, uuid):
        self.created.append({
            "props": props,
            "class_name": class_name,
            "id": uuid
        })

class DummyClient:
    def __init__(self):
        self.data_object = DummyDataObject()

class DummyVDB:
    def __init__(self):
        self.client = DummyClient()

    def index_table(self, table_id, name, df):
        self.client.data_object.create(
            props={
                "table_id": table_id,
                "text": f"Table cols={list(df.columns)} samples={df.head(3).to_dict()}"
            },
            class_name="TableDoc",
            uuid=table_id
        )

@pytest.fixture(autouse=True)
def fixed_uuid(monkeypatch):

    monkeypatch.setattr(
        uuid, "uuid4",
        lambda: uuid.UUID("12345678-1234-5678-1234-567812345678")
    )

def test_index_table_creates_object_and_returns_uuid():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    vdb = DummyVDB()
    service = IndexService(vdb=vdb)

    table_id = "12345678-1234-5678-1234-567812345678"
    returned_id = service.index_table(table_id, "test.csv", df)

    assert returned_id == table_id


    created = vdb.client.data_object.created
    assert len(created) == 1
    first = created[0]
    assert first["class_name"] == "TableDoc"
    assert first["id"] == returned_id


    props = first["props"]
    assert props["table_id"] == returned_id
    expected_text = f"Table cols={list(df.columns)} samples={df.head(3).to_dict()}"
    assert props["text"] == expected_text
