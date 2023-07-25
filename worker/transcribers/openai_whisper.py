import io

import numpy as np
from numpy.typing import NDArray
from pydub import AudioSegment
from transcribers.base import Transcriber

import whisper


class WhisperTranscriber(Transcriber):
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def _convert_audio_to_numpy(
        self, content: bytes, format: str = "mp3"
    ) -> NDArray[np.float32]:
        buffer = io.BytesIO(content)
        segment = AudioSegment.from_file(buffer, format=format)

        if segment.frame_rate != 16_000:
            segment = segment.set_frame_rate(16_000)

        if segment.sample_width != 2:
            segment = segment.set_sample_width(2)

        if segment.channels != 1:
            segment = segment.set_channels(1)

        return np.array(segment.get_array_of_samples()).astype(np.float32) / 32768.0

    def run(self, filename: str, content: bytes) -> dict[str, str]:
        arr = self._convert_audio_to_numpy(content)

        return self.model.transcribe(arr, language="en")
