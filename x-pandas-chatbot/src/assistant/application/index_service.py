# src/assistant/application/index_service.py

import uuid
import pandas as pd
from assistant.infrastructure.weaviate_client import WeaviateClient
from io import BytesIO

class IndexService:
    def __init__(self, vdb=None):
        self.vdb = vdb or WeaviateClient()

    def index_table(self, table_id: str, name: str, df: pd.DataFrame) -> str:

        self.vdb.index_table(table_id, name, df)
        return table_id

    def upload_table(self, filename: str, data: bytes) -> str:

        ext = filename.rsplit(".", 1)[-1].lower()
        buf = BytesIO(data)
        if ext == "csv":
            df = pd.read_csv(buf)
        elif ext in ("xls", "xlsx"):
            df = pd.read_excel(buf)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        table_id = str(uuid.uuid4())
        return self.index_table(table_id, filename, df)
