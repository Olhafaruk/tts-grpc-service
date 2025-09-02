#tests/domain/test_question.py

from assistant.domain.question import Question

def test_question_dataclass_stores_text():
    q = Question(text="How are you?")
    assert hasattr(q, "text")
    assert q.text == "How are you?"
