"""Pagination helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)


@dataclass
class Page(BaseModel, Generic[T]):  # type: ignore[generic-class]
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
