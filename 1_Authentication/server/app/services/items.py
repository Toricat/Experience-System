from .common.exceptions import (
    SuccessResponse,
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
)
from .common.handle import handle_error

from crud.items import crud_item
from schemas.items import ItemCreate, ItemUpdate, ItemInDB

class ItemService:
    def __init__(self):
        pass
    @handle_error
    async def get_item_service(self,session, item_id: int,kwargs):
        return await crud_item.get(session, id=item_id, **kwargs)

    @handle_error
    async def get_multi_items_service(self,session, offset: int, limit: int,kwargs):
        result= await crud_item.get_multi(session, offset=offset, limit=limit,**kwargs )
        return result
    
    @handle_error
    async def create_item_service(self,  session, item_in: ItemCreate,kwargs):
        obj_in = ItemInDB(
            **item_in.dict()
            )
        print(obj_in)
        result= await crud_item.create(session, obj_in = obj_in,**kwargs )
        return result

    @handle_error
    async def update_item_service(self, session, item_id: int, item_in: ItemUpdate,kwargs):
        obj_in = ItemUpdate(
            **item_in.dict(exclude_unset=True, exclude_none=True)
            )
        print(obj_in)
        print(kwargs)
        result =await crud_item.update(session,id=item_id, obj_in = obj_in,**kwargs )
        return result
    @handle_error
    async def delete_item_service(self, session, item_id: int,kwargs):
        result=await crud_item.delete(session, id=item_id,**kwargs )
        if not result:
            return NotFoundError("Resource not found or does not exist.")
        return  SuccessResponse("Delete success")
    
  
