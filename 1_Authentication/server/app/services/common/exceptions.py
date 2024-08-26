class ServiceError(Exception):
    """Base class for service errors."""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class BadRequestError(ServiceError):
    def __init__(self, message="Bad Request", code=400):
        super().__init__(message, code)

class UnauthorizedError(ServiceError):
    def __init__(self, message="Unauthorized", code=401):
        super().__init__(message, code)

class ForbiddenError(ServiceError):
    def __init__(self, message="Forbidden", code=403):
        super().__init__(message, code)

class NotFoundError(ServiceError):
    def __init__(self, message="Not Found", code=404):
        super().__init__(message, code)

class MethodNotAllowedError(ServiceError):
    def __init__(self, message="Method Not Allowed", code=405):
        super().__init__(message, code)

class ConflictError(ServiceError):
    def __init__(self, message="Conflict", code=409):
        super().__init__(message, code)

class GoneError(ServiceError):
    def __init__(self, message="Gone", code=410):
        super().__init__(message, code)

class TooManyRequestsError(ServiceError):
    def __init__(self, message="Too Many Requests", code=429):
        super().__init__(message, code)
class AttributeError(ServiceError):
    def __init__(self, message="Attribute Error", code=500):
        super().__init__(message, code)
class DatabaseTimeoutError(ServiceError):
    def __init__(self, message="Database Timeout", code=504):
        super().__init__(message, code)

class DatabaseConnectionError(ServiceError):
    def __init__(self, message="Database Connection Error", code=505):
        super().__init__(message, code)

