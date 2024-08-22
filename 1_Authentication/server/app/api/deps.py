from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone
from typing import Annotated

from core.config import settings
from core.db import SessionLocal
from core.security import ALGORITHM

from schemas.users import User

from crud.users import crud_user


from schemas.tokens import AccessTokenPayload

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


async def get_session():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2)]

def get_token_data(token: TokenDep) -> AccessTokenPayload:
    try:
        secret_key = settings.SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    
        if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"},)

        token_data = AccessTokenPayload(**payload)
    except JWTError :
        raise HTTPException(status_code=403, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)
    return token_data


async def get_current_user( 
    session: SessionDep,
    # token: AccessTokenPayload = get_token_data()
    token: AccessTokenPayload = Depends(get_token_data)
):  
    user = await crud_user.get(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_active_user(current_user: CurrentUser):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user",headers={"WWW-Authenticate": "Bearer"},)
    return current_user

CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]

def RoleChecker(allowed_roles: list[str]):
    async def role_checker(
        current_user:  User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
            )
        return current_user
    
    return role_checker

def ownership_check(owner_id, current_user: CurrentActiveUser):
    if current_user.role not in ["admin"] and owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to access this resource"
        )