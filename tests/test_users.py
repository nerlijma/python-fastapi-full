from fastapi.testclient import TestClient
from blog.main import app
from fastapi import status

client = TestClient(app)

# @pytest.fixture(scope="function")
# def client() -> TestClient:
#     "Starts the client"
#     return TestClient(app)


def get_access_token(user: str, password: str) -> str:
    user = {"username": user, "password": password}
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.post("/token", data=user, headers=header)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_user_not_authorized():
    user = {"username": "n", "password": "n"}
    response = client.post("/token", data=user)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_token():
    auth_header = get_access_token("nico", "nico")
    response = client.get("/user/1", headers=auth_header)
    assert response.status_code == 200
