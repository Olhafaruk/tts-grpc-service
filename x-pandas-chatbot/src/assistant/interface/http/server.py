#interface/http/server.py

from fastapi import FastAPI, UploadFile, Form
from sse_starlette.sse import EventSourceResponse
from assistant.application.index_service import IndexService
from assistant.application.query_service import QueryService
from assistant.domain.question import Question

def create_app():
    app = FastAPI()
    idx = IndexService()
    qs  = QueryService()

    @app.post("/run")
    async def run(files: list[UploadFile], question: str = Form(...)):
        tables = [idx.upload_table(f.filename, await f.read()) for f in files]
        async def stream():
            for part in qs.ask(tables, Question(question)):
                ev, data = next(iter(part.items()))
                yield {"event": ev, "data": data}
        return EventSourceResponse(stream())

    return app
