# utils/error/verify.py

from utils.errors.base import UnauthorizedError, ConflictError,NotFoundError

# ======================
# Activate Code Errors
# ======================
class ActivateCodeNotFoundError(NotFoundError):
    """
    Raised when the activation code is not found.
    """
    def __init__(self, language: str = "en"):
        super().__init__("activate_code_not_found", language)


class ActivateCodeExpiredError(UnauthorizedError):
    """
    Raised when the activation code has expired.
    """
    def __init__(self, language: str = "en"):
        super().__init__("activate_code_expired", language)


class ActivateCodeAlreadyUsedError(ConflictError):
    """
    Raised when the activation code has already been used.
    """
    def __init__(self, language: str = "en"):
        super().__init__("activate_code_already_used", language)


# ======================
# Recovery Code Errors
# ======================
class RecoveryCodeNotFoundError(NotFoundError):
    """
    Raised when the recovery code is not found.
    """
    def __init__(self, language: str = "en"):
        super().__init__("recovery_code_not_found", language)


class RecoveryCodeExpiredError(UnauthorizedError):
    """
    Raised when the recovery code has expired.
    """
    def __init__(self, language: str = "en"):
        super().__init__("recovery_code_expired", language)


class RecoveryCodeAlreadyUsedError(ConflictError):
    """
    Raised when the recovery code has already been used.
    """
    def __init__(self, language: str = "en"):
        super().__init__("recovery_code_already_used", language)
