

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .users import User

class VerifyCode(BaseModel):
    verify_code: str 
class VerifyBase(BaseModel): 
    verify_code: Optional[str]
    exp: Optional[datetime] 
class CreateVerify(VerifyBase):
    pass
class VerifyInDB(VerifyBase):
    user_id: Optional[int]
    exp: Optional[datetime] 

class VerifyUpdateDB(VerifyBase):
    pass
class Verify(VerifyBase):
    id: int
    User: Optional[User]
    class Config:
        from_attributes=True