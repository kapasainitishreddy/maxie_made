"""A peg deviation snapshot at a point in time, sourced from one or more venues."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, UUIDMixin


class PegSnapshot(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "peg_snapshots"
    __table_args__ = (
        Index("ix_peg_snapshots_symbol_ts", "stablecoin_id", "observed_at"),
    )

    stablecoin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("stablecoins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    observed_at: Mapped[datetime] = mapped_column(
        # Stored as ISO string for SQLite portability; parsed in service layer.
        # In Postgres prod, swap to TIMESTAMPTZ.
        String(32),
        nullable=False,
        index=True,
    )

    # Price data (medians across sources)
    price_usd: Mapped[float] = mapped_column(Float, nullable=False)
    deviation_pct: Mapped[float] = mapped_column(Float, nullable=False)
    # ((price - 1.0) / 1.0) * 100

    # Source breakdown
    curve_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    uniswap_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    cex_median_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    sources_count: Mapped[int] = mapped_column(Float, default=0, nullable=False)

    # Liquidity depth
    liquidity_depth_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # Sum of stable liquidity within ±0.5% of peg, in USD

    # Z-score vs 7-day rolling mean
    z_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    stablecoin: Mapped["Stablecoin"] = relationship(back_populates="snapshots")  # type: ignore[name-defined]  # noqa: F821

    def __repr__(self) -> str:
        return f"<PegSnapshot {self.stablecoin_id} @ {self.observed_at} ${self.price_usd:.4f}>"
