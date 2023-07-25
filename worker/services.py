from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import requests
from exceptions import RetriableNetworkError


def download_audio(url: str) -> tuple[str, bytes]:
    response = _request_with_retriable_error("get", url)

    filename = _parse_filename_from_url(url)

    return filename, response.content


def send_result_to_webhook(result: dict[str, str], url: str) -> None:
    _request_with_retriable_error(method="post", url=url, json=result)


def _parse_filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    return Path(unquote(parsed.path)).name


def _request_with_retriable_error(
    method: str, url: str, **kwargs: Any
) -> requests.Response:
    try:
        response = requests.request(method=method, url=url, **kwargs)
    except requests.RequestException as exc:
        raise RetriableNetworkError(str(exc))

    if not response.ok:
        if response.status_code == 429 or response.status_code >= 500:
            raise RetriableNetworkError(
                f"Invalid status {response.status_code} received"
            )
        response.raise_for_status()

    return response
