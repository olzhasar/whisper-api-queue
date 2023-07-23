from transcribers.base import Transcriber


class WhisperTranscriber(Transcriber):
    def run(self, filename: str, content: bytes) -> dict[str, str]:
        return {}
