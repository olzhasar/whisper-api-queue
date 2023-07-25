from pathlib import Path

import pytest
import responses


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def audio_content():
    return b"test_content"


@pytest.fixture
def audio_filename():
    return "input.mp3"


@pytest.fixture
def test_assets_dir():
    return Path().joinpath("worker", "tests_worker", "assets").absolute()


@pytest.fixture
def sample_audio_path(test_assets_dir: Path):
    return test_assets_dir.joinpath("recognition.mp3")


@pytest.fixture
def sample_audio_bytes(sample_audio_path: Path):
    with open(sample_audio_path, "rb") as f:
        content = f.read()

    return content


@pytest.fixture
def sample_audio_text():
    return "recognition"
