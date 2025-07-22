#client/test_grpc.py
import grpc
from server import audio_service_pb2, audio_service_pb2_grpc

def main():

    channel = grpc.insecure_channel("localhost:50051")
    stub = audio_service_pb2_grpc.AudioServiceStub(channel)


    request = audio_service_pb2.SynthesisRequest(text="Приветствую, Halli Hallo, gRPC!")


    response = stub.Synthesize(request)


    print(f"audio received: {len(response.audio)} byte")


    with open("out.mp3", "wb") as f:
        f.write(response.audio)
    print("Audio saved to file: out.mp3")

if __name__ == "__main__":
    main()
