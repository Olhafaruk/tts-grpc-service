# Dockerfile

FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest pytest-cov pytest-asyncio


COPY src     ./src
COPY proto   ./proto
COPY tests   ./tests

#RUN touch src/assistant/interface/grpc/__init__.py


RUN python -m grpc_tools.protoc \
    --proto_path=./proto \
    --python_out=src/assistant/interface/grpc \
    --grpc_python_out=src/assistant/interface/grpc \
    proto/assistant.proto



ENV PYTHONPATH=/app/src

EXPOSE 50051 8000


CMD ["uvicorn", "assistant.interface.http.server:app", "--host", "0.0.0.0", "--port", "8000"]
