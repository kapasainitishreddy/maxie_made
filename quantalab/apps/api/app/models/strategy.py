import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
class Strategy(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "strategies"
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="", nullable=False)
    author: Mapped[str] = mapped_column(String, default="anonymous", nullable=False)
    code: Mapped[str] = mapped_column(String, default="", nullable=False)
    price_cents: Mapped[int] = mapped_column(default=0, nullable=False)
    downloads: Mapped[int] = mapped_column(default=0, nullable=False)
    rating: Mapped[float] = mapped_column(default=0.0, nullable=False)
