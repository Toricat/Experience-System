from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
)
from .common.utils import handle_error

from core.security import get_password_hash

from crud.users import crud_user
from schemas.users import UserCreate, UserUpdate, UserInDB,UserUpdateDB

class UserService:

    @handle_error
    async def get_users_service(self, session, offset: int, limit: int):
        result =  await crud_user.get_multi(session, offset=offset, limit=limit)
        return  result 

    @handle_error
    async def get_user_service(self, session, user_id: int):
        result = await crud_user.get(session, id=user_id)
        return  result
    

    @handle_error
    async def create_user_service(self, session, user_in: UserCreate):
        hashed_password = get_password_hash(user_in.password)
        obj_in = UserInDB(
            **user_in.dict(),
            hashed_password=hashed_password,
        )
        result = await crud_user.create(session, obj_in)
        return result

    # @handle_error
    async def update_user_service(self, session, user_id: int, user_in: UserUpdate):
        update_data = user_in.dict(exclude_unset=True, exclude_none=True)
        obj_in = UserUpdateDB(**update_data,hashed_password=get_password_hash(user_in.password))
        result = await crud_user.update(session, id=user_id, obj_in= obj_in)
        return result

    @handle_error
    async def delete_user_service(self, session, user_id: int):
        result= await crud_user.delete(session, id=user_id)
        return result
  
