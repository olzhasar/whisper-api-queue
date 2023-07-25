from unittest.mock import MagicMock

import pytest
from app import ASR_TASK_NAME
from fastapi.testclient import TestClient


@pytest.fixture
def post_data():
    return {
        "file_url": "http://test.com/input.mp3",
        "webhook_url": "http://test.com/webhook",
    }


def test_ok(
    client: TestClient,
    mock_send_task: MagicMock,
    post_data: dict[str, str],
):
    response = client.post("/", json=post_data)

    assert response.status_code == 200, response.text

    mock_send_task.assert_called_once_with(ASR_TASK_NAME, kwargs=post_data)


@pytest.mark.parametrize("field", ["file_url", "webhook_url"])
def test_returns_error_on_invalid_url(
    client: TestClient,
    mock_send_task: MagicMock,
    post_data: dict[str, str],
    field: str,
):
    post_data[field] = "invalid"

    response = client.post("/", json=post_data)

    assert response.status_code == 422
    mock_send_task.assert_not_called()


@pytest.mark.parametrize("field", ["file_url", "webhook_url"])
def test_returns_error_on_missing_field(
    client: TestClient,
    mock_send_task: MagicMock,
    post_data: dict[str, str],
    field: str,
):
    del post_data[field]

    response = client.post("/", json=post_data)

    assert response.status_code == 422
    mock_send_task.assert_not_called()
