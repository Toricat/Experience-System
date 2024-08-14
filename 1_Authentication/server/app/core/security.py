from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.users import crud_user
from crud.tokens import crud_token
from models.users import User

import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM=settings.ALGORITHM

def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"exp": expire, 
         "user_id": str(user.id),
        },
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

def create_refresh_token() -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token =str(uuid.uuid4()) 

    return refresh_token, expire 


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(
    session: AsyncSession, email: EmailStr, password: str
) -> Optional[User]:
    user = await crud_user.get(session, email=email)
    if user is not None and is_valid_password(password, user.hashed_password):
        return user
    return None