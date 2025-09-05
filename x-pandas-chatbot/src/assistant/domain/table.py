# src/assistant/domain/table.py
from dataclasses import dataclass


@dataclass
class TableDoc:
    table_id: str
    text: str
