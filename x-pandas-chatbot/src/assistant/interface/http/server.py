# src/assistant/interface/http/server.py

import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from pydantic import BaseModel
from typing import List


load_dotenv()


project_src = os.environ.get("PYTHONPATH", "/app/src")
if project_src not in sys.path:
    sys.path.insert(0, project_src)


from assistant.application.query_service import QueryService
from assistant.application.table_store import TableService

qs = QueryService()
ts = TableService()


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


def custom_openapi():
    app.openapi_schema = None
    schema = get_openapi(title=app.title, version=app.version, routes=app.routes)


    schema.get("components", {}).get("schemas", {}).pop("Body_upload_upload_post", None)


    post_block = (
        schema.setdefault("paths", {})
              .setdefault("/upload", {})
              .setdefault("post", {})
    )
    post_block["requestBody"] = {
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "format": "binary"
                            },
                            "description": "Выберите один или несколько CSV/XLSX-файлов"
                        }
                    },
                    "required": ["files"]
                },
                "encoding": {
                    "files": {
                        "style": "form",
                        "explode": False
                    }
                }
            }
        }
    }


    return schema




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
    description="Задать вопрос к загруженным таблицам",
)
async def ask(request: AskRequest = Body(...)):
    answer = qs.ask(request.question)
    return AskResponse(answer=answer)

app.openapi = custom_openapi