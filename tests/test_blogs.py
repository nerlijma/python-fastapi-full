from starlette.testclient import TestClient
from requests import Response


def test_get_blogs(test_client: TestClient):
    response: Response = test_client.get('/blog')

    assert response.status_code == 200
