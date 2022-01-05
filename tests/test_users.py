from jose import jwt

from app import schemas
from app.config import settings

#
# use with: pytest --disable-warnings -v -x
#


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@pytest.de", "password": "password123"}
    )
    new_user = schemas.UserData(**res.json())

    assert new_user.email == "hello123@pytest.de"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload["user_id"]

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
