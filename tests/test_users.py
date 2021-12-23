from fastapi.testclient import TestClient
from app.main import app

# use with: pytest --disable-warnings -v -x

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.json().get("message") == "Hello, new stuff"
    assert response.status_code == 200
