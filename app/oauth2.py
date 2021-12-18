from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# openssl rand -hex 32
SECRET_KEY = "773140f78db1a62f5fa00f640aab2a7fa9959b2b0959a0a9874ef744f36a73c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return access_token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "No valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
