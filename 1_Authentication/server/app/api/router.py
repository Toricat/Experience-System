from fastapi import APIRouter

from api.v1 import items, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(items.router, tags=["Items"])