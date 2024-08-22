from .common.exceptions import (
    NotFoundError, 
    UnauthorizedError, 
    ConflictError, 
    ForbiddenError,
    TooManyRequestsError,
)


from core.security import get_password_hash
from crud.users import crud_user
from schemas.users import UserCreate, UserUpdate, UserInDB

class UserService:

    async def read_users(self, session, offset: int, limit: int):
        return await crud_user.get_multi(session, offset=offset, limit=limit)

    async def get_user(self, session, user_id: int, current_user):
        user = await crud_user.get(session, id=user_id)
        if not user:
           return NotFoundError("User not found")
        
      
        
        return user

    async def create_user(self, session, user_in: UserCreate):
        user = await crud_user.get(session, email=user_in.email)
        if user:
           return ConflictError("A user with this email already exists")
        
        obj_in = UserInDB(
            **user_in.dict(),
            hashed_password= get_password_hash(user_in.password),
        )
        return await crud_user.create(session, obj_in)

    async def update_user(self, session, user_id: int, user_in: UserUpdate, current_user):
        user = await self.get_user(session, user_id, current_user)
        if not user:
           return NotFoundError("User not found")
        
      
        
        update_data = user_in.dict(exclude={"password"}, exclude_none=True)
        if user_in.password:
            update_data["hashed_password"] = get_password_hash(user_in.password),
        
        await crud_user.update(session, db_obj=user, obj_in=update_data)

        return {"msg": "User updated"}

    async def delete_user(self, session, user_id: int, current_user):
        user = await self.get_user(session, user_id, current_user)
        if not user:
           return NotFoundError("User not found")
       
        
        await crud_user.delete(session, db_obj=user)

        return {"msg": "User deleted"}
