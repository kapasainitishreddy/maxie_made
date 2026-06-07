"""Typed application errors with HTTP status codes."""
from fastapi import HTTPException, status


class AppError(HTTPException):
    """Base error for application-level issues."""

    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.detail = detail


class NotFoundError(AppError):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class AuthError(AppError):
    def __init__(self, detail: str = "Authentication required") -> None:
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
    def __init__(self, detail: str = "Access denied") -> None:
        super().__init__(detail, status.HTTP_403_FORBIDDEN)


class ValidationError(AppError):
    def __init__(self, detail: str = "Invalid input") -> None:
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)


class RateLimitError(AppError):
    def __init__(self, detail: str = "Rate limit exceeded") -> None:
        super().__init__(detail, status.HTTP_429_TOO_MANY_REQUESTS)


class PlanLimitError(AppError):
    """Raised when user tries to use a feature above their subscription tier."""

    def __init__(self, detail: str = "Plan limit reached. Please upgrade.") -> None:
        super().__init__(detail, status.HTTP_402_PAYMENT_REQUIRED)
