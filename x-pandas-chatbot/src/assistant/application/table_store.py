# src/assistant/application/table_store.py
import uuid
from io import BytesIO
import pandas as pd
from typing import Dict

from assistant.infrastructure.weaviate_client import WeaviateClient
import logging

logger = logging.getLogger(__name__)


class TableService:
    def __init__(self):
        self._tables: Dict[str, pd.DataFrame] = {}
        self._filenames: Dict[str, str] = {}  # filename → table_id
        self.indexer = WeaviateClient()

    def upload(self, filename: str, data: bytes) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        buf = BytesIO(data)

        try:
            if ext == "csv":
                df = pd.read_csv(buf)
            elif ext == "xls":
                df = pd.read_excel(buf)
            elif ext == "xlsx":
                df = pd.read_excel(buf, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported file type: {filename}")
        except Exception as e:
            raise ValueError(f"Error reading file {filename}: {e}")

        if filename in self._filenames:
            logger.warning(f"File '{filename}' already exists. Overwriting previous table with new data.")

            old_id = self._filenames[filename]
            self._tables.pop(old_id, None)

        table_id = str(uuid.uuid4())
        self._tables[table_id] = df
        self._filenames[filename] = table_id
        logger.info(f"Saving table: {filename} → {table_id}")
        logger.info(f"Current table store: {list(self._tables.keys())}")

        try:
            self.indexer.index_table(table_id, filename, df)
        except Exception as e:
            raise RuntimeError(f"Error indexing table {filename}: {e}")

        logger.info(f"Uploaded table '{filename}' with ID {table_id}")
        return table_id


    def get(self, table_id: str) -> pd.DataFrame:
        return self._tables[table_id]

    def get_any(self, ref: str) -> pd.DataFrame:
        logger.info(f"get_any called with ref: {ref}")
        logger.info(f"Available table_ids: {list(self._tables.keys())}")
        logger.info(f"Available filenames: {list(self._filenames.keys())}")

        if ref in self._tables:
            return self._tables[ref]
        if ref in self._filenames:
            return self.get_by_filename(ref)
        raise KeyError(f"No table found for reference: {ref}")

    def get_by_filename(self, filename: str) -> pd.DataFrame:
        table_id = self._filenames.get(filename)
        if not table_id:
            raise KeyError(f"No table found for filename: {filename}")
        return self._tables[table_id]

    def list_ids(self) -> list[str]:
        return list(self._tables.keys())

    def get_latest_id(self) -> str:
        if not self._tables:
            raise KeyError("No tables available")
        return list(self._tables.keys())[-1]

    @property
    def tables(self) -> Dict[str, pd.DataFrame]:
        return self._tables
