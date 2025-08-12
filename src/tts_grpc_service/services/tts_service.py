from tts_grpc_service.domain.tts import SynthesisRequest, SynthesisResponse
from tts_grpc_service.repository.gtts_provider import GTTSProvider


class TTSService:
    def __init__(self, provider=None):
        self.provider = provider or GTTSProvider()

    def synthesize(self, req: SynthesisRequest) -> SynthesisResponse:
        audio = self.provider.synthesize(req.text)
        return SynthesisResponse(audio_bytes=audio)
