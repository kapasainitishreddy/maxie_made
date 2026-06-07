"""Cloud account model (AWS/GCP/Azure)."""
from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class CloudProvider(str, enum.Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class CloudAccount(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "cloud_accounts"

    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    provider: Mapped[CloudProvider] = mapped_column(Enum(CloudProvider, name="cloud_provider"), nullable=False)
    account_id: Mapped[str] = mapped_column(String, nullable=False)
    account_name: Mapped[str] = mapped_column(String, nullable=False)
    role_arn: Mapped[str | None] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, default="us-east-1", nullable=False)
    monthly_cost: Mapped[float] = mapped_column(default=0.0, nullable=False)
    resource_count: Mapped[int] = mapped_column(default=0, nullable=False)
    last_scanned_at: Mapped[str | None] = mapped_column(String, nullable=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
