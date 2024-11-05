from repositories.items import items_repo
from schemas.items import ItemCreate, ItemUpdate, ItemInDB

from utils.errors.item import ItemNotFoundError

from logging import getLogger
logger = getLogger(__name__)

class ItemService:
    def __init__(self):
        self.items_repo = items_repo
    
    async def get_item_service(self,session, item_id: int):
        result = await  self.items_repo.get(session, filters={"id": item_id})
        return result

    
    async def get_multi_items_service(self,session, offset: int, limit: int):
        result= await  self.items_repo.get_all(session, offset=offset, limit=limit )
        if not result:
            raise ItemNotFoundError()
        return result
    
    
    async def create_item_service(self,  session, item_in: ItemCreate):
        item_create = ItemInDB(
            **item_in.model_dump()
            )
        result= await  self.items_repo.create(session, data = item_create.model_dump())
        return result

    
    async def update_item_service(self, session, item_id: int, item_in: ItemUpdate):
        item_update = ItemUpdate(
            **item_in.dict(exclude_unset=True, exclude_none=True)
            )
        result =await  self.items_repo.update(session,filters={"id": item_id}, data = item_update.model_dump())
        return result
    
    async def delete_item_service(self, session, item_id: int):
        result = await  self.items_repo.delete(session, filters={"id": item_id})
        if not result:
            return ItemNotFoundError()
        return {"message": "Delete success"}
    
  
