import pytest
from app import app
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture
def mock_send_task(mocker: MockerFixture):
    return mocker.patch("app.celery_app.send_task", autospec=True)
