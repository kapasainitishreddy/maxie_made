"""Peg deviation statistics - the core of PegWatch.

We compute the *median* of available price sources per snapshot, then a
z-score against a rolling 7-day window. The z-score is what triggers alerts.
"""
from __future__ import annotations

import math
import statistics
from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.peg_snapshot import PegSnapshot
from app.models.stablecoin import Stablecoin

# Default thresholds (in % deviation and z-score)
WATCH_DEVIATION_PCT = 0.10       # 0.10% off peg -> "watch"
WARNING_DEVIATION_PCT = 0.30     # 0.30% off peg -> "warning"
CRITICAL_DEVIATION_PCT = 1.00    # 1.00% off peg -> "critical"

WATCH_Z = 1.5
WARNING_Z = 2.0
CRITICAL_Z = 3.0

ROLLING_WINDOW_HOURS = 24 * 7  # 7 days


def median_price(prices: Iterable[float]) -> float:
    """Median of non-null prices. Returns 1.0 if all are missing."""
    cleaned = [p for p in prices if p is not None and p > 0]
    if not cleaned:
        return 1.0
    return float(statistics.median(cleaned))


def deviation_pct(price: float, peg: float = 1.0) -> float:
    """Percent deviation from peg. Negative = below peg."""
    if peg == 0:
        return 0.0
    return ((price - peg) / peg) * 100.0


def severity_from_z(z: float, dev_pct: float) -> str:
    """Classify the peg state from z-score AND deviation. Both must agree.

    - healthy: |z| < 1.5 AND |dev| < 0.10%
    - watch:   |z| >= 1.5 OR |dev| >= 0.10%
    - warning: |z| >= 2.0 OR |dev| >= 0.30%
    - critical: |z| >= 3.0 OR |dev| >= 1.00%
    """
    abs_z = abs(z)
    abs_dev = abs(dev_pct)
    if abs_z >= CRITICAL_Z or abs_dev >= CRITICAL_DEVIATION_PCT:
        return "critical"
    if abs_z >= WARNING_Z or abs_dev >= WARNING_DEVIATION_PCT:
        return "warning"
    if abs_z >= WATCH_Z or abs_dev >= WATCH_DEVIATION_PCT:
        return "watch"
    return "healthy"


def rolling_stats(prices: list[float]) -> tuple[float, float]:
    """Mean and stddev of a list of prices. Returns (1.0, 0.0) on empty input."""
    if len(prices) < 2:
        return 1.0, 0.0
    mean = statistics.mean(prices)
    stddev = statistics.stdev(prices) if len(prices) > 1 else 0.0
    return mean, stddev


def z_score_of(value: float, mean: float, stddev: float) -> float:
    """Standard z-score. Returns 0.0 if stddev is 0 (no volatility)."""
    if stddev <= 0:
        return 0.0
    return (value - mean) / stddev


class PegEngine:
    """Compute and persist peg snapshots, with z-score-based alerts."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_recent_prices(self, stablecoin_id: str, hours: int = ROLLING_WINDOW_HOURS) -> list[float]:
        """Pull recent prices for z-score baseline."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        result = await self.db.execute(
            select(PegSnapshot.price_usd)
            .where(PegSnapshot.stablecoin_id == stablecoin_id)
            .where(PegSnapshot.observed_at >= cutoff.isoformat())
            .order_by(PegSnapshot.observed_at)
        )
        return [float(r[0]) for r in result.all()]

    async def record_snapshot(
        self,
        stablecoin_id: str,
        curve_price: float | None,
        uniswap_price: float | None,
        cex_median_price: float | None,
        liquidity_depth_usd: float = 0.0,
    ) -> PegSnapshot:
        """Take a new measurement, compute z-score, persist."""
        prices = [p for p in (curve_price, uniswap_price, cex_median_price) if p is not None]
        if not prices:
            raise ValueError("At least one price source is required")
        price_usd = median_price(prices)
        dev_pct = deviation_pct(price_usd)

        recent = await self.get_recent_prices(stablecoin_id)
        baseline = recent + [price_usd]
        mean, stddev = rolling_stats(baseline)
        z = z_score_of(price_usd, mean, stddev)

        snap = PegSnapshot(
            stablecoin_id=stablecoin_id,
            observed_at=datetime.now(timezone.utc).isoformat(),
            price_usd=price_usd,
            deviation_pct=dev_pct,
            curve_price=curve_price,
            uniswap_price=uniswap_price,
            cex_median_price=cex_median_price,
            sources_count=len(prices),
            liquidity_depth_pct=liquidity_depth_usd,
            z_score=z,
        )
        self.db.add(snap)
        await self.db.commit()
        await self.db.refresh(snap)
        return snap

    async def current_status(self, symbol: str) -> dict:
        """Build a dashboard-ready peg status for one stablecoin."""
        result = await self.db.execute(select(Stablecoin).where(Stablecoin.symbol == symbol))
        coin = result.scalar_one_or_none()
        if not coin:
            from app.core.errors import NotFoundError
            raise NotFoundError(f"Stablecoin {symbol} not found")

        latest = await self.db.execute(
            select(PegSnapshot)
            .where(PegSnapshot.stablecoin_id == coin.id)
            .order_by(PegSnapshot.observed_at.desc())
            .limit(1)
        )
        snap = latest.scalar_one_or_none()
        if not snap:
            # No data yet — report healthy at $1
            return {
                "symbol": coin.symbol,
                "name": coin.name,
                "issuer": coin.issuer,
                "price_usd": 1.0,
                "deviation_pct": 0.0,
                "z_score": 0.0,
                "liquidity_depth_usd": 0.0,
                "severity": "healthy",
                "last_updated": datetime.now(timezone.utc),
                "market_cap_usd": coin.market_cap_usd,
                "sources_count": 0,
            }
        severity = severity_from_z(snap.z_score, snap.deviation_pct)
        return {
            "symbol": coin.symbol,
            "name": coin.name,
            "issuer": coin.issuer,
            "price_usd": snap.price_usd,
            "deviation_pct": snap.deviation_pct,
            "z_score": snap.z_score,
            "liquidity_depth_usd": snap.liquidity_depth_pct,
            "severity": severity,
            "last_updated": snap.observed_at,
            "market_cap_usd": coin.market_cap_usd,
            "sources_count": int(snap.sources_count),
        }

    async def history(self, symbol: str, hours: int = 168) -> dict:
        """Return 7d history of price + z-score for charting."""
        result = await self.db.execute(select(Stablecoin).where(Stablecoin.symbol == symbol))
        coin = result.scalar_one_or_none()
        if not coin:
            from app.core.errors import NotFoundError
            raise NotFoundError(f"Stablecoin {symbol} not found")

        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        snaps = await self.db.execute(
            select(PegSnapshot)
            .where(PegSnapshot.stablecoin_id == coin.id)
            .where(PegSnapshot.observed_at >= cutoff.isoformat())
            .order_by(PegSnapshot.observed_at)
        )
        rows = snaps.scalars().all()
        prices = [s.price_usd for s in rows]
        mean, stddev = rolling_stats(prices)
        return {
            "symbol": symbol,
            "points": [
                {
                    "observed_at": s.observed_at,
                    "price_usd": s.price_usd,
                    "deviation_pct": s.deviation_pct,
                    "z_score": s.z_score,
                }
                for s in rows
            ],
            "mean_7d": mean,
            "stddev_7d": stddev,
        }
