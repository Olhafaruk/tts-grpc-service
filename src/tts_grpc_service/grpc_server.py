# src/tts_grpc_service/grpc_server.py

from concurrent import futures

import grpc

from tts_grpc_service.config import configure_logging, load_env
from tts_grpc_service.domain.tts import SynthesisRequest
from tts_grpc_service.grpc import audio_service_pb2 as audio_pb2
from tts_grpc_service.grpc import audio_service_pb2_grpc as audio_pb2_grpc
from tts_grpc_service.repository.gtts_provider import GTTSProvider
from tts_grpc_service.services.tts_service import TTSService

load_env()
configure_logging()


class AudioServiceServicer(audio_pb2_grpc.AudioServiceServicer):
    def __init__(self, tts_service: TTSService):
        self.tts = tts_service

    def Synthesize(self, request, context):
        text = request.text.strip()
        if not text:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Text must not be empty")
            return audio_pb2.SynthesisResponse()
        dom_req = SynthesisRequest(text=text)
        dom_res = self.tts.synthesize(dom_req)
        return audio_pb2.SynthesisResponse(audio=dom_res.audio_bytes)


def serve():
    provider = GTTSProvider()
    service = TTSService(provider)
    servicer = AudioServiceServicer(service)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_AudioServiceServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    configure_logging()
    serve()
