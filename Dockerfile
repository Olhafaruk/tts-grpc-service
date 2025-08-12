FROM python:3.11-slim


RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY setup.py requirements.txt ./

COPY src/ ./src

RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir -e . \
 && pip install --no-cache-dir grpcio-tools

RUN python -m grpc_tools.protoc \
    -I src/tts_grpc_service/proto \
    --python_out=src/tts_grpc_service/grpc \
    --grpc_python_out=src/tts_grpc_service/grpc \
    src/tts_grpc_service/proto/*.proto

COPY cmd/ ./cmd
COPY .env.example ./.env.example
COPY Makefile ./


EXPOSE 50051
CMD ["python", "-u", "cmd/main.py"]

