import pytest
from transcribers.openai_whisper import WhisperTranscriber


@pytest.fixture(scope="module")
def transcriber():
    return WhisperTranscriber(model_name="tiny")


def test_run(
    sample_audio_bytes: bytes, sample_audio_text: str, transcriber: WhisperTranscriber
):
    result = transcriber.run("recognition.mp3", sample_audio_bytes)

    assert result["text"].strip().removesuffix(".").lower() == sample_audio_text
