# src/assistant/interface/http/models.py

from typing import List, Optional

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    table_id: Optional[str] = None
    preview_url: Optional[str] = None


class TableUploadResponse(BaseModel):
    table_ids: List[str]
