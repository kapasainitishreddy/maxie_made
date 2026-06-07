"""Watchlist + infringement alerts."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    NEW = "new"
    REVIEWED = "reviewed"
    DISMISSED = "dismissed"
    ESCALATED = "escalated"


class Watchlist(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "watchlists"

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_company: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    target_drug: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    keywords: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    patent_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    alerts: Mapped[list["InfringementAlert"]] = relationship(
        "InfringementAlert",
        back_populates="watchlist",
        cascade="all, delete-orphan",
    )


class InfringementAlert(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "infringement_alerts"

    watchlist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("watchlists.id", ondelete="CASCADE"),
        nullable=False,
    )
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        nullable=False,
    )
    matched_patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        nullable=False,
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity, name="alert_severity"),
        default=AlertSeverity.MEDIUM,
        nullable=False,
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, name="alert_status"),
        default=AlertStatus.NEW,
        nullable=False,
    )
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    claim_chart: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    watchlist: Mapped["Watchlist"] = relationship("Watchlist", back_populates="alerts")
