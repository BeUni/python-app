from passlib.context import CryptContext
from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = 'c1ddcd25f7d432e5ed7672829fa6dc4bd9d8ae0cb8ea914536d7a0a8c8c097c0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 8


def hash_pass(password):
    return pwd_context.hash(password)


def verify_pass(password, hash_password):
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
    to_encode.update({"expire": str(expire)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # expire: str = payload.get("expire")
        print(payload)
        # print(datetime.time(expire))
        # print(datetime.now(datetime))
        # if datetime.ctime(expire) > datetime.now(datetime.UTC):
        #     raise HTTPException(
        #         status_code=401,
        #         detail="Unauthorized"
        #     )
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

