# src/assistant/interface/http/server.py
import json
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse

import time
from typing import List, Optional

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
    table_id: Optional[str] = None
    preview_url: Optional[str] = None


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
    description="Ask your question about tables"
)
async def ask(
    request: AskRequest = Body(
        ...,
        examples={
            "Filter by Country": {
                "summary": "Filter rows where Country is Japan",
                "value": {"question": "Show rows where Country is Japan"}
            },
            "Convert Currency": {
                "summary": "Convert 100 EUR to USD",
                "value": {"question": "Convert 100 EUR to USD using the rate from 2025-01-01"}
            },
            "Compare Rates": {
                "summary": "Compare EUR and GBP",
                "value": {"question": "Compare exchange rates for EUR and GBP on 2025-01-01"}
            }
        }
    )
):
    answer = qs.ask(request.question)

    if isinstance(answer, dict):
        if "reply" in answer:
            return AskResponse(answer=answer["reply"])
        return AskResponse(answer=json.dumps(answer, ensure_ascii=False))

    return AskResponse(answer=answer)

@app.post("/ask/stream")
def ask_stream(
    payload: AskRequest = Body(
        ...,
        examples={
            "Filter by Country": {
                "summary": "Filter rows where Country is Japan",
                "value": {"question": "Show rows where Country is Japan"}
            },
            "Convert Currency": {
                "summary": "Convert 100 EUR to USD",
                "value": {"question": "Convert 100 EUR to USD using the rate from 2025-01-01"}
            }
        }
    )
):

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
                yield f"data: {json.dumps(text, ensure_ascii=False)}\n\n"

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

@app.post("/show_table_html")
def show_table_html(table_id: str = Body(..., embed=True)):
    try:
        df = ts.get_any(table_id)
        html_table = df.to_html(index=False, classes="styled-table")

        html_page = f"""
        <html>
        <head>
            <title>Table Preview</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                h2 {{
                    color: #333;
                }}
                .styled-table {{
                    border-collapse: collapse;
                    margin: 25px 0;
                    font-size: 16px;
                    min-width: 600px;
                    border: 1px solid #ddd;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .styled-table th, .styled-table td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                .styled-table thead tr {{
                    background-color: #009879;
                    color: #ffffff;
                    text-align: left;
                }}
                .styled-table tbody tr:nth-child(even) {{
                    background-color: #f3f3f3;
                }}
            </style>
        </head>
        <body>
            <h2>Table ID: {table_id}</h2>
            {html_table}
        </body>
        </html>
        """
        return HTMLResponse(content=html_page)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Table '{table_id}' not found.")

def create_app():
    return app



app.openapi = lambda: custom_openapi(app)
