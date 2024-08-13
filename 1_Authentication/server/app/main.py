from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from api.router import api_router
from core import redis
from core.config import settings


# async def create_redis_pool():
#     redis.pool = await create_pool(
#         RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
#     )

# async def close_redis_pool():
#     redis.pool.close()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    # application.add_event_handler("startup", create_redis_pool)
    # application.add_event_handler("shutdown", close_redis_pool)
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    application.include_router(api_router , prefix= settings.API_VERSION)
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

