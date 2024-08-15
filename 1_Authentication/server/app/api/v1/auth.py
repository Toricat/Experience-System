from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import CurrentUser, SessionDep , verify_refresh_token
from core.security import authenticate, create_access_token,create_refresh_token, create_verify_code, get_password_hash, is_valid_password

from schemas.tokens import TokenLogin,TokenInDB
from schemas.verifies import  VerifyCode
from schemas.users import UserMe, UserCreate
from schemas.authetications import ChangePassword, TokenRefresh, RecoveryPassword

from crud.users import crud_user
from crud.tokens import crud_token
from crud.verifies import crud_verify


router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenLogin)
async def login(session: SessionDep ,data: OAuth2PasswordRequestForm = Depends()):
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

@router.post("/register", response_model=VerifyCode)
async def register(session: SessionDep, data: UserCreate):
    user = await crud_user.get(session, email=data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(data.password)
    new_user = UserCreate(email=data.email, full_name=data.full_name, hashed_password=hashed_password, image=data.image,role="user") 
    user = await crud_user.create(session, obj_in=new_user)

    verify_code = create_verify_code()
    return {"verify_code": verify_code}


@router.post("/refresh-token",  response_model=TokenLogin)
async def refresh_token(
    token_data: TokenRefresh,
    session:  SessionDep ,
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
    current_user: CurrentUser,
    session:  SessionDep 
):
    if not is_valid_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password"
        )
    current_user.hashed_password = get_password_hash(data.new_password)
    await crud_user.update(session, db_obj=current_user, obj_in={"hashed_password": current_user.hashed_password})
    return {"msg": "Password changed successfully"}

@router.post("/recovery",response_model= VerifyCode)
async def recovery_password(
    data: RecoveryPassword,
    session:  SessionDep 
):
    user = await crud_user.get(session, email=data.email)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    if user.email == data.email:
        verify_code,expire  = create_verify_code()
        await crud_verify.create(session, obj_in=data.dict(),expire=expire)
    
    return {"verify_code" : verify_code}


@router.get("/me", response_model=UserMe)
async def read_users_me(current_user: CurrentUser, session:  SessionDep ):
    return current_user