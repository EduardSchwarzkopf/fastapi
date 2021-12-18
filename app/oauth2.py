from jose import JWTError, jwt
from datetime import datetime, timedelta

# openssl rand -hex 32
SECRET_KEY = "773140f78db1a62f5fa00f640aab2a7fa9959b2b0959a0a9874ef744f36a73c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token
