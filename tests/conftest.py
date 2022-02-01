import pytest

from fastapi.testclient import TestClient
from blog import main

@pytest.fixture(scope='module')
def test_client():
    with TestClient(main.app) as testing_client:
        yield testing_client