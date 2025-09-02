#src/assistant/infrastructure/weaviate_client.py

from weaviate import Client
from assistant.config import WEAVIATE_URL
from weaviate.exceptions import UnexpectedStatusCodeException

TABLE_CLASS = {
    "class": "TableDoc",
    "vectorizer": "text2vec-transformers",
    "properties": [
        {"name": "table_id", "dataType": ["string"]},
        {"name": "text", "dataType": ["text"]},
    ],
}

class WeaviateClient:
    def __init__(self, vdb=None):
        self.client = Client(
            url=WEAVIATE_URL,
            startup_period=30
        )
        self._ensure_schema()

    def _ensure_schema(self):

        schema = self.client.schema.get()
        existing = {c["class"] for c in schema.get("classes", [])}


        if TABLE_CLASS["class"] not in existing:
            try:
                self.client.schema.create_class(TABLE_CLASS)
                print("✅ Schema TableDoc created")
            except UnexpectedStatusCodeException as e:

                if "already exists" in str(e):
                    print("⚠️ Schema TableDoc already existed, skipping")
                else:

                    raise

    def index_table(self, table_id, name, df):
        text = f"{name}: cols={list(df.columns)} samples={df.head(3).to_dict()}"
        self.client.data_object.create(
            {"table_id": table_id, "text": text},
            class_name="TableDoc",
            uuid=table_id
        )

    def retrieve_context(self, ids: list[str]) -> str:

        result = []
        for tid in ids:
            obj = self.client.data_object.get(tid, "TableDoc")
            txt = obj["properties"]["text"]
            result.append(txt)

        return "\n\n".join(result)
