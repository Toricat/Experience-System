from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError, SQLAlchemyError
from sqlalchemy.orm.exc import UnmappedInstanceError, UnmappedColumnError, UnmappedClassError,DetachedInstanceError,UnmappedError
from .exceptions import (
    ServiceResponse,
    NotFoundError, 
    ConflictError, 
    TooManyRequestsError,
    ForbiddenError,
    UnauthorizedError,
    BadRequestError,
    AttributeError,)

def handle_error(func):
    
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            if result is None:
                return NotFoundError("Resource not found or does not exist.")
            return result
        except (NoResultFound,
                UnmappedInstanceError,   
                DetachedInstanceError,   
                UnmappedClassError,     
                UnmappedColumnError,     
                UnmappedError):
            return NotFoundError("Resource not found or does not exist.")
        except IntegrityError as e:
            if "foreign key constraint" in str(e).lower():
                return ConflictError("Related resource does not exist or violates foreign key constraints.")
            if "duplicate entry" in str(e).lower() or "unique constraint" in str(e).lower():
                return ConflictError("Resource already exists.")
            return ConflictError("Data integrity violation.")
        except OperationalError:
            return TooManyRequestsError("Database resource constraints. Please try again later.")
        except ForbiddenError:
            return ForbiddenError("Permission denied.")
        except UnauthorizedError:
            return UnauthorizedError("Unauthorized access.")
        except BadRequestError:
            return BadRequestError("Bad request.")
        except SQLAlchemyError:
            return ServiceResponse("Database error.",code=500)
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                return NotFoundError("Resource not found or does not exist.")
            return ServiceResponse("Attribute error.")
        except Exception as e:
            if "'NoneType' object has no attribute" in str(e):
                return NotFoundError("Resource not found or does not exist.")
            return BadRequestError(f"An unexpected error occurred: {str(e)}")
    return wrapper