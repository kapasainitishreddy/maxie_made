"""Stablecoin master record (USDC, USDT, DAI, FRAX, ...)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import TimestampMixin, UUIDMixin


class Stablecoin(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stablecoins"

    symbol: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    issuer: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(32), default="fiat-backed", nullable=False)
    # fiat-backed | crypto-backed | algorithmic | commodity-backed
    peg_currency: Mapped[str] = mapped_column(String(8), default="USD", nullable=False)
    chain: Mapped[str] = mapped_column(String(32), default="ethereum", nullable=False)
    contract_address: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Market data snapshot (refreshed periodically)
    market_cap_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    circulating_supply: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tier: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # 1 = free tier visible | 2 = pro tier | 3 = api tier

    # Relationships
    snapshots: Mapped[list["PegSnapshot"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="stablecoin",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="stablecoin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Stablecoin {self.symbol} ({self.issuer})>"
