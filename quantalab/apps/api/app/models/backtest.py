import uuid
from sqlalchemy import Float, ForeignKey, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
class Backtest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "backtests"
    notebook_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("notebooks.id", ondelete="SET NULL"), nullable=True)
    strategy_name: Mapped[str] = mapped_column(String, nullable=False)
    asset: Mapped[str] = mapped_column(String, nullable=False)
    sharpe: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sortino: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    max_drawdown: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_return: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    equity_curve: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
