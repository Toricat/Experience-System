from fastapi import APIRouter

from api.deps import SessionDep,handle_service_result

from schemas.authetications import  VerifyEmailSend,VerifyCodeComfirm,VerifyCodeChangePassword
from schemas.utils import Message

from services.verify import VerifyService

verify_service = VerifyService()

router = APIRouter(prefix="/verify")



@router.post("/active/code", response_model=Message)
async def active_code_by_email(
    data: VerifyEmailSend, 
    session: SessionDep
):
    result = await verify_service.active_code_by_email_service(session, data)
    return handle_service_result(result)

@router.post("/active/code/confirm",response_model=Message)
async def confirm_active_code(
    data: VerifyCodeComfirm, 
    session: SessionDep
):
    result = await verify_service.confirm_active_code_service(session, data)
    return handle_service_result(result)
@router.post("/active/code/active-account",response_model=Message)
async def confirm_verify_code_active_account(
    data: VerifyCodeComfirm, 
    session: SessionDep
    ):
    result = await verify_service.confirm_active_code_account_service(session, data)
    return handle_service_result(result)
@router.post("/recovery/code", response_model=Message)
async def recovery_code_by_email(
    data: VerifyEmailSend, 
    session: SessionDep):
    result = await verify_service.recovery_code_by_email_service(session, data)
    return handle_service_result(result)

@router.post("/recovery/code/confirm",response_model=Message)
async def confirm_recovery_code(
    data: VerifyCodeComfirm, 
    session: SessionDep
    ):
    result = await verify_service.confirm_recovery_code_service(session, data)
    return handle_service_result(result)

@router.post("/code/change-password",response_model=Message)
async def confirm_recovery_code_change_password(
    session: SessionDep,
    data: VerifyCodeChangePassword, 
    ):
    result = await verify_service.confirm_recovery_code_change_password_service(session, data)
    return handle_service_result(result)