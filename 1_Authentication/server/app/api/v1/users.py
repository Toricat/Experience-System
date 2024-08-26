from fastapi import APIRouter, Depends, HTTPException

from api.deps import SessionDep, RoleChecker

from schemas.users import UserCreate, User, UserUpdate
from services.users import UserService

user_service = UserService()

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[User])
async def read_users(
    session: SessionDep, 
    current_user: User = Depends(RoleChecker(["admin", "manager"])),                            
    offset: int = 0,
    limit: int = 100,
):  
    result =  await user_service.get_users_service(session,offset=offset,limit=limit)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result
  


@router.get("/{user_id}/", response_model=User)
async def read_user(
    user_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin", "manager", "user"])),
     
):
    result =  await user_service.get_user_service(session, user_id)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result


@router.post("/", response_model=User)
async def create_user(
    session: SessionDep, 
    user_in: UserCreate, 
    current_user: User = Depends(RoleChecker(["admin"])) 
):
    result = await user_service.create_user_service(session, user_in)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    session: SessionDep,
    user_in: UserUpdate,
    current_user: User = Depends(RoleChecker(["admin", "user"])) 
):
  
    result= await user_service.update_user_service(session, user_id, user_in)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: User = Depends(RoleChecker(["admin"])) 
):
    result= await user_service.delete_user_service(session, user_id)
    if isinstance(result, Exception):
        raise HTTPException(status_code=result.code, detail={"message": result.message, "code": result.code})
    return result