from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError
from .common.utils import handle_db_errors
from crud.items import crud_item
from schemas.items import ItemCreate, ItemUpdate, ItemInDB

class ItemService:
    
    def _build_conditions(self, current_user, item_id):

        if current_user.role not in ["admin"]:
            return {"id": item_id, "owner_id": current_user.id}
        return {"id": item_id}
    @handle_db_errors
    async def read_items(self, session, offset: int, limit: int):
        return await crud_item.get_multi(session, offset=offset, limit=limit)
    @handle_db_errors
    async def get_item(self, session, item_id: int, current_user):

        return await crud_item.get(session, **self._build_conditions(current_user, item_id))

    @handle_db_errors
    async def create_item(self, session, item_in: ItemCreate):
        item_in_db = ItemInDB(**item_in.dict())
     
        return await crud_item.create(session, obj_in=item_in_db)

    @handle_db_errors
    async def update_item(self, session, item_id: int, item_in: ItemUpdate, current_user):
    
        update_data = item_in.dict(exclude_none=True)
        return await crud_item.update(
            session, 
            obj_in=update_data,
            **self._build_conditions(current_user, item_id)
        )

    @handle_db_errors
    async def delete_item(self, session, item_id: int, current_user):
      
        return await crud_item.delete(session, **self._build_conditions(current_user, item_id))
       