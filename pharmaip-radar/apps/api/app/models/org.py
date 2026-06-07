"""Organization + membership."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class OrgRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class Org(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orgs"

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    clerk_org_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    stripe_customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String, default="starter", nullable=False)
    subscription_status: Mapped[str] = mapped_column(String, default="trialing", nullable=False)

    members: Mapped[list["OrgMember"]] = relationship(
        "OrgMember",
        back_populates="org",
        cascade="all, delete-orphan",
    )


class OrgMember(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "org_members"
    __table_args__ = (UniqueConstraint("org_id", "user_id", name="uq_org_user"),)

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orgs.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[OrgRole] = mapped_column(
        Enum(OrgRole, name="org_role"),
        default=OrgRole.MEMBER,
        nullable=False,
    )

    org: Mapped["Org"] = relationship("Org", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="memberships")
