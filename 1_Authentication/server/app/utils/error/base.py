class AppError(Exception):
    """
    Base class for all application-specific errors.
    Supports multi-language messages.
    """
    def __init__(self, key: str, language: str = "en", code: int = 400):
        self.key = key  
        self.language = language 
        self.code = code  
        super().__init__(key)

    def get_message(self):
        """
        Translate error message to the specified language.
        """
        from utils.translation import translate
        return translate(self.key, self.language)

class BadRequestError(AppError):
    """
    Represents a generic 400 Bad Request error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 400)  # HTTP 400 Bad Request


class UnauthorizedError(AppError):
    """
    Represents a 401 Unauthorized error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 401)  # HTTP 401 Unauthorized


class ForbiddenError(AppError):
    """
    Represents a 403 Forbidden error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 403)  # HTTP 403 Forbidden


class NotFoundError(AppError):
    """
    Represents a 404 Not Found error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 404)  # HTTP 404 Not Found


class ConflictError(AppError):
    """
    Represents a 409 Conflict error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 409)  # HTTP 409 Conflict


class GoneError(AppError):
    """
    Represents a 410 Gone error.
    """
    def __init__(self, key: str, language: str = "en"):
        super().__init__(key, language, 410)  # HTTP 410 Gone



