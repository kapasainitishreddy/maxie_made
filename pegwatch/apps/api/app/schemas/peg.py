"""Peg snapshot schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PegSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    stablecoin_id: str
    observed_at: datetime
    price_usd: float
    deviation_pct: float
    curve_price: float | None = None
    uniswap_price: float | None = None
    cex_median_price: float | None = None
    sources_count: int = 0
    liquidity_depth_pct: float = 0.0
    z_score: float = 0.0


class PegStatus(BaseModel):
    """Current peg status for a stablecoin - the dashboard's primary read."""

    symbol: str
    name: str
    issuer: str
    price_usd: float
    deviation_pct: float
    z_score: float
    liquidity_depth_usd: float
    severity: str  # healthy | watch | warning | critical
    last_updated: datetime
    market_cap_usd: float = 0.0
    sources_count: int = 0


class PegHistoryPoint(BaseModel):
    observed_at: datetime
    price_usd: float
    deviation_pct: float
    z_score: float = 0.0


class PegHistoryResponse(BaseModel):
    symbol: str
    points: list[PegHistoryPoint]
    mean_7d: float
    stddev_7d: float
