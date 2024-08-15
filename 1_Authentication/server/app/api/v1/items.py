from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import CurrentUser, SessionDep
from crud.items import crud_item  
from crud.users import crud_user

from schemas.items import Item, ItemCreate, ItemUpdate, ItemInDB

router = APIRouter(prefix="/items")

@router.get("/", response_model=List[Item])
async def read_items( session:  SessionDep, current_user :CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retrieve items
    """
    
    items = await crud_item.get_multi(session, offset=offset, limit=limit)
    return items

@router.post("/", response_model=Item)
async def create_item(
    item_in: ItemCreate,
   session:  SessionDep, current_user :CurrentUser,
   
):
    """
    Create new item
    """
    
    item = await crud_item.get(session, title=item_in.title)
    if item is not None:
        raise HTTPException(
            status_code=409,
            detail="The item with this name already exists in the system",
        )
    user = await crud_user.get(session, id=current_user.id)
    if not user.is_active:
        raise HTTPException(
            status_code=400, 
            detail="Inactive user"  
        )
    if user is None:
        raise HTTPException(
            status_code=400, 
            detail="ID of User not found"  
        )

    obj_in = ItemInDB(
        **item_in.dict()
    )
    item = await crud_item.create(session, obj_in)
    return item

@router.get("/{item_id}/", response_model=Item)
async def read_item(
    item_id: int,
   session:  SessionDep, current_user :CurrentUser,
):
    """
    Get a specific item by id
    """
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@router.put("/{item_id}/", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    session:  SessionDep, current_user :CurrentUser,
):
    """
    Update an item
    """
    
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="The item with this name does not exist in the system",
        )
    return await crud_item.update(session, db_obj=item, obj_in=item_in.dict(exclude_none=True))

@router.delete("/{item_id}/", status_code=204)
async def delete_item(
    item_id: int,
   session:  SessionDep, current_user :CurrentUser,
):
    """
    Delete an item
    """
    
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await crud_item.delete(session, db_obj=item)
