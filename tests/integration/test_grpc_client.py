# tests/integration/test_grpc_client.py

import os

import grpc
import pytest

from tts_grpc_service.grpc import audio_service_pb2, audio_service_pb2_grpc


@pytest.mark.parametrize(
    "text",
    [
        "Hello, gRPC!",
        "Привет, привет!",
        "Bonjour le monde!",
        "Hallo Halli!",
        "Привіт, моє сонечко!",
    ],
)
def test_synthesize_returns_audio_for_various_languages(text):
    port = os.getenv("SERVER_PORT", "50051")
    channel = grpc.insecure_channel(f"localhost:{port}")
    stub = audio_service_pb2_grpc.AudioServiceStub(channel)

    request = audio_service_pb2.SynthesisRequest(text=text)
    response = stub.Synthesize(request)

    # Checking that a byte result has been returned
    assert isinstance(response.audio, bytes)
    assert len(response.audio) > 1000
