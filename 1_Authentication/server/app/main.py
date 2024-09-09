import time
from typing import Awaitable, Callable

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI,Request, Response
from fastapi.routing import APIRoute

import logging

from api.router import api_router
from core import redis
from core.config import settings

from utils.logger import logger
from middlewares.error_handlers import  register_error_handlers
from middlewares.middle_ware import register_middleware


description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """
 
def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

# async def create_redis_pool():
#     redis.pool = await create_pool(
#         RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
#     )

# async def close_redis_pool():
#     redis.pool.close()

def create_application() -> FastAPI:
    application = FastAPI(title=settings.APP_NAME,
                        generate_unique_id_function=custom_generate_unique_id,
                        description=description,
                        version=settings.APP_VERSION,
                        license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
                        contact={
                            "name": "Ssali Jonathan",
                            "url": "https://github.com/jod35",
                            "email": "ssalijonathank@gmail.com",
                        },
                        terms_of_service="httpS://example.com/tos",
                        openapi_url=f"{settings.API_VERSION}/openapi.json",
                        docs_url=f"{settings.API_VERSION}/docs",
                        redoc_url=f"{settings.API_VERSION}/redoc"
                        )

    register_error_handlers(application)
    register_middleware(application)
    
    # application.add_event_handler("startup", create_redis_pool)
    # application.add_event_handler("shutdown", close_redis_pool)

    application.include_router(api_router , prefix= settings.API_VERSION)

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    logger.info("Environment: " + settings.ENVIRONMENT) 
    logger.info("Starting server...")
    logger.info(f"Server run at: {settings.server_host}")
    uvicorn.run("main:app", host=settings.DOMAIN, port=settings.DOMAIN_HOST, reload=settings.RELOAD)


