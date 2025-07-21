FROM python:3.11-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir grpcio-tools grpcio


COPY . .


#RUN python -m grpc_tools.protoc \
 #   -I . \
  #  --python_out . \
   # --grpc_python_out . \
    #server/proto/audio_service.proto



CMD ["python", "-u", "-m", "server.server"]
EXPOSE 50051
