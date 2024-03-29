from fastapi.testclient import TestClient
from blog.main import app

client = TestClient(app)


def test_main_default_url_not_accesible():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "this works!"
