from typing import Literal,Optional
from pydantic import BaseModel
from datetime import datetime
from .users import User

class TokenLogin(BaseModel):
    token_type: Literal["bearer"]
    refresh_token: Optional[str]
    access_token: Optional[str]
class TokenBase(BaseModel): 
    refresh_token: Optional[str]
class AccessTokenPayload(BaseModel):
    user_id: Optional[str]
    exp: Optional[int]
class CreateToken(TokenBase):
    pass
class TokenInDB(TokenBase):
    user_id: Optional[int]
    exp: Optional[datetime] 

class TokenUpdate(TokenBase):
    pass
class Token(TokenBase):
    id: int
    User: Optional[User]
    class Config:
        from_attributes=True




