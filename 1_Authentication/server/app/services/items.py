from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
)
from .common.utils import handle_error

from crud.items import crud_item
from schemas.items import ItemCreate, ItemUpdate, ItemInDB

class ItemService:

    @handle_error
    async def get_items_service(self, session, offset: int, limit: int):
        result= await crud_item.get_multi(session, offset=offset, limit=limit)
        return result
    @handle_error
    async def get_item_service(self, session, Item_id: int):
        result = await crud_item.get(session, id=Item_id)  
        return result

    @handle_error
    async def create_item_service(self, session, Item_in: ItemCreate):
        obj_in = ItemInDB(
            **Item_in.dict()
        )
        result= await crud_item.create(session, obj_in)
        return result

    @handle_error
    async def update_item_service(self, session, Item_id: int, Item_in: ItemUpdate):
        update_data =Item_in.dict(exclude_unset=True, exclude_none=True)
        obj_in = ItemUpdate(**update_data)
        result =await crud_item.update(session,id=Item_id,obj_in= obj_in)
        return result
    @handle_error
    async def delete_item_service(self, session, Item_id: int):
        result=await crud_item.delete(session, id=Item_id)
        return  result
    
  
