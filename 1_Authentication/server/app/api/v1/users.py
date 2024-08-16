from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import CurrentUser, SessionDep 
from core.security import get_password_hash
from crud.users import crud_user
from schemas.users import UserCreate, UserInDB, User, UserUpdate

router = APIRouter(prefix="/users")


@router.get("/", response_model=List[User])
async def read_users(
    current_user: CurrentUser,
    session: SessionDep,
    offset: int = 0,
    limit: int = 100
):
    """
    Retrieve users.
    """
    users = await crud_user.get_multi(session, offset=offset, limit=limit)
    return users

@router.get("/{user_id}/", response_model=User)
async def read_user(
    user_id: int,
    current_user: CurrentUser,
    session: SessionDep,
):
    """
    Get a specific user by id.
    """
    if current_user.id == user_id:
        return current_user
    
    else:
        try:
            user = await crud_user.get(session, id=user_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
@router.post("/", response_model=User)
async def create_user(
    user_in: UserCreate,
    current_user: CurrentUser,
    session: SessionDep,
):
    """
    Create new user.
    """
    obj_in = UserInDB(
        **user_in.dict(), hashed_password=get_password_hash(user_in.password)
    )
    try:
        new_user = await crud_user.create(session, obj_in)
        return new_user
    except IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )



@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: CurrentUser,
    session: SessionDep,
):
    update_data = user_in.dict(exclude={"password"}, exclude_none=True)
    if user_in.password:
        update_data["hashed_password"] = get_password_hash(user_in.password)

    try:
        updated_user = await crud_user.update(
            session,
            db_obj_id=user_id,
            obj_in=update_data
        )
        return updated_user
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID does not exist in the system",
        )



@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: CurrentUser,
    session: SessionDep,
):
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="User can't delete itself")

    try:
        user = await crud_user.get(session, id=user_id)
        await crud_user.delete(session, db_obj=user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")