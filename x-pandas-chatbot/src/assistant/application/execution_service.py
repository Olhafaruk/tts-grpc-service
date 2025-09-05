# src/assistant/application/execution_service.py

import logging

from assistant.application.index_service import IndexService
from assistant.application.query_service import QueryService
from assistant.infrastructure.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class ExecutionService:
    def __init__(self):
        self.indexer = IndexService()
        self.searcher = QueryService()
        self.llm = OpenAIProvider()

    def answer_question(self, question: str):
        hits = self.searcher.find_tables(question)
        ids = [hit[0] for hit in hits[:3]]

        if not ids:
            logger.warning(f"No relevant tables found for question: '{question}'")
            return "No relevant tables found to answer the question."

        context = self.searcher.vdb.retrieve_context(ids)
        logger.info(f"Question received: '{question}', tables used: {ids}")

        prompt = (
            f"You have the following tables:\n{context}\n\n"
            f"Question: {question}\nAnswer:"
        )
        return self.llm.complete(prompt)
