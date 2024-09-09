from datetime import datetime
from .common.utils import send_email, render_email_template

from core.security import create_verify_code, get_password_hash
from repositories.users import crud_user
from repositories.verifies import crud_verify
from schemas.verifies import ActivateCodeInDB, RecoveryCodeInDB
from schemas.auths import VerifyCodeComfirm, VerifyEmailSend, VerifyCodeChangePassword
from schemas.utils import InfoEmailSend

# Import custom errors
from utils.error.verify import (
    ActivateCodeNotFoundError, ActivateCodeExpiredError, ActivateCodeAlreadyUsedError,
    RecoveryCodeNotFoundError, RecoveryCodeExpiredError, RecoveryCodeAlreadyUsedError
)
from utils.error.auth import EmailSendFailureError,UnauthorizedError
from utils.error.user import UserNotFoundError, ConflictError


class VerifyService:
    def __init__(self):
        pass
    
    async def active_code_by_email_service(self, session, data: VerifyEmailSend):
        """
        Send activation code to user's email. If code already sent and not expired, 
        return a message indicating the code has already been sent.
        """
        user = await crud_user.get(session, email=data.email)
        if user is None:
            raise UserNotFoundError()

        verify_active = await crud_verify.get(session, return_columns=["id", "exp_active"], user_id=user.id)
        if verify_active and verify_active.exp_active and verify_active.exp_active > datetime.now():
            return {"message": "Already sent code. Please check your email to verify your account."}

        # Generate new activation code
        new_code_active, new_exp_active = create_verify_code()
        new_verify_active = ActivateCodeInDB(code_active=new_code_active, exp_active=new_exp_active, user_id=user.id)

        if verify_active:
            await crud_verify.update(session, id=verify_active.id, obj_in=new_verify_active.dict(exclude_unset=True, exclude_none=True))
        else:
            await crud_verify.create(session, obj_in=new_verify_active)

        # Send email with activation code
        info = InfoEmailSend(email=data.email, name=user.full_name, verification_code=new_code_active)
        html_content = await render_email_template("verify_code.html", **info.dict())
        response = await send_email(
            email_to=data.email,
            subject="Your Activation Code",
            html_content=html_content
        )
        if not response:
            raise EmailSendFailureError()

        return {"message": "Successfully sent code. Please check your email to verify your account."}

    
    async def recovery_code_by_email_service(self, session, data: VerifyEmailSend):
        """
        Send recovery code to user's email. If code already sent and not expired,
        return a message indicating the code has already been sent.
        """
        user = await crud_user.get(session, email=data.email)
        if user is None:
            raise UserNotFoundError()

        verify_recovery = await crud_verify.get(session, return_columns=["id", "exp_recovery"], user_id=user.id)
        if verify_recovery and verify_recovery.exp_recovery and verify_recovery.exp_recovery > datetime.now():
            return {"message": "Already sent code. Please check your email to recover your account."}

        # Generate new recovery code
        new_code_recovery, new_exp_recovery = create_verify_code()
        new_verify_recovery = RecoveryCodeInDB(code_recovery=new_code_recovery, exp_recovery=new_exp_recovery, user_id=user.id)

        if verify_recovery:
            await crud_verify.update(session, id=verify_recovery.id, obj_in=new_verify_recovery.dict(exclude_unset=True, exclude_none=True))
        else:
            await crud_verify.create(session, obj_in=new_verify_recovery)

        # Send email with recovery code
        info = InfoEmailSend(email=data.email, name=user.full_name, verification_code=new_code_recovery)
        html_content = await render_email_template("verify_code.html", **info.dict())
        response = await send_email(
            email_to=data.email,
            subject="Your Recovery Code",
            html_content=html_content
        )
        if not response:
            raise EmailSendFailureError()

        return {"message": "Successfully sent code. Please check your email to recover your account."}

    
    async def confirm_active_code(self, session, data: VerifyCodeComfirm):
        """
        Confirm the activation code. Raises appropriate errors if the code is invalid,
        expired, or already used.
        """
        verify_active = await crud_verify.get(session, return_columns=["exp_active", "user_id", "used_active"], code_active=data.verify_code)
        if verify_active is None:
            raise ActivateCodeNotFoundError()
        if verify_active.used_active:
            raise ActivateCodeAlreadyUsedError()
        if verify_active.exp_active < datetime.now():
            raise ActivateCodeExpiredError()

        verify_user = await crud_user.get(session, return_columns=["email", "id", "is_active"], email=data.email)
        if verify_user is None or verify_user.id != verify_active.user_id:
            raise UnauthorizedError("Invalid email or mismatch with the user ID.")
        if verify_user.is_active:
            raise ConflictError("User already activated.")
        
        return verify_active

    
    async def confirm_active_code_service(self, session, data: VerifyCodeComfirm):
        """
        Service to confirm the activation code without updating user status.
        """
        verify_active = await self.confirm_active_code(session, data)
        return {"message": "Activation code confirmed."}

    
    async def confirm_active_code_account_service(self, session, data: VerifyCodeComfirm):
        """
        Service to confirm the activation code and activate the user account.
        """
        verify_active = await self.confirm_active_code(session, data)

        # Update user and mark activation code as used
        await crud_user.update(session, id=verify_active.user_id, email=data.email, obj_in={"is_active": True})
        await crud_verify.update(session, user_id=verify_active.user_id, obj_in={"used_active": True})

        return {"message": "User activated successfully."}

    
    async def confirm_recovery_code(self, session, data: VerifyCodeComfirm):
        """
        Confirm the recovery code. Raises appropriate errors if the code is invalid,
        expired, or already used.
        """
        verify_recovery = await crud_verify.get(session, return_columns=["exp_recovery", "user_id", "used_recovery"], code_recovery=data.verify_code)
        if verify_recovery is None:
            raise RecoveryCodeNotFoundError()
        if verify_recovery.used_recovery:
            raise RecoveryCodeAlreadyUsedError()
        if verify_recovery.exp_recovery < datetime.now():
            raise RecoveryCodeExpiredError()

        verify_user = await crud_user.get(session, return_columns=["email", "id"], email=data.email)
        if verify_user is None or verify_user.id != verify_recovery.user_id:
            raise UnauthorizedError("Invalid email or mismatch with the user ID.")

        return verify_recovery

    
    async def confirm_recovery_code_service(self, session, data: VerifyCodeComfirm):
        """
        Service to confirm the recovery code without changing the password.
        """
        verify_recovery = await self.confirm_recovery_code(session, data)
        return {"message": "Recovery code confirmed."}

    
    async def confirm_recovery_code_change_password_service(self, session, data: VerifyCodeChangePassword):
        """
        Service to confirm the recovery code and change the user's password.
        """
        verify_recovery = await self.confirm_recovery_code(session, data)

        await crud_user.update(session, id=verify_recovery.user_id, obj_in={"hashed_password": get_password_hash(data.new_password)})
        await crud_verify.update(session, user_id=verify_recovery.user_id, obj_in={"used_recovery": True})

        return {"message": "Password changed successfully."}
