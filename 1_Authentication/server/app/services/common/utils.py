from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError, SQLAlchemyError
from .exceptions import (
    ServiceError,
    NotFoundError, 
    ConflictError, 
    TooManyRequestsError,
    ForbiddenError,
    UnauthorizedError,
    BadRequestError
)

def handle_db_errors(func):
    """Decorator để xử lý lỗi cơ sở dữ liệu và trả về phản hồi thích hợp cho mọi dịch vụ."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="The requested resource could not be found.")
        except IntegrityError as e:
            if "foreign key constraint" in str(e).lower():
                raise HTTPException(status_code=409, detail="A related resource does not exist or violates foreign key constraints.")
            raise HTTPException(status_code=409, detail="The resource already exists or violates data integrity constraints.")
        except OperationalError:
            raise HTTPException(status_code=429, detail="The database operation failed due to resource constraints. Please try again later.")
        except ForbiddenError:
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
        except UnauthorizedError:
            raise HTTPException(status_code=401, detail="Unauthorized access. Please check your credentials.")
        except BadRequestError as e:
            raise HTTPException(status_code=400, detail=f"Bad request: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return wrapper
