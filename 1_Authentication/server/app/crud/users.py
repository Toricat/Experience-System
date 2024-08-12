from crud.base import CRUDBase
from models.users import User
from schemas.users import UserInDB, UserUpdateDB

CRUDUser = CRUDBase[User, UserInDB, UserUpdateDB]
crud_user = CRUDUser(User)