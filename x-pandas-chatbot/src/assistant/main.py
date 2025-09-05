# src/assistant/main.py

import logging

import uvicorn
from assistant.application.query_service import QueryService
from assistant.application.table_store import TableService
from assistant.interface.grpc.server import serve as serve_grpc
from assistant.interface.http.server import create_app
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,  # Можно заменить на DEBUG, WARNING, ERROR
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class FunctionCall(BaseModel):
    function: str
    arguments: dict


def get_query_service() -> QueryService:
    return QueryService(ts=TableService())


def create_extended_app() -> FastAPI:
    app = create_app()

    @app.post("/execute")
    def execute_function(
        call: FunctionCall, qs: QueryService = Depends(get_query_service)
    ):
        try:
            result = qs._execute(call.function, call.arguments)
            return {"result": result}
        except Exception as e:
            logging.error(f"Function execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


def main_http():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


def main_grpc():
    serve_grpc()


if __name__ == "__main__":
    main_http()
