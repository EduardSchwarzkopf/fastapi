from fastapi.testclient import TestClient
from app.main import app
from app import schemas

# use with: pytest --disable-warnings -v -x

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.json().get("message") == "Hello, new stuff"
    assert response.status_code == 200


def test_create_user():
    res = client.post(
        "/users/", json={"email": "hello123@pytest.de", "password": "password123"}
    )
    new_user = schemas.UserData(**res.json())

    assert new_user.email == "hello123@pytest.de"
    assert res.status_code == 201
