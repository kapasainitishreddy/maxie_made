"""Error handling + pagination tests."""

from __future__ import annotations

import pytest

from app.core.errors import (
    AppError,
    NotFoundError,
    AuthError,
    ForbiddenError,
    ValidationError,
    ConflictError,
    UpstreamError,
)
from app.schemas.common import PageResponse


def test_app_error_default_status():
    e = AppError("boom")
    assert e.status_code == 500
    assert e.code == "internal_error"
    assert e.message == "boom"


def test_not_found_error():
    e = NotFoundError("user 42")
    assert e.status_code == 404
    assert e.code == "not_found"


def test_auth_error():
    e = AuthError("bad token")
    assert e.status_code == 401
    assert e.code == "unauthorized"


def test_forbidden_error():
    e = ForbiddenError()
    assert e.status_code == 403


def test_validation_error():
    e = ValidationError("bad input")
    assert e.status_code == 422


def test_conflict_error():
    e = ConflictError("dup")
    assert e.status_code == 409


def test_upstream_error():
    e = UpstreamError("stripe down")
    assert e.status_code == 502


def test_app_error_custom_code():
    e = AppError("oops", code="custom_thing")
    assert e.code == "custom_thing"


def test_page_response_empty():
    p = PageResponse.build([], total=0)
    assert p.total == 0
    assert p.total_pages == 1
    assert p.items == []


def test_page_response_exact_multiple():
    p = PageResponse.build([1, 2, 3, 4], total=4, page=1, page_size=2)
    assert p.total_pages == 2
    assert p.page == 1


def test_page_response_partial_last_page():
    p = PageResponse.build([1], total=21, page=3, page_size=10)
    assert p.total_pages == 3
    assert p.page == 3
