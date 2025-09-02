# src/assistant/application/execution_service.py
from assistant.application.index_service import IndexService
from assistant.application.query_service import QueryService
from assistant.infrastructure.openai_provider import OpenAIProvider

class ExecutionService:
    def __init__(self):
        self.indexer = IndexService()
        self.searcher = QueryService()
        self.llm = OpenAIProvider()

    def answer_question(self, question: str):

        hits = self.searcher.find_tables(question)


        ids = [hit[0] for hit in hits[:3]]


        context = self.searcher.vdb.retrieve_context(ids)


        prompt = (
            f"You have the following tables:\n{context}\n\n"
            f"Question: {question}\nAnswer:"
        )
        return self.llm.complete(prompt)
