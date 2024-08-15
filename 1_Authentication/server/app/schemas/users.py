from typing import Optional
from .items import ItemBase
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    image: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str]
    is_active: Optional[bool] 

class UserInDB(UserBase):
    hashed_password: str
    account_type: Optional[str] = "local"
    is_active: Optional[bool] = False


class UserUpdateDB(UserBase):
    hashed_password: Optional[str] 
    is_active: Optional[bool] 

class User(UserBase):
    id: int

    class Config:
        from_attributes=True

class UserMe(UserBase):
    items: list[ItemBase]
