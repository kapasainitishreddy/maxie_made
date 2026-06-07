import uuid
from sqlalchemy import Float, ForeignKey, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin, UUIDMixin
class Backtest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "backtests"
    strategy_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False)
    asset: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[str] = mapped_column(String, nullable=False)
    end_date: Mapped[str] = mapped_column(String, nullable=False)
    initial_capital: Mapped[float] = mapped_column(Float, default=100000.0, nullable=False)
    final_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sharpe: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sortino: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    max_drawdown: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_return: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    num_trades: Mapped[int] = mapped_column(default=0, nullable=False)
    equity_curve: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    trades: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String, default="completed", nullable=False)
