# src/assistant/application/table_store.py
import uuid
from io import BytesIO
import pandas as pd
from typing import Dict

from assistant.infrastructure.weaviate_client import WeaviateClient

class TableService:
    def __init__(self):
        self._tables: Dict[str, pd.DataFrame] = {}
        self.indexer = WeaviateClient()

    def upload(self, filename: str, data: bytes) -> str:
        """
        1) Читает CSV/XLS/XLSX
        2) Генерирует UUID
        3) Сохраняет в память и индексирует в Weaviate
        """
        ext = filename.rsplit(".", 1)[-1].lower()
        buf = BytesIO(data)

        try:
            if ext == "csv":
                df = pd.read_csv(buf)
            elif ext == "xls":
                df = pd.read_excel(buf, engine="xlrd")
            elif ext == "xlsx":
                df = pd.read_excel(buf, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported file type: {filename}")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла {filename}: {e}")

        table_id = str(uuid.uuid4())
        self._tables[table_id] = df

        # ✅ Индексация в Weaviate
        try:
            self.indexer.index_table(table_id, filename, df)
        except Exception as e:
            raise RuntimeError(f"Ошибка при индексации таблицы {filename}: {e}")

        return table_id

    def get(self, table_id: str) -> pd.DataFrame:
        return self._tables[table_id]

    def list_ids(self) -> list[str]:
        return list(self._tables.keys())
