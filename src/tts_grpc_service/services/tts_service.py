# src/tts-grpc_service/services/tts_service.py
from tts_grpc_service.domain.tts import (
    SpeechSynthesizer,
    SynthesisRequest,
    SynthesisResponse,
)


class TTSService:
    def __init__(self, synthesizer: SpeechSynthesizer):
        self.synthesizer = synthesizer

    def synthesize(self, req: SynthesisRequest) -> SynthesisResponse:
        audio = self.synthesizer.synthesize(req.text)
        return SynthesisResponse(audio_bytes=audio)
