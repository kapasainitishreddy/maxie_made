"""Common schemas."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str
    version: str
    env: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict | None = None


class PageResponse(BaseModel, Generic[T]):  # type: ignore[generic-class]
    items: list[T]
    total: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)
    total_pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int = 1, page_size: int = 25) -> "PageResponse[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=max(1, (total + page_size - 1) // page_size),
        )
