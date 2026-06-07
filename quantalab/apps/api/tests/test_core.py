from app.core.errors import AppError, NotFoundError, ValidationError
def test_app_error(): assert AppError("x").status_code == 500
def test_not_found(): assert NotFoundError("x").status_code == 404
def test_validation(): assert ValidationError("x").status_code == 422
