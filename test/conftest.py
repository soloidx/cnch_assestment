import pytest
import httpx
from fastapi.testclient import TestClient
from settings import settings, TestTargetEnum
from project.app import app


@pytest.fixture(scope="module")
def app_client():
    client = None
    try:
        if settings.TEST_TARGET == TestTargetEnum.local:
            yield TestClient(app)
        else:
            client = httpx.Client(base_url=settings.REMOTE_ENDPOINT)
            yield client
    finally:
        if settings.TEST_TARGET == TestTargetEnum.remote:
            client.close()
