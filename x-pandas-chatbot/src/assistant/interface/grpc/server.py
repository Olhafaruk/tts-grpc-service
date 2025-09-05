# interface/grpc/server.py

from concurrent import futures

import grpc
import pandas as pd
from assistant.application.index_service import IndexService
from assistant.application.shared_services import qs
from assistant.domain.question import Question
from assistant.interface.grpc import assistant_pb2, assistant_pb2_grpc


class AssistantServicer(assistant_pb2_grpc.AssistantServicer):
    def __init__(self):
        self.indexer = IndexService()
        self.querier = qs

    def UploadTable(self, request, context):
        table = self.indexer.upload_table(request.name, request.csv)
        return assistant_pb2.UploadTableRes(table_id=table.id)

    def Ask(self, request, context):
        tables = [self.indexer.index_table(pd.DataFrame({"A": [1], "B": [2]}))]

        for part in self.querier.ask(tables, Question(request.question)):
            if "code" in part:
                yield assistant_pb2.AskRes(
                    code=assistant_pb2.Code(content=part["code"])
                )
            elif "log" in part:
                yield assistant_pb2.AskRes(log=assistant_pb2.Log(line=part["log"]))
            else:
                yield assistant_pb2.AskRes(text=assistant_pb2.Text(msg=part["text"]))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    assistant_pb2_grpc.add_AssistantServicer_to_server(AssistantServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
