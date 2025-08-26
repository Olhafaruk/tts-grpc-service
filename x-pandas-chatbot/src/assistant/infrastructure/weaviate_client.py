#infrastructure/weaviate_client.py

from weaviate import Client
from assistant.config import WEAVIATE_URL

class WeaviateClient:
    def __init__(self):
        self.client = Client(WEAVIATE_URL)

    def index_table(self, table_id, name, df):
        text = f"{name}: cols={list(df.columns)} samples={df.head(3).to_dict()}"
        self.client.data_object.create(
            {"table_id": table_id, "text": text},
            class_name="TableDoc", uuid=table_id)
    def retrieve_context(self, table_ids):
        texts = [self.client.data_object.get(tid, "TableDoc")["properties"]["text"]
                 for tid in table_ids]
        return "\n".join(texts)
