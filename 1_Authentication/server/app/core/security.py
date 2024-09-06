from datetime import datetime, timedelta


from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models.user import User

import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM=settings.ALGORITHM

def create_access_token(user: User) -> str:
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"exp": expire, 
         "user_id": str(user.id),
        },
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
def create_refresh_token() -> str:
    expire = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token =str(uuid.uuid4()) 
    return refresh_token, expire 

def create_verify_code() -> str:
    expire = datetime.now() + timedelta(minutes=settings.VERIFY_CODE_EXPIRE_MINUTES)
    verify_code =str(uuid.uuid4()) 
    return verify_code, expire 
def create_state() -> str:
    state =str(uuid.uuid4()) 
    return state


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)




