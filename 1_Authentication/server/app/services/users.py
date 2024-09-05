from datetime import datetime
from .common.exceptions import (
    SuccessResponse,
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
)

from .common.handle import handle_error

from core.security import get_password_hash
from crud.users import crud_user
from schemas.users import UserCreate, UserUpdate, UserInDB,UserUpdate

class UserService:
    def __init__(self):
        pass
    @handle_error
    async def get_users_service(self, session, offset: int, limit: int,kwargs):
        result =  await crud_user.get_multi(session, offset=offset, limit=limit,**kwargs )
        return  result 

    @handle_error
    async def get_user_service(self, session, user_id: int,kwargs):
        result = await crud_user.get(session, id=user_id,**kwargs )
        return  result
    
    @handle_error
    async def create_user_service(self, session, user_in: UserCreate,kwargs):
        obj_in = UserInDB(
            **user_in.dict(),
            hashed_password=get_password_hash(user_in.password),
            created_at=datetime.utcnow(),    
        )
        result = await crud_user.create(session, obj_in,**kwargs)
        return result

    @handle_error
    async def update_user_service(self, session, user_id: int, user_in: UserUpdate,kwargs):
        obj_in = UserUpdate(
            **user_in.dict(exclude_unset=True, exclude_none=True),
        )
        if user_in.password:
            obj_in["hashed_password"] = get_password_hash(user_in.password)
        result = await crud_user.update(session, id=user_id, obj_in= obj_in,**kwargs )
        return result

    @handle_error
    async def delete_user_service(self, session, user_id: int,kwargs):
        print(kwargs)
        result= await crud_user.delete(session, id=user_id,**kwargs )
        if not result:
            return NotFoundError("Resource not found or does not exist.")
        return SuccessResponse("Delete success")
        
      
  
