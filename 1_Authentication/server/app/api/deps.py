from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import SessionLocal
from core.security import ALGORITHM
from crud.users import crud_user
from models.users import User
from schemas.token import TokenPayload

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
    scopes={
        "user": "Basic user with limited access",
        "manager": "Manager with elevated permissions",
        "admin": "Admin with full access",
    },
)


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(security_scopes: SecurityScopes,token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        print(payload)
        token_data = TokenPayload(payload.get("user_id"), payload.get("scopes", []))
       
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):  
    user = await crud_user.get(session, id=token.user_id)
    print(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

