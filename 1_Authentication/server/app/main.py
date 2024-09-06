import time

from arq import create_pool
from arq.connections import RedisSettings
from fastapi.exceptions import HTTPException
from fastapi import FastAPI
from fastapi.routing import APIRoute

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

from api.router import api_router
from core import redis
from core.config import settings

from logger import logger  

logger.info("Environment: " + settings.ENVIRONMENT) 

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request: {request.method} {request.url} - Processed in {process_time:.2f}s - Status: {response.status_code}")
        return response

        
    
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
                          generate_unique_id_function=custom_generate_unique_id)
    logger.info("Starting application...") 
    # application.add_event_handler("startup", create_redis_pool)
    # application.add_event_handler("shutdown", close_redis_pool)

    application.add_middleware(LoggingMiddleware)

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

    application.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        session_cookie="session", 
        same_site="lax"
    )
    application.include_router(api_router , prefix= settings.API_VERSION)
    logger.info("Application setup complete.")

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    logger.info(f"Server run at: {settings.server_host}")
    uvicorn.run("main:app", host=settings.DOMAIN, port=settings.DOMAIN_HOST, reload=settings.RELOAD)


