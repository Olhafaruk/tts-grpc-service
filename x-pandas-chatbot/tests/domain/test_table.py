# tests/domain/test_table.py

from assistant.domain.table import TableDoc


def test_tabledoc_dataclass_fields():
    tid = "abcd-1234"
    desc = "Table contents"
    t = TableDoc(table_id=tid, text=desc)

    assert hasattr(t, "table_id")
    assert hasattr(t, "text")

    assert t.table_id == tid
    assert t.text == desc
