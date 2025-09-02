# tests/interface/grpc/test_server.py

import pytest
from assistant.interface.grpc import server as grpc_server
from assistant.interface.grpc.assistant_pb2 import AskReq, AskRes

class DummyQueryService:
    def ask(self, tables, question):

        return [{"text": f"echo: {question.text}"}]

@pytest.fixture(autouse=True)
def patch_query_service(monkeypatch):

    monkeypatch.setattr(
        grpc_server,
        "QueryService",
        lambda *args, **kwargs: DummyQueryService()
    )

def test_grpc_ask_returns_stream_of_AskRes():

    servicer = grpc_server.AssistantServicer()


    req = AskReq(table_ids=["ignored"], question="hallo")


    responses = list(servicer.Ask(req, context=None))


    assert len(responses) == 1

    resp = responses[0]
    assert isinstance(resp, AskRes)


    assert resp.text.msg == "echo: hallo"
