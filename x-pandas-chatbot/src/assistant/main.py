#src/assistant/main.py

import uvicorn
from assistant.interface.http.server import create_app
from assistant.interface.grpc.server import serve as serve_grpc

def main_http():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

def main_grpc():
    serve_grpc()

if __name__ == "__main__":
    main_http()
