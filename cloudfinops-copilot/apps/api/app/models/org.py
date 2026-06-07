"""Org model."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Org(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orgs"
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    clerk_org_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    stripe_customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String, default="audit", nullable=False)
    savings_share_pct: Mapped[float] = mapped_column(default=20.0, nullable=False)
