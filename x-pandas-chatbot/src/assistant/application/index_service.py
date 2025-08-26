#index_service.py

import uuid
from assistant.domain.table import Table
from assistant.infrastructure.weaviate_client import WeaviateClient

class IndexService:
    def __init__(self, vdb=None):
        self.vdb = vdb or WeaviateClient()

    def upload_table(self, name: str, csv_bytes: bytes) -> Table:
        table_id = str(uuid.uuid4())
        import io, pandas as pd
        df = pd.read_csv(io.BytesIO(csv_bytes))
        self.vdb.index_table(table_id, name, df)
        return Table(table_id, name, df)
