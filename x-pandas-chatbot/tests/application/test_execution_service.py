#tests/application/test_execution_service.py

import pytest
import assistant.application.execution_service as exec_mod

class DummyVDB:
    def retrieve_context(self, ids):
        return "CTX"

class DummyQueryService:
    def __init__(self, *args, **kwargs):
        self.vdb = DummyVDB()
    def find_tables(self, question, certainty=0.7):

        return [
            ("tid1", "text1", 0.9),
            ("tid2", "text2", 0.8),
            ("tid3", "text3", 0.7),
        ]

class DummyOpenAIProvider:
    def complete(self, prompt):
        return f"ANSWER: {prompt}"

def test_answer_question_builds_correct_prompt(monkeypatch):

    monkeypatch.setattr(
        exec_mod, "IndexService",
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        exec_mod, "QueryService",
        lambda *args, **kwargs: DummyQueryService()
    )
    monkeypatch.setattr(
        exec_mod, "OpenAIProvider",
        lambda *args, **kwargs: DummyOpenAIProvider()
    )

    svc = exec_mod.ExecutionService()
    answer = svc.answer_question("Hello?")

    expected_prompt = (
        "You have the following tables:\n"
        "CTX\n\n"
        "Question: Hello?\n"
        "Answer:"
    )
    assert answer == f"ANSWER: {expected_prompt}"
