from worker.transcribers.base import Transcriber


class WhisperTranscriber(Transcriber):
    def run(filename: str, content: bytes) -> dict[str, str]:
        pass
