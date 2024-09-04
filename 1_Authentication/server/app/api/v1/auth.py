from fastapi import APIRouter, Depends

from api.deps import SessionDep, RoleChecker,handle_service_result
from fastapi.security import OAuth2PasswordRequestForm

from schemas.tokens import TokenLogin
from schemas.users import UserCreate, UserMe, User
from schemas.authetications import ChangePassword, TokenRefresh, VerifyEmailSend,VerifyCodeComfirm,VerifyCodeChangePassword
from schemas.utils import Message

from services.authentications import AuthService

auth_service = AuthService()

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenLogin)
async def login(
    session: SessionDep,
    data: OAuth2PasswordRequestForm = Depends()):
    result = await auth_service.login_service(session, data=data )  
    return handle_service_result(result)

@router.post("/register",response_model=Message)
async def register(
    session: SessionDep,
    data: UserCreate):
    result = await auth_service.register_service(session, data)
    return handle_service_result(result)

@router.post("/refresh-token", response_model=TokenLogin)
async def refresh_token(
    session: SessionDep,
    token_data: TokenRefresh, 
):
    result = await auth_service.refresh_token_service( session,token_data)
    return handle_service_result(result)

@router.get("/me", response_model=UserMe)
async def read_users_me(
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "user"]))):
    result = current_user.dict()
    return handle_service_result(result)

@router.post("/update-me",response_model=Message)
async def change_password(
    session: SessionDep,
    data: ChangePassword, 
    current_user: User = Depends(RoleChecker(["admin","user"]))
):
    result = await auth_service.change_password_service(session, data, current_user)
    return handle_service_result(result)