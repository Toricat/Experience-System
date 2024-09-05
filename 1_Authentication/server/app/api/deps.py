from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone
from typing import Annotated,Optional, Dict

from jose import JWTError, jwt
from core.config import settings
from core.db import SessionLocal
from core.security import ALGORITHM

from schemas.users import User
from schemas.tokens import AccessTokenPayload

from crud.users import crud_user



oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


async def get_session():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2)]

async def get_token_data(token: TokenDep) -> AccessTokenPayload:
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
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403,detail={"message": f"Not enough permissions", "code": 403},)
        return current_user
    return role_checker

async def check_permissions(
    current_user,
    action: str,
    obj_in: Optional[dict] = None,
    owner_field: str = "owner_id",
    id: Optional[int] = None
) -> Dict[str, any]:
    if current_user.role == "admin":
        return {}

    if id and id != current_user.id:
        raise HTTPException(status_code=403, detail={"message": "You are not allowed to perform this action", "code": 403})

    kwargs = {}

    if action == "create":
        if obj_in:
            if obj_in.get(owner_field) and obj_in[owner_field] != current_user.id:
                raise HTTPException(status_code=403, detail={"message": "You are not allowed to perform this action", "code": 403})
    if action in ["get", "get_multi", "update", "delete"]:
        if id is None:
            kwargs[owner_field] = current_user.id

    return kwargs

def handle_service_result(result):
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result