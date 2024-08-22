from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,

)
from .common.utils import handle_db_errors
from datetime import datetime
from core.security import create_access_token, create_refresh_token, create_verify_code, get_password_hash, is_valid_password
from crud.users import crud_user
from crud.tokens import crud_token
from crud.verifies import crud_verify
from schemas.tokens import TokenInDB
from schemas.users import UserInDB, UserCreate
from schemas.verifies import VerifyInDB, VerifyUpdateDB
from schemas.authetications import  TokenRefresh,ChangePassword, RecoveryPassword, ComfirmVerifyCode

class AuthService:

    @handle_db_errors
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

    @handle_db_errors
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

        # Thực hiện tạo người dùng, lỗi sẽ được handle_db_errors xử lý nếu có
        user = await crud_user.create(session, obj_in=new_user)

        # Tạo verify code cho người dùng mới
        verify_code, expire = create_verify_code()
        obj_in = VerifyInDB(verify_code=verify_code, exp=expire, user_id=user.id)
        await crud_verify.create(session, obj_in=obj_in)

        return {"verify_code": verify_code}

    @handle_db_errors
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

    @handle_db_errors
    async def change_password_service(self, session, data: ChangePassword, current_user: UserInDB):
        if not is_valid_password(data.current_password, current_user.hashed_password):
            return UnauthorizedError("Incorrect current password")

        current_user.hashed_password = get_password_hash(data.new_password)
        await crud_user.update(session, db_obj=current_user, obj_in={"hashed_password": current_user.hashed_password})

        return {"msg": "Password changed successfully"}

    @handle_db_errors
    async def recovery_by_email_service(self, session, data: RecoveryPassword):
        user = await crud_user.get(session, email=data.email)
        if not user or not user.is_active:
            return UnauthorizedError("Invalid email or user is inactive")

        verify_code, expire = create_verify_code()
        obj_in = VerifyUpdateDB(verify_code=verify_code, exp=expire)
        await crud_verify.update(session, obj_in=obj_in.dict(exclude=None))

        return {"verify_code": verify_code}

    @handle_db_errors
    async def confirm_verify_code_service(self, session, data: ComfirmVerifyCode):
        verify = await crud_verify.get(session, data.verify_code)
        if not verify or verify.exp < datetime.utcnow():
            return UnauthorizedError("Invalid or expired verify code")

        await crud_user.update(session, user_id=verify.user_id, obj_in={"is_active": True})
        return {"msg": "User Activated"}
