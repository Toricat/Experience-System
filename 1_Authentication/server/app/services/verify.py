 
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
from schemas.verifies import ActivateCodeInDB,RecoveryCodeInDB
from schemas.authetications import  TokenRefresh,ChangePassword, VerifyCodeComfirm,VerifyEmailSend,VerifyCodeChangePassword, Login 
from schemas.utils import InfoEmailSend


class  VerifyService:
        def __init__(self):
            pass
        @handle_error
        async def active_code_by_email_service(self, session, data: VerifyEmailSend):
            user = await crud_user.get(session, email=data.email)
            if user is None:
                return NotFoundError("User not found")
        
            verify_active = await crud_verify.get(session, return_columns=["id","exp_active"],user_id=user.id)
            if verify_active is not None and verify_active.exp_active > datetime.utcnow():
                return SuccessResponse("Already send code. Please check your email to verify your account.")
            
            new_code_active, new_exp_active = create_verify_code()
            new_verify_active = ActivateCodeInDB(code_active=new_code_active,exp_active=new_exp_active, user_id=user.id)

            if verify_active is not None and verify_active.exp_active < datetime.utcnow():
                await crud_verify.update(session, id=verify_active.id, obj_in=new_verify_active.dict(exclude_unset=True, exclude_none=True))
            else:
                await crud_verify.create(session , obj_in=new_verify_active)
            info = InfoEmailSend(email=data.email,name=user.full_name, verification_code=new_code_active)
            html_content = await render_email_template("verify_code.html",**info.dict())
            response = await send_email(
                email_to=data.email,
                subject="Your Activation Code",
                html_content=html_content)
            if not response:
                return BadRequestError("Failed to send email")
            return SuccessResponse("Successfully send code. Please check your email to verify your account.")
        

        @handle_error
        async def recovery_code_by_email_service(self, session, data: VerifyEmailSend):
            user = await crud_user.get(session, email=data.email)
            if user is None:
                return NotFoundError("User not found")
        
            verify_recovery = await crud_verify.get(session, return_columns = ["id","exp_recovery"],user_id=user.id)
            print("hello",verify_recovery )
            if verify_recovery.exp_recovery is not None and verify_recovery.exp_recovery > datetime.utcnow():
                return SuccessResponse("Already send code. Please check your email to verify your account.")
            
            new_code_recovery, new_exp_recovery = create_verify_code()
            new_verify_recovery = RecoveryCodeInDB(code_recovery=new_code_recovery,exp_recovery=new_exp_recovery, user_id=user.id)
            print("hello",new_verify_recovery)
            if verify_recovery.exp_recovery is not None and verify_recovery.exp_recovery < datetime.utcnow():

                await crud_verify.update(session, id=verify_recovery.id, obj_in=new_verify_recovery.dict(exclude_unset=True, exclude_none=True))
            else:
                await crud_verify.update(session , id=verify_recovery.id, obj_in=new_verify_recovery.dict(exclude_unset=True, exclude_none=True))
            info = InfoEmailSend(email=data.email,name=user.full_name, verification_code=new_code_recovery)
            html_content = await render_email_template("verify_code.html",**info.dict())
            response = await send_email(
                email_to=data.email,
                subject="Your Recovery Code",
                html_content=html_content)
            if not response:
                return BadRequestError("Failed to send email")
            return SuccessResponse("Successfully sent code. Please check your email to recover your account.")
        
        @handle_error
        async def confirm_active_code(self, session, data: VerifyCodeComfirm):
            verify_active = await crud_verify.get(session,return_columns=["exp_active","user_id"], code_active=data.verify_code,email=data.email)
            if verify_active is None:
                return UnauthorizedError("Invalid verify code")
            if verify_active.exp_active < datetime.utcnow():
                return UnauthorizedError("Expired verify code")
            verify_user = await crud_user.get(session,return_columns=["email","id"], email=data.email)
            if verify_user is None:
                return UnauthorizedError("Invalid email")
            if verify_user.id != verify_active.user_id:
                return UnauthorizedError("Invalid email")
            return  verify_active
        
        @handle_error
        async def confirm_active_code_service(self, session, data: VerifyCodeComfirm):
            verify_active = await self.confirm_active_code(session,data)

            if isinstance(verify_active, UnauthorizedError):
                return verify_active
            return SuccessResponse("Active code confirmed")
        
        @handle_error
        async def confirm_active_code_account_service(self, session, data: VerifyCodeComfirm):
            verify_active = await self.confirm_active_code(session, data=data)
            if isinstance(verify_active, UnauthorizedError):
                return verify_active
            obj_in = UserActivate(is_active=True)
            await crud_user.update(session, id=verify_active.user_id, email=data.email,obj_in=obj_in)
            return SuccessResponse("User Activated")

        @handle_error
        async def confirm_recovery_code(self, session, data: VerifyCodeComfirm):
            verify_recovery = await crud_verify.get(session,return_columns=["exp_recovery","user_id"], code_recovery=data.verify_code)
            if verify_recovery is None:
                return UnauthorizedError("Invalid recovery code")
            if verify_recovery.exp_recovery < datetime.utcnow():
                return UnauthorizedError("Expired recoveryy code")
            verify_user = await crud_user.get(session,return_columns=["email","id"], email=data.email)
            if verify_user is None:
                return UnauthorizedError("Invalid email")
            if verify_user.id != verify_recovery.user_id:
                return UnauthorizedError("Invalid email")
            return  verify_recovery

        @handle_error
        async def confirm_recovery_code_service(self, session, data: VerifyCodeComfirm):
            verify_recovery = await self.confirm_recovery_code(session,data)
            print(verify_recovery)
            if isinstance( verify_recovery, UnauthorizedError):
                return  verify_recovery
            return SuccessResponse("Recovery code confirmed")
        
        @handle_error
        async def confirm_recovery_code_change_password_service(self, session, data: VerifyCodeChangePassword):
            verify_recovery = await self.confirm_recovery_code(session, data=data)
            print(verify_recovery)
            if isinstance(verify_recovery, UnauthorizedError):
                return verify_recovery
            await crud_user.update(session, id=verify_recovery.user_id, obj_in={"hashed_password": get_password_hash(data.new_password)})
            return SuccessResponse("Password changed successfully")
            
