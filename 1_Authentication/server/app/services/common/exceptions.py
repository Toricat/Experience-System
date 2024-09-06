class ServiceResponse(Exception):
    """Base class for service responses."""
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code
        super().__init__(self.message)


class SuccessResponse(ServiceResponse):
    def __init__(self, message="Success", code=200):
        super().__init__(message, code)

class UnauthorizedError(ServiceResponse):
    def __init__(self, message="Unauthorized", code=401):
        super().__init__(message, code)

class ForbiddenError(ServiceResponse):
    def __init__(self, message="Forbidden", code=403):
        super().__init__(message, code)

class NotFoundError(ServiceResponse):
    def __init__(self, message="Not Found", code=404):
        super().__init__(message, code)

class MethodNotAllowedError(ServiceResponse):
    def __init__(self, message="Method Not Allowed", code=405):
        super().__init__(message, code)

class ConflictError(ServiceResponse):
    def __init__(self, message="Conflict", code=409):
        super().__init__(message, code)

class GoneError(ServiceResponse):
    def __init__(self, message="Gone", code=410):
        super().__init__(message, code)

class TooManyRequestsError(ServiceResponse):
    def __init__(self, message="Too Many Requests", code=429):
        super().__init__(message, code)
class AttributeError(ServiceResponse):
    def __init__(self, message="Attribute Error", code=500):
        super().__init__(message, code)
class DatabaseTimeoutError(ServiceResponse):
    def __init__(self, message="Database Timeout", code=504):
        super().__init__(message, code)

class DatabaseConnectionError(ServiceResponse):
    def __init__(self, message="Database Connection Error", code=505):
        super().__init__(message, code)
class BadRequestError(ServiceResponse):
    def __init__(self, message="Bad Request", code=500):
        super().__init__(message, code)

