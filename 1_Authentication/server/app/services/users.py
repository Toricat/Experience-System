from datetime import datetime
from utils.errors.user import UserNotFoundError
from core.security import get_password_hash
from repositories.users import user_repo
from schemas.users import UserCreate, UserUpdate, UserInDB,UserUpdate

from logging import getLogger
logger = getLogger(__name__)

class UserService:
    def __init__(self):
        self.user_repo = user_repo
    async def get_multi_users_service(self, session, offset: int, limit: int):
        result =  await self.user_repo.get_all( session=session, offset=offset, limit=limit)
        if not result:
            raise UserNotFoundError()
        return  result 

    async def get_user_service(self, session, user_id: int):
        result = await self.user_repo.get(session=session,filters ={"id": user_id})
        return  result
    
    async def create_user_service(self, session, user_in: UserCreate):
        user_create = UserInDB(
            **user_in.model_dump(),
            hashed_password=get_password_hash(user_in.password),
            created_at=datetime.now()  
        )
        result = await self.user_repo.create(session=session, data=user_create.model_dump())
        return result

    async def update_user_service(self, session, user_id: int, user_in: UserUpdate):
        user_update = UserUpdate(
            **user_in.model_dump(exclude_unset=True, exclude_none=True),
        )
        if user_in.password:
            user_update["hashed_password"] = get_password_hash(user_in.password)
        result = await self.user_repo.update(session, filters={"id": user_id}, data=user_update.model_dump())  
        return result

    async def delete_user_service(self, session, user_id: int):
        result= await self.user_repo.delete(session, filters={"id": user_id})
        if not result:
            return UserNotFoundError()
        return {"message": "Delete success"}
        
      
  
