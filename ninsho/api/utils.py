from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from ninsho.config import config

pwd_context = CryptContext(schemes=["sha256_crypt"])

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm="HS256")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=["HS256"])
        return payload
    except JWTError as e:
        print(e)
        return None


