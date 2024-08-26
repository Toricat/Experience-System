

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .users import User

class VerifyCode(BaseModel):
    verify_code: str = Field(..., min_length=1)
class VerifyBase(BaseModel): 
    verify_code: Optional[str] = Field(None, min_length=1)
    exp: Optional[datetime] = None
class CreateVerify(VerifyBase):
    pass
class VerifyInDB(VerifyBase):
    user_id: Optional[int] = Field(None, gt=0)
    exp: Optional[datetime] = None

class VerifyUpdateDB(VerifyBase):
    pass
class Verify(VerifyBase):
    id: int
    User: Optional[User]
    class Config:
        from_attributes=True