from fastapi import APIRouter, Depends, HTTPException

from api.deps import SessionDep, RoleChecker

from schemas.items import Item, ItemCreate, ItemUpdate
from schemas.users import  User
from services.items import ItemService

item_service = ItemService()

router = APIRouter(prefix="/items")

@router.get("/", response_model=list[Item])
async def read_items(
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin"])),
    offset: int = 0,
    limit: int = 100,
):
    """
    Retrieve items
    """
    
    result = await item_service.get_items_service(session, offset=offset, limit=limit)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.get("/{item_id}/", response_model=Item)
async def read_item(
    item_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "user"])),
):
    """
    Get a specific item by id
    """
    result = await item_service.get_item_service(session, item_id) 
    
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.post("/", response_model=Item)
async def create_item(
    item_in: ItemCreate,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "user"])),
):
    """
    Create new item
    """
    result = await item_service.create_item_service(session, item_in)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result


@router.put("/{item_id}/", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "user"])),
):
    """
    Update an item
    """
    result = await item_service.update_item_service(session, item_id, item_in)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.delete("/{item_id}/", status_code=204)
async def delete_item(
    item_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin"])),
):
    """
    Delete an item
    """
    result = await item_service.delete_item_service(session, item_id)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return {"msg": "Item deleted"}
