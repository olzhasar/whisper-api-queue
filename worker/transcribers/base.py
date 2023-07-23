import abc


class Transcriber(abc.ABC):
    @abc.abstractmethod
    def run(self, filename: str, content: bytes) -> dict[str, str]:
        pass
