"""Verified savings ledger."""
from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Savings(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "savings"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cloud_accounts.id", ondelete="CASCADE"), nullable=False
    )
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    service: Mapped[str] = mapped_column(String, nullable=False)
    raw_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    baseline_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    verified_savings: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String, default="USD", nullable=False)
