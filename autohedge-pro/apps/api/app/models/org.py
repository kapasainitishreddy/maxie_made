import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
class Org(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orgs"
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    clerk_org_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String, default="pro", nullable=False)
    aum: Mapped[float] = mapped_column(default=0.0, nullable=False)
