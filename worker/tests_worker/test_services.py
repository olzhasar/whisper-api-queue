import pytest
import services
from exceptions import RetriableNetworkError
from requests import ConnectionError, HTTPError, Timeout
from responses import RequestsMock, matchers


@pytest.fixture
def download_url(audio_filename: str):
    return f"http://test.com/{audio_filename}?foo=bar"


def test_download_audio(
    mocked_responses: RequestsMock,
    download_url: str,
    audio_filename: str,
    audio_content: bytes,
):
    mocked_responses.get(download_url, body=audio_content)

    assert services.download_audio(download_url) == (audio_filename, audio_content)


@pytest.mark.parametrize("exc", (ConnectionError, Timeout))
def test_download_audio_raises_retriable_error_for_errors(
    mocked_responses: RequestsMock,
    download_url: str,
    audio_filename: str,
    audio_content: bytes,
    exc: type[Exception],
):
    mocked_responses.get(download_url, body=exc("Error"))

    with pytest.raises(RetriableNetworkError):
        services.download_audio(download_url)


@pytest.mark.parametrize("status", (429, *range(500, 505)))
def test_download_audio_raises_retriable_error_for_statuses(
    mocked_responses: RequestsMock,
    download_url: str,
    audio_filename: str,
    audio_content: bytes,
    status: int,
):
    mocked_responses.get(download_url, status=status)

    with pytest.raises(RetriableNetworkError):
        services.download_audio(download_url)


@pytest.mark.parametrize("status", range(400, 405))
def test_download_audio_does_not_raise_retriable_error_for_other_statuses(
    mocked_responses: RequestsMock,
    download_url: str,
    audio_filename: str,
    audio_content: bytes,
    status: int,
):
    mocked_responses.get(download_url, status=status)

    with pytest.raises(HTTPError):
        services.download_audio(download_url)


@pytest.fixture
def webhook_url():
    return "http://test.com/webhook"


@pytest.fixture
def transcription_result():
    return {"result": "lorem ipsum"}


def test_send_result_to_webhook(
    mocked_responses: RequestsMock,
    webhook_url: str,
    transcription_result: dict[str, str],
):
    mocked_responses.post(
        webhook_url,
        match=[
            matchers.json_params_matcher(transcription_result),
        ],
    )

    services.send_result_to_webhook(transcription_result, webhook_url)


@pytest.mark.parametrize("exc", (ConnectionError, Timeout))
def test_send_result_to_webhook_raises_retriable_error_for_errors(
    mocked_responses: RequestsMock,
    webhook_url: str,
    transcription_result: dict[str, str],
    exc: type[Exception],
):
    mocked_responses.post(webhook_url, body=exc("Error"))

    with pytest.raises(RetriableNetworkError):
        services.send_result_to_webhook(transcription_result, webhook_url)


@pytest.mark.parametrize("status", (429, *range(500, 505)))
def test_send_result_to_webhook_raises_retriable_error_for_statuses(
    mocked_responses: RequestsMock,
    webhook_url: str,
    transcription_result: dict[str, str],
    status: int,
):
    mocked_responses.post(webhook_url, status=status)

    with pytest.raises(RetriableNetworkError):
        services.send_result_to_webhook(transcription_result, webhook_url)


@pytest.mark.parametrize("status", range(400, 405))
def test_send_result_to_webhook_does_not_raise_retriable_error_for_other_statuses(
    mocked_responses: RequestsMock,
    webhook_url: str,
    transcription_result: dict[str, str],
    status: int,
):
    mocked_responses.post(webhook_url, status=status)

    with pytest.raises(HTTPError):
        services.send_result_to_webhook(transcription_result, webhook_url)
