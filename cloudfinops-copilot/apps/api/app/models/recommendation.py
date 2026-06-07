"""Recommendation model (rightsizing, idle, etc.)."""
from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class RecommendationType(str, enum.Enum):
    RIGHTSIZE = "rightsize"
    TERMINATE_IDLE = "terminate_idle"
    SCHEDULE = "schedule"          # stop/start non-prod
    RESERVED_INSTANCE = "reserved_instance"
    STORAGE_CLASS = "storage_class"
    graviton = "graviton"          # ARM migration


class RecommendationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    FAILED = "failed"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recommendation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "recommendations"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cloud_accounts.id", ondelete="CASCADE"), nullable=False
    )
    resource_id: Mapped[str] = mapped_column(String, nullable=False)
    resource_type: Mapped[str] = mapped_column(String, nullable=False)
    rec_type: Mapped[RecommendationType] = mapped_column(Enum(RecommendationType, name="rec_type"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    current_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    projected_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    monthly_savings: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel, name="risk_level"), default=RiskLevel.MEDIUM, nullable=False)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, name="rec_status"), default=RecommendationStatus.PENDING, nullable=False
    )
    terraform_hcl: Mapped[str] = mapped_column(Text, default="", nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
