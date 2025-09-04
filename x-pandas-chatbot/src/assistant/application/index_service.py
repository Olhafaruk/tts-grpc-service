# src/assistant/application/index_service.py

import uuid
import pandas as pd
import logging
from assistant.infrastructure.weaviate_client import WeaviateClient
from io import BytesIO


logger = logging.getLogger(__name__)


class IndexService:
    def __init__(self, vdb=None):
        self.vdb = vdb or WeaviateClient()

    def index_table(self, table_id: str, name: str, df: pd.DataFrame) -> str:
        self.vdb.index_table(table_id, name, df)
        logger.info(f"Table indexed successfully: id={table_id}, name='{name}', columns={list(df.columns)}")
        return table_id

    def upload_table(self, filename: str, data: bytes) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        buf = BytesIO(data)

        try:
            if ext == "csv":
                df = pd.read_csv(buf)
            elif ext in ("xls", "xlsx"):
                df = pd.read_excel(buf)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            raise ValueError(f"Failed to read file '{filename}': {e}")

        table_id = str(uuid.uuid4())
        return self.index_table(table_id, filename, df)

