from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session, get_current_user
from core.security import authenticate, create_access_token,create_refresh_token, get_password_hash, is_valid_password
from schemas.token import Token
from schemas.users import User
from crud.users import crud_user

router = APIRouter(tags=["Login"])

@router.post("/login", response_model=Token)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate(session, email=data.username, password=data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {"token_type": "bearer", "access_token": create_access_token(user), "refresh_token": create_refresh_token()}

@router.post("/change-password/")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if not is_valid_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password"
        )
    current_user.hashed_password = get_password_hash(new_password)
    await crud_user.update(session, db_obj=current_user, obj_in={"hashed_password": current_user.hashed_password})
    return {"msg": "Password changed successfully"}