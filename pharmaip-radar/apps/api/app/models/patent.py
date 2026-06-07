"""Patent + claims + family models."""

from __future__ import annotations

import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class PatentStatus(str, enum.Enum):
    PENDING = "pending"
    GRANTED = "granted"
    EXPIRED = "expired"
    ABANDONED = "abandoned"
    WITHDRAWN = "withdrawn"


class Patent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "patents"
    __table_args__ = (
        Index("ix_patent_number_jurisdiction", "patent_number", "jurisdiction"),
    )

    org_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="CASCADE"),
        nullable=True,
    )

    patent_number: Mapped[str] = mapped_column(String, index=True, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String, nullable=False)  # US, EP, WO, JP, etc.
    title: Mapped[str] = mapped_column(String, nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignee: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    inventors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    ipc_classes: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    filing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    grant_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[PatentStatus] = mapped_column(
        Enum(PatentStatus, name="patent_status"),
        default=PatentStatus.PENDING,
        nullable=False,
    )
    therapeutic_area: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    drug_name: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    family_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patent_families.id", ondelete="SET NULL"),
        nullable=True,
    )

    claims: Mapped[list["PatentClaim"]] = relationship(
        "PatentClaim",
        back_populates="patent",
        cascade="all, delete-orphan",
    )
    family: Mapped["PatentFamily | None"] = relationship(  # type: ignore[name-defined]
        "PatentFamily",
        back_populates="patents",
    )


class PatentClaim(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "patent_claims"

    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        nullable=False,
    )
    claim_number: Mapped[int] = mapped_column(Integer, nullable=False)
    claim_type: Mapped[str] = mapped_column(String, default="independent", nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_independent: Mapped[bool] = mapped_column(default=True, nullable=False)
    depends_on: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    patent: Mapped["Patent"] = relationship("Patent", back_populates="claims")


class PatentFamily(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "patent_families"

    family_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    title: Mapped[str | None] = mapped_column(String, nullable=True)

    patents: Mapped[list["Patent"]] = relationship("Patent", back_populates="family")
