from typing import Optional
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int = Field(..., gt=0)

class ItemUpdate(ItemBase):
    pass
class ItemInDB(ItemBase):
    owner_id: int = Field(..., gt=0)
class ItemUpdateDB(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int = Field(..., gt=0)

    class Config:
        from_attributes=True




