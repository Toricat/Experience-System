from pydantic import BaseModel

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
class  TokenRefresh(BaseModel):
    refresh_token: str
    user_id: int
class VerifyCodeSend(BaseModel):
    email: str
class VerifyCodeComfirm(BaseModel):
    verify_code: str 
class VerifyCodeChangePassword(BaseModel):
    new_password: str
    verify_code: str