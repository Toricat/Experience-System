from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,)
from .common.utils import handle_error

from datetime import datetime

from core.security import create_access_token, create_refresh_token, create_verify_code, get_password_hash, is_valid_password

from crud.users import crud_user
from crud.tokens import crud_token
from crud.verifies import crud_verify

from schemas.tokens import TokenInDB
from schemas.users import UserInDB, UserCreate,UserUpdateDB
from schemas.verifies import VerifyInDB, VerifyUpdateDB, VerifyInDB
from schemas.authetications import  TokenRefresh,ChangePassword, VerifyCodeComfirm,VerifyCodeSend

class AuthService:

    @handle_error
    async def login_service(self, session, data):
        user = await crud_user.get(session, email=data.username)
        if not user or not is_valid_password(data.password, user.hashed_password):
            return UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            return ForbiddenError("User is inactive")

        existing_token = await crud_token.get(session, user_id=user.id)
        access_token = create_access_token(user)

        if existing_token:
            refresh_token = existing_token.refresh_token
        else:
            refresh_token, expire = create_refresh_token()
            obj_in = TokenInDB(refresh_token=refresh_token, user_id=user.id, exp=expire)
            await crud_token.create(session, obj_in=obj_in)

        return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token}

    @handle_error
    async def register_service(self, session, data: UserCreate):
        hashed_password = get_password_hash(data.password)
        new_user = UserInDB(
            email=data.email, 
            full_name=data.full_name, 
            hashed_password=hashed_password, 
            image=data.image, 
            role="user", 
            account_type="local", 
            is_active=False
        )

        user = await crud_user.create(session, obj_in=new_user)

        verify_code, expire = create_verify_code()
        obj_in = VerifyInDB(verify_code=verify_code, exp=expire, user_id=user.id)
        await crud_verify.create(session, obj_in=obj_in)

        return {"verify_code": verify_code}

    @handle_error
    async def refresh_token_service(self, session, token_data: TokenRefresh):
        result = await crud_token.get(session, refresh_token=token_data.refresh_token)
        if not result or result.exp < datetime.utcnow() or result.user_id != token_data.user_id:
            return UnauthorizedError("Invalid or expired refresh token")

        user = await crud_user.get(session, id=token_data.user_id)
        if not user or not user.is_active:
            return UnauthorizedError("Invalid user or user is inactive")

        access_token = create_access_token(user)
        refresh_token = token_data.refresh_token

        return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token}

    @handle_error
    async def change_password_service(self, session, data: ChangePassword, current_user: UserInDB):
        if not is_valid_password(data.current_password, current_user.hashed_password):
            return UnauthorizedError("Incorrect current password")
        await crud_user.update(session, id=current_user.id, obj_in={"hashed_password": get_password_hash(data.new_password)})

        return {"msg": "Password changed successfully"}

    @handle_error
    async def verify_code_by_email_service(self, session, data: VerifyCodeSend):
        user = await crud_user.get(session, email=data.email)
        if user is None:
            return NotFoundError("User not found")
        verify = await crud_verify.get(session, user_id=user.id)
        if verify is not None and verify.exp > datetime.utcnow():
            return {"verify_code": verify.verify_code}
        

        verify_code, expire = create_verify_code()
        obj_in = VerifyUpdateDB(verify_code=verify_code, exp=expire)

        if verify is not None and verify.exp < datetime.utcnow():
            await crud_verify.update(session, obj_in=obj_in.dict(exclude=None))
        else:
            obj_in = VerifyInDB(verify_code=verify_code, exp=expire, user_id=user.id)
            await crud_verify.create(session, obj_in=obj_in)

        return {"verify_code": verify_code}
        


    @handle_error
    async def confirm_verify_code_service(self, session, data: VerifyCodeComfirm):
        verify = await crud_verify.get(session, verify_code = data.verify_code)
        if verify is not None and verify.exp  > datetime.utcnow():      
            obj_in = UserUpdateDB(is_active=True)
            await crud_user.update(session,  obj_in=obj_in)
            return {"msg": "User Activated"}
        elif verify is not None and verify.exp < datetime.utcnow():  
            return UnauthorizedError("Expired verify code")
        else:
            return UnauthorizedError("Invalid verify code")

       