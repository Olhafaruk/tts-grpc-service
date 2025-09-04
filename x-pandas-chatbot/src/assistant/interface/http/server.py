# src/assistant/interface/http/server.py
import json
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import time
from typing import List

from pydantic import BaseModel

from assistant.interface.http.openapi_config import custom_openapi
from assistant.application.shared_services import ts, qs


load_dotenv()


project_src = os.environ.get("PYTHONPATH", "/app/src")
if project_src not in sys.path:
    sys.path.insert(0, project_src)


app = FastAPI(
    title="x-pandas-chatbot",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TableUploadResponse(BaseModel):
    table_ids: List[str]

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str




@app.post("/upload", response_model=TableUploadResponse)
async def upload(files: List[UploadFile] = File(...)):
    table_ids = []
    for file in files:
        data = await file.read()
        table_id = ts.upload(file.filename, data)
        table_ids.append(table_id)
    return TableUploadResponse(table_ids=table_ids)



@app.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask Endpoint",
    description="Ask your question about tables",
)
async def ask(request: AskRequest = Body(...)):
    answer = qs.ask(request.question)

    if isinstance(answer, dict):
        if "reply" in answer:
            return AskResponse(answer=answer["reply"])
        return AskResponse(answer=json.dumps(answer, ensure_ascii=False))

    return AskResponse(answer=answer)


@app.post("/ask/stream")
def ask_stream(payload: AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in request")

    def stream():
        try:
            result = qs.ask(question)
            text = result.get("reply") or result.get("result")
            if not text:
                yield f"data: [ERROR] No reply or result found\n\n"
                return
            if isinstance(text, dict):
                text = json.dumps(text)
            for token in str(text).split():
                yield f"data: {token}\n\n"
                time.sleep(0.05)
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    # Example: return number of indexed tables (stubbed)
    return {"tables_indexed": len(ts.tables)}

def create_app():
    return app



app.openapi = lambda: custom_openapi(app)
