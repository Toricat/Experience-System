from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(ItemBase):
    title: str
    description: Optional[str] = None
class ItemInDB(ItemBase):
    owner_id: int
class ItemUpdateDB(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes=True




