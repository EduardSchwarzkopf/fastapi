from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_passwort}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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
