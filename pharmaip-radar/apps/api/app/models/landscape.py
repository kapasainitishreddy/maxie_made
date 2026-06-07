"""Landscape models — saved patent landscapes."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Landscape(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "landscapes"

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    query: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    summary: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)

    patents: Mapped[list["LandscapePatent"]] = relationship(
        "LandscapePatent",
        back_populates="landscape",
        cascade="all, delete-orphan",
    )


class LandscapePatent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "landscape_patents"

    landscape_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("landscapes.id", ondelete="CASCADE"),
        nullable=False,
    )
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        nullable=False,
    )
    relevance_score: Mapped[float] = mapped_column(default=0.0, nullable=False)
    cluster_label: Mapped[str | None] = mapped_column(String, nullable=True)

    landscape: Mapped["Landscape"] = relationship("Landscape", back_populates="patents")
