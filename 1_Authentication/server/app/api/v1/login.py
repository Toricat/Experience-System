from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session, get_current_user, verify_refresh_token
from core.security import authenticate, create_access_token,create_refresh_token, get_password_hash, is_valid_password

from schemas.tokens import Token,TokenLogin,TokenInDB
from schemas.users import User,UserMe
from schemas.authetications import ChangePassword,  TokenRefresh

from crud.users import crud_user
from crud.tokens import crud_token

import time
router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenLogin)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate(session, email=data.username, password=data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(user)
    refresh_token, expire  = create_refresh_token()
    obj_in = TokenInDB(
        refresh_token= refresh_token,
        user_id = user.id,
        exp = expire 
    )
    await crud_token.create(session, obj_in)
    return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh-token",  response_model=TokenLogin)
async def refresh_token(
    token_data: TokenRefresh,
    session: AsyncSession = Depends(get_session),
):
    user = await verify_refresh_token(token_data.refresh_token,session)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    access_token = create_access_token(user)
    refresh_token = token_data.refresh_token

    return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token}
@router.post("/reset-password")
async def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if not is_valid_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password"
        )
    current_user.hashed_password = get_password_hash(data.new_password)
    await crud_user.update(session, db_obj=current_user, obj_in={"hashed_password": current_user.hashed_password})
    return {"msg": "Password changed successfully"}

@router.get("/me", response_model=UserMe)
async def read_users_me(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return current_user