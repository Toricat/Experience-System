from typing import Optional
from .items import ItemBase
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    image: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str]

class UserInDB(UserBase):
    hashed_password: str

class UserUpdateDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes=True

class UserMe(UserBase):
    items: list[ItemBase]