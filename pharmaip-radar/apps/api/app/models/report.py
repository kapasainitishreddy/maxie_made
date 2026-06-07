"""Generated reports."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class ReportType(str, enum.Enum):
    FTO = "fto"               # Freedom to Operate
    LANDSCAPE = "landscape"
    INFRINGEMENT = "infringement"
    PATENTABILITY = "patentability"


class ReportStatus(str, enum.Enum):
    QUEUED = "queued"
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"


class Report(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reports"

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="CASCADE"),
        nullable=False,
    )
    report_type: Mapped[ReportType] = mapped_column(
        Enum(ReportType, name="report_type"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, name="report_status"),
        default=ReportStatus.QUEUED,
        nullable=False,
    )
    query: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    pdf_path: Mapped[str | None] = mapped_column(String, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
