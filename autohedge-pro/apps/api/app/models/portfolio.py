import uuid
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
class Portfolio(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "portfolios"
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String, default="Main", nullable=False)
    cash: Mapped[float] = mapped_column(Float, default=100000.0, nullable=False)
    total_value: Mapped[float] = mapped_column(Float, default=100000.0, nullable=False)
    mode: Mapped[str] = mapped_column(String, default="paper", nullable=False)  # paper | live
class Position(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "positions"
    portfolio_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    avg_entry: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    unrealized_pnl: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    side: Mapped[str] = mapped_column(String, default="long", nullable=False)
