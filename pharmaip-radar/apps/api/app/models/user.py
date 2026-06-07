"""User model — mirrors Clerk."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    clerk_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    default_org_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="SET NULL"),
        nullable=True,
    )

    default_org: Mapped["Org | None"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Org",
        foreign_keys=[default_org_id],
    )
    memberships: Mapped[list["OrgMember"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "OrgMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
