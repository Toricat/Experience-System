from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int
    pass

class ItemUpdate(ItemBase):
    pass

class ItemUpdateDB(BaseModel):
    title: Optional[str] = None

class Item(BaseModel):
    id: int
    owner_id: int

    class Config:
        from_attributes=True

class ItemInDB(Item):
    pass


