from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from utils.error.base import AppError
from utils.logger import logger
import logging


logger = logging.getLogger('api_calls')
async def app_error_handler(request: Request, exc: AppError):
    """
    Handle all exceptions derived from AppError.
    Logs the error and returns a JSON response with the error message and HTTP status code.
    """
    message = exc.get_message()

    logger.error(f"Error occurred: {message} - Path: {request.url} - Status Code: {exc.code}")

    return JSONResponse(
        status_code=exc.code,
        content={
            "message": message,
            "error_type": exc.__class__.__name__
        }
    )

# Handler for validation errors
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors or other input-related exceptions.
    Logs the error and returns a 400 Bad Request response.
    """
    logger.warning(f"Validation error: {exc.errors()} - Path: {request.url}")
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid request", "details": exc.errors()}
    )

# Handler for internal server errors
async def internal_server_error_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions (500 Internal Server Error).
    Logs the error and returns a 500 Internal Server Error response.
    """
    logger.error(f"Internal Server Error: {str(exc)} - Path: {request.url}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error, please try again later."}
    )

def register_error_handlers(app):
    """
    Register all custom error handlers with FastAPI.
    Add more handlers if necessary.
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, internal_server_error_handler)