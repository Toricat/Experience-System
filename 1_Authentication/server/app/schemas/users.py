from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, min_length=1) 
    full_name: Optional[str] = Field(None, min_length=3) 
    image: Optional[str] = None
    role: Optional[str] = Field("user", min_length=1)  
    is_active: Optional[bool] = None 

class UserCreate(UserBase):
    email: EmailStr  
    password: str = Field(..., min_length=6)  

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6)  
    is_active: Optional[bool] = None  

class UserInDB(UserBase):
    hashed_password: str
    account_type: Optional[str] = "local"
    is_active: Optional[bool] = False

class UserUpdateDB(UserBase):
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes=True

class UserMe(UserBase):
    pass
