from pydantic import BaseModel
class Login (BaseModel):
    username: str
    password: str
class ChangePassword(BaseModel):
    current_password: str
    new_password: str
class TokenRefresh(BaseModel):
    refresh_token: str
    user_id: int
class VerifyEmailSend(BaseModel):
    email: str
class VerifyCodeComfirm(BaseModel):
    verify_code: str 
class VerifyCodeChangePassword(BaseModel):
    new_password: str
    verify_code: str