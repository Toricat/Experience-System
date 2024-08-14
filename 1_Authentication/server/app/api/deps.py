from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from core.config import settings
from core.db import SessionLocal
from core.security import ALGORITHM
from crud.users import crud_user
from crud.tokens import crud_token
from models.users import User
from schemas.tokens import AccessTokenPayload

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
)


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2)) -> AccessTokenPayload:
    try:
        secret_key = settings.SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        

        if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        token_data = AccessTokenPayload(**payload)
    except JWTError :
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):  
    user = await crud_user.get(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def verify_refresh_token(
    refresh_token: str, session: AsyncSession = Depends(get_session)
) -> User:
    result = await crud_token.get(session, refresh_token=refresh_token)


    if result is None:
        raise HTTPException(
            status_code=401, detail="Invalid refresh token"
        )
    if result.exp < datetime.utcnow():
        raise HTTPException(
            status_code=401, detail="Refresh token has expired"
        )

    user = await session.get(User, result.user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=400, detail="Inactive user"
        )

    return user
        
  
