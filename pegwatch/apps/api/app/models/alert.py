"""Alert rules and incident log."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, UUIDMixin


class Alert(Base, UUIDMixin, TimestampMixin):
    """A triggered depeg event (incident)."""

    __tablename__ = "alerts"

    stablecoin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("stablecoins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    triggered_at: Mapped[datetime] = mapped_column(
        # ISO string for SQLite portability
        String(32),
        nullable=False,
        index=True,
    )
    severity: Mapped[str] = mapped_column(String(16), default="warning", nullable=False)
    # info | warning | critical

    price_at_trigger: Mapped[float] = mapped_column(Float, nullable=False)
    deviation_pct: Mapped[float] = mapped_column(Float, nullable=False)
    z_score: Mapped[float] = mapped_column(Float, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(String(32), nullable=True)
    notification_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    stablecoin: Mapped["Stablecoin"] = relationship(back_populates="alerts")  # type: ignore[name-defined]  # noqa: F821

    def __repr__(self) -> str:
        return f"<Alert {self.title} @ {self.triggered_at} ({self.severity})>"


class AlertChannel(Base, UUIDMixin, TimestampMixin):
    """A user's notification channel (Telegram, Discord, webhook, email)."""

    __tablename__ = "alert_channels"

    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    channel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    # telegram | discord | webhook | email
    target: Mapped[str] = mapped_column(String(512), nullable=False)
    # chat_id, webhook URL, email, etc.

    min_severity: Mapped[str] = mapped_column(String(16), default="warning", nullable=False)
    min_deviation_pct: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    watched_symbols: Mapped[str] = mapped_column(
        String(512), default="USDC,USDT,DAI", nullable=False
    )
    # Comma-separated list of stablecoin symbols. Empty/blank = watch all.

    def __repr__(self) -> str:
        return f"<AlertChannel {self.channel_type}→{self.target[:30]}>"
