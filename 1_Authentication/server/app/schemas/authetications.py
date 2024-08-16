from pydantic import BaseModel

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
class  TokenRefresh(BaseModel):
    refresh_token: str
    user_id: int
class RecoveryPassword(BaseModel):
    email: str

class ComfirmVerifyCode(BaseModel):
    user_id: int
    verify_code: str 