from tts_grpc_service.config import configure_logging, load_env
from tts_grpc_service.grpc_server import serve
import logging

def main():
    load_env()
    configure_logging()
    logging.getLogger("tts").info("Start gRPC-server")
    serve()

if __name__ == "__main__":
    main()