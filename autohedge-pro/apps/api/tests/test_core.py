from app.core.errors import AppError, NotFoundError, AuthError, ValidationError
from app.config import get_settings

def test_app_error_default():
    e = AppError("x"); assert e.status_code == 500
def test_not_found():
    e = NotFoundError("x"); assert e.status_code == 404
def test_auth():
    e = AuthError("x"); assert e.status_code == 401
def test_validation():
    e = ValidationError("x"); assert e.status_code == 422
def test_settings_singleton():
    assert get_settings() is get_settings()
def test_app_name():
    assert "AutoHedge" in get_settings().app_name
