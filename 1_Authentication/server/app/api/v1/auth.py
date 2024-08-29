from fastapi import APIRouter, Depends

from api.deps import SessionDep, RoleChecker,handle_service_result
from fastapi.security import OAuth2PasswordRequestForm

from schemas.tokens import TokenLogin
from schemas.users import UserCreate, UserMe, User
from schemas.authetications import ChangePassword, TokenRefresh, VerifyCodeSend,VerifyCodeComfirm,VerifyCodeChangePassword
from schemas.utils import Message

from services.authetications import AuthService

auth_service = AuthService()

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenLogin)
async def login(
    session: SessionDep, 
    data: OAuth2PasswordRequestForm = Depends()):
    result = await auth_service.login_service(session, data)  
    return handle_service_result(result)

@router.post("/register",response_model=Message)
async def register(
    session: SessionDep, 
    data: UserCreate):
    result = await auth_service.register_service(session, data)
    return handle_service_result(result)

@router.post("/refresh-token", response_model=TokenLogin)
async def refresh_token(
    token_data: TokenRefresh, 
    session: SessionDep, 
):
    result = await auth_service.refresh_token_service(session, token_data)
    return handle_service_result(result)

@router.post("/update-me",response_model=Message)
async def change_password(
    data: ChangePassword, 
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin","user"]))
):
    result = await auth_service.change_password_service(session, data, current_user)
    return handle_service_result(result)

@router.post("/verify/code", response_model=Message)
async def verify_code_by_email(
    data: VerifyCodeSend, 
    session: SessionDep):
    result = await auth_service.verify_code_by_email_service(session, data)
    return handle_service_result(result)
@router.post("/verify/code/confirm",response_model=Message)
async def confirm_verify_code(
    data: VerifyCodeComfirm, 
    session: SessionDep
    ):
    result = await auth_service.confirm_verify_code_service(session, data)
    return handle_service_result(result)
@router.post("/verify/code/confirm/active-account",response_model=Message)
async def confirm_verify_code_active_account(
    data: VerifyCodeComfirm, 
    session: SessionDep
    ):
    result = await auth_service.confirm_verify_code_active_account_service(session, data)
    return handle_service_result(result)

@router.post("/verify/code/confirm/change-password",response_model=Message)
async def confirm_verify_code_change_password(
    session: SessionDep,
    data: VerifyCodeChangePassword, 
    ):
    result = await auth_service.confirm_verify_code_change_password_service(session, data)
    return handle_service_result(result)


@router.get("/me", response_model=UserMe)
async def read_users_me(
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "user"]))):
    result = current_user.dict()
    return handle_service_result(result)
