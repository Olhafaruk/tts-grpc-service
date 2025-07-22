import grpc
from server import audio_service_pb2, audio_service_pb2_grpc

def test_synthesize_returns_audio():
    channel = grpc.insecure_channel("localhost:50051")
    stub = audio_service_pb2_grpc.AudioServiceStub(channel)

    request = audio_service_pb2.SynthesisRequest(text="Integration test: everything works?")
    response = stub.Synthesize(request)

    # Проверяем, что вернулся байтовый результат
    assert isinstance(response.audio, bytes)
    assert len(response.audio) > 1000
