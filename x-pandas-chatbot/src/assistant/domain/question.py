#domain/question.py

from dataclasses import dataclass

@dataclass(frozen=True)
class Question:
    text: str
