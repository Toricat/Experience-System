from datetime import datetime
from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
    SuccessResponse,
    BadRequestError,
    AttributeError,
    )
from .common.handle import handle_error
from .common.utils import send_email,render_email_template

from core.security import create_access_token, create_refresh_token, create_verify_code, get_password_hash, is_valid_password

from crud.users import crud_user
from crud.tokens import crud_token
from crud.verifies import crud_verify

from schemas.tokens import TokenInDB,TokenLogin
from schemas.users import UserInDB, UserCreate,UserBase, UserActivate
from schemas.verifies import ActivateCodeInDB
from schemas.authetications import  TokenRefresh,ChangePassword, VerifyCodeComfirm,VerifyEmailSend,VerifyCodeChangePassword, Login 


class AuthService:
    def __init__(self, session):
        self.session = session

    @handle_error
    async def login_service(self,data: Login):
        user = await crud_user.get(self.session, email=data.username)
        if not user or not is_valid_password(data.password, user.hashed_password):
            return UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            return ForbiddenError("User is inactive")

        existing_token = await crud_token.get(self.session,user_id=user.id)
        access_token = create_access_token(user)

        if existing_token and existing_token.exp > datetime.utcnow():
            refresh_token = existing_token.refresh_token
        else:
            refresh_token, expire = create_refresh_token()
            obj_in = TokenInDB(refresh_token=refresh_token, user_id=user.id, exp=expire)
            await crud_token.create(self.session, obj_in=obj_in)

        return TokenLogin( token_type="bearer", refresh_token=refresh_token, access_token=access_token)    
    @handle_error
    async def register_service(self,  data: UserCreate):
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
        user = await crud_user.create(self.session, obj_in=new_user)
        code_active, exp_active = create_verify_code()
        obj_in = ActivateCodeInDB(code_active=code_active,exp_active=exp_active, user_id=user.id)
        await crud_verify.create(self.session, obj_in=obj_in)
        html_content = await render_email_template( "register_code.html",verification_code=code_active)
        response = await send_email(
            email_to=data.email,
            subject="Your Verification Code",
            html_content=html_content)
        if not response:
            return BadRequestError("Failed to send email")
        return SuccessResponse("Successfully registered. Please check your email to verify your account.")
            

    @handle_error
    async def refresh_token_service(self,  token_data: TokenRefresh):
        result = await crud_token.get(self.session, refresh_token=token_data.refresh_token)
        if not result or result.exp < datetime.utcnow() or result.user_id != token_data.user_id:
            return UnauthorizedError("Invalid or expired refresh token")

        user = await crud_user.get(self.session, id=token_data.user_id)
        if not user or not user.is_active:
            return UnauthorizedError("Invalid user or user is inactive")

        access_token = create_access_token(user)
        refresh_token = token_data.refresh_token

        return TokenLogin( token_type="bearer", refresh_token=refresh_token, access_token=access_token)    

    @handle_error
    async def change_password_service(self,  data: ChangePassword, current_user: UserBase):
        if not is_valid_password(data.current_password, current_user.password):
            return UnauthorizedError("Incorrect current password")
        await crud_user.update(self.session, id=current_user.id, obj_in={"hashed_password": get_password_hash(data.new_password)})

        return SuccessResponse("Password changed successfully")

   
       