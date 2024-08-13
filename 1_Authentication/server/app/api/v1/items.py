from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import  SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user, get_session
from crud.items import crud_item  

from models.users import User
from schemas.items import Item, ItemCreate, ItemUpdate, ItemInDB

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[Item])
async def read_items(
    security_scopes: SecurityScopes,
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve items. Only accessible by admin.
    """
    if "admin" not in security_scopes.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    items = await crud_item.get_multi(session, offset=offset, limit=limit)
    return items

@router.post("/", response_model=Item)
async def create_item(
    security_scopes: SecurityScopes,
    item_in: ItemCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create new item. Accessible by manager or admin.
    """
    if not set(security_scopes.scopes).intersection({"manager", "admin"}):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    item = await crud_item.get(session, name=item_in.name)
    if item is not None:
        raise HTTPException(
            status_code=409,
            detail="The item with this name already exists in the system",
        )
    obj_in = ItemInDB(
        **item_in.dict()
    )
    return await crud_item.create(session, obj_in)

@router.get("/{item_id}/", response_model=Item)
async def read_item(
    security_scopes: SecurityScopes,
    item_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a specific item by id. Users can only access their own items.
    """
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Only allow user to see their own items or if they are manager/admin
    if "user" in security_scopes.scopes and current_user.role == "user" and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this item"
        )
    return item

@router.put("/{item_id}/", response_model=Item)
async def update_item(
    security_scopes: SecurityScopes,
    item_id: int,
    item_in: ItemUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update an item. Only accessible by admin.
    """
    if "admin" not in security_scopes.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="The item with this name does not exist in the system",
        )
    return await crud_item.update(session, db_obj=item, obj_in=item_in.dict(exclude_none=True))

@router.delete("/{item_id}/", status_code=204)
async def delete_item(
    security_scopes: SecurityScopes,
    item_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete an item. Only accessible by admin.
    """
    if "admin" not in security_scopes.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    item = await crud_item.get(session, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await crud_item.delete(session, db_obj=item)
