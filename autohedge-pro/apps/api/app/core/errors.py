class AppError(Exception):
    status_code: int = 500; code: str = "internal_error"
    def __init__(self, message: str = "", *, code: str | None = None):
        super().__init__(message or self.__class__.__name__)
        self.message = message or self.__class__.__name__
        if code: self.code = code
class NotFoundError(AppError): status_code=404; code="not_found"
class AuthError(AppError): status_code=401; code="unauthorized"
class ValidationError(AppError): status_code=422; code="validation_error"
class ForbiddenError(AppError): status_code=403; code="forbidden"
