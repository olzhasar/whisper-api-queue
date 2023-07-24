from unittest import mock
from unittest.mock import MagicMock

import pytest
from celery.exceptions import Retry
from exceptions import RetriableNetworkError
from pytest_mock import MockerFixture
from tasks import run_asr, send_asr_result
from transcribers.base import Transcriber


class StubTranscriber(Transcriber):
    _calls: list[tuple[str, bytes]]

    def __init__(self):
        self._calls = []

    def run(self, filename: str, content: bytes) -> dict[str, str]:
        self._calls.append((filename, content))

        return {"text": "test result"}


@pytest.fixture
def audio_content():
    return b"test_content"


@pytest.fixture
def audio_filename():
    return "input.mp3"


@pytest.fixture
def transcriber():
    return StubTranscriber()


@pytest.fixture(autouse=True)
def _patch_transcriber(mocker: MockerFixture, transcriber: StubTranscriber):
    # TODO: this should be specified in a dedicated test settings module instead
    mocker.patch("tasks.transcriber", transcriber)


@pytest.fixture
def mock_download_audio(
    mocker: MockerFixture, audio_content: bytes, audio_filename: str
):
    mock = mocker.patch("tasks.download_audio", autospec=True)
    mock.return_value = audio_filename, audio_content
    return mock


@mock.patch("tasks.send_asr_result", autospec=True)
def test_run_asr(
    mock_send_asr_result: MagicMock,
    mock_download_audio: MagicMock,
    audio_filename: str,
    audio_content: bytes,
    transcriber: StubTranscriber,
):
    file_url = "http://test.com/img.jpg"
    webhook_url = "http://test.com/webhook"

    run_asr(file_url, webhook_url)

    assert transcriber._calls == [(audio_filename, audio_content)]

    mock_send_asr_result.delay.assert_called_once_with(
        result={"text": "test result"}, url=webhook_url
    )


@mock.patch("tasks.run_asr.retry", side_effect=Retry)
def test_run_asr_retries_on_retriable_error(
    mock_retry: MagicMock,
    mock_download_audio: MagicMock,
):
    mock_download_audio.side_effect = RetriableNetworkError

    file_url = "http://test.com/img.jpg"
    webhook_url = "http://test.com/webhook"

    with pytest.raises(Retry):
        run_asr(file_url, webhook_url)


@mock.patch("tasks.run_asr.retry", side_effect=Retry)
def test_run_asr_does_not_retry_on_other_errors(
    mock_retry: MagicMock,
    mock_download_audio: MagicMock,
):
    mock_download_audio.side_effect = RuntimeError

    file_url = "http://test.com/img.jpg"
    webhook_url = "http://test.com/webhook"

    with pytest.raises(RuntimeError):
        run_asr(file_url, webhook_url)


@pytest.fixture
def mock_send_result_to_webhook(mocker: MockerFixture):
    return mocker.patch("tasks.send_result_to_webhook", autospec=True)


def test_send_asr_results(mock_send_result_to_webhook: MagicMock):
    result = {"foo": "bar"}
    url = "http://test.com/webhook"

    send_asr_result(result, url)

    mock_send_result_to_webhook.assert_called_once_with(result, url)


@mock.patch("tasks.send_asr_result.retry", side_effect=Retry)
def test_send_asr_results_retries_on_retriable_error(
    mock_retry: MagicMock,
    mock_send_result_to_webhook: MagicMock,
):
    mock_send_result_to_webhook.side_effect = RetriableNetworkError

    result = {"foo": "bar"}
    url = "http://test.com/webhook"

    with pytest.raises(Retry):
        send_asr_result(result, url)


@mock.patch("tasks.send_asr_result.retry", side_effect=Retry)
def test_send_asr_results_does_not_retry_on_other_errors(
    mock_retry: MagicMock,
    mock_send_result_to_webhook: MagicMock,
):
    mock_send_result_to_webhook.side_effect = RuntimeError

    result = {"foo": "bar"}
    url = "http://test.com/webhook"

    with pytest.raises(RuntimeError):
        send_asr_result(result, url)
