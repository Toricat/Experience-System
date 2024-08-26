from fastapi import APIRouter, HTTPException, Depends

from api.deps import SessionDep, RoleChecker
from fastapi.security import OAuth2PasswordRequestForm

from schemas.tokens import TokenLogin
from schemas.users import UserCreate, UserMe, User
from schemas.verifies import VerifyCode
from schemas.authetications import ChangePassword, TokenRefresh, VerifyCodeSend,VerifyCodeComfirm
from services.authetications import AuthService

auth_service = AuthService()

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenLogin)
async def login(session: SessionDep, data: OAuth2PasswordRequestForm = Depends()):
    result = await auth_service.login_service(session, data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/register", response_model=VerifyCode)
async def register(session: SessionDep, data: UserCreate):
    result = await auth_service.register_service(session, data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/refresh-token", response_model=TokenLogin)
async def refresh_token(
    token_data: TokenRefresh, 
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "manager", "user"])) 
):
    result = await auth_service.refresh_token_service(session, token_data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/reset-password")
async def change_password(
    data: ChangePassword, 
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "manager", "user"]))
):
    result = await auth_service.change_password_service(session, data, current_user)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/verify/code", response_model=VerifyCode)
async def verify_code_by_email(data: VerifyCodeSend, session: SessionDep):
    result = await auth_service.verify_code_by_email_service(session, data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/verify/code/confirm")
async def confirm_verify_code(data: VerifyCodeComfirm, session: SessionDep):
    result = await auth_service.confirm_verify_code_service(session, data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.get("/me", response_model=UserMe)
async def read_users_me(
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "manager", "user"]))):
    result = current_user.dict()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
