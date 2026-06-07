"""Errors + config tests."""

from __future__ import annotations

from app.core.errors import AppError, NotFoundError, AuthError, ValidationError, UpstreamError
from app.config import get_settings


def test_app_error_default():
    e = AppError("boom")
    assert e.status_code == 500
    assert e.code == "internal_error"


def test_not_found():
    assert NotFoundError("x").status_code == 404


def test_auth():
    assert AuthError("x").status_code == 401


def test_validation():
    assert ValidationError("x").status_code == 422


def test_upstream():
    assert UpstreamError("x").status_code == 502


def test_app_error_custom_code():
    e = AppError("oops", code="custom")
    assert e.code == "custom"


def test_settings_singleton():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2


def test_settings_default_app_name():
    s = get_settings()
    assert "CloudFinOps" in s.app_name
