import os, grpc
from dotenv import load_dotenv
import server.audio_service_pb2 as audio_pb2
import server.audio_service_pb2_grpc as audio_pb2_grpc

load_dotenv()

def run():
    target = os.getenv("SERVER_TARGET", "localhost:50051")
    channel = grpc.insecure_channel(target)
    stub = audio_pb2_grpc.AudioServiceStub(channel)
    resp = stub.Synthesize(audio_pb2.SynthesisRequest(text="Hello, gRPC!"))
    with open("output.mp3", "wb") as f:
        f.write(resp.audio)
    print("Сохранено output.mp3")

if __name__ == "__main__":
    run()
