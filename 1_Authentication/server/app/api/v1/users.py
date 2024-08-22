from fastapi import APIRouter, Depends, HTTPException

from api.deps import SessionDep, RoleChecker
from schemas.users import UserCreate, User, UserUpdate
from services.users import UserService

user_service = UserService()

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[User])
async def read_users(
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "manager"])) 
):
    return await user_service.read_users(session)

@router.get("/{user_id}/", response_model=User)
async def read_user(
    user_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "manager", "user"])) 
):
    if current_user.id != user_id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await user_service.read_user(session, user_id)

@router.post("/", response_model=User)
async def create_user(
    session: SessionDep, 
    user_in: UserCreate, 
    current_user: User = Depends(RoleChecker(["admin"])) 
):
    return await user_service.create_user(session, user_in)

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    session: SessionDep,
    user_in: UserUpdate,
    current_user: User = Depends(RoleChecker(["admin", "user"])) 
):
    if current_user.id != user_id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await user_service.update_user(session, user_id, user_in)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin"])) 
):
    return await user_service.delete_user(session, user_id)
