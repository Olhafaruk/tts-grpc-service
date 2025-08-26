#domain/table.py

from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class Table:
    id: str
    name: str
    df: pd.DataFrame
