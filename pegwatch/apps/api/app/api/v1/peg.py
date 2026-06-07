"""Peg status + history + manual snapshot."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUser, get_current_user
from app.db import get_db
from app.schemas.peg import PegHistoryResponse, PegStatus
from app.services.peg_engine import PegEngine
from app.services.price_ingestor import PriceIngestor

router = APIRouter()


@router.get("/status", response_model=list[PegStatus])
async def all_statuses(
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
) -> list[dict]:
    """Get the current peg status of every active stablecoin (dashboard home)."""
    from app.models.stablecoin import Stablecoin
    from sqlalchemy import select

    result = await db.execute(
        select(Stablecoin).where(Stablecoin.is_active.is_(True)).order_by(Stablecoin.market_cap_usd.desc())
    )
    coins = list(result.scalars().all())
    engine = PegEngine(db)
    out: list[dict] = []
    for coin in coins:
        try:
            out.append(await engine.current_status(coin.symbol))
        except NotFoundError:
            continue
    return out


@router.get("/{symbol}/status", response_model=PegStatus)
async def get_status(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
) -> dict:
    engine = PegEngine(db)
    return await engine.current_status(symbol.upper())


@router.get("/{symbol}/history", response_model=PegHistoryResponse)
async def get_history(
    symbol: str,
    hours: int = Query(default=168, ge=1, le=720),
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
) -> dict:
    engine = PegEngine(db)
    return await engine.history(symbol.upper(), hours=hours)


@router.post("/{symbol}/refresh", response_model=PegStatus)
async def refresh_snapshot(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> dict:
    """Trigger a fresh price fetch + z-score snapshot for a symbol."""
    from app.models.stablecoin import Stablecoin
    from sqlalchemy import select

    if user.plan == "free":
        from app.core.errors import PlanLimitError
        raise PlanLimitError("Manual refresh is a Pro feature. Upgrade to trigger live updates.")

    result = await db.execute(select(Stablecoin).where(Stablecoin.symbol == symbol.upper()))
    coin = result.scalar_one_or_none()
    if not coin:
        raise NotFoundError(f"Stablecoin {symbol} not found")

    ingestor = PriceIngestor()
    quotes = await ingestor.fetch_all(coin.symbol)
    engine = PegEngine(db)
    snap = await engine.record_snapshot(
        stablecoin_id=coin.id,
        curve_price=quotes.get("curve_price"),
        uniswap_price=quotes.get("uniswap_price"),
        cex_median_price=quotes.get("cex_median_price"),
        liquidity_depth_usd=quotes.get("liquidity_depth_usd", 0.0),
    )

    # If severity is critical, fire an alert automatically
    from app.services.peg_engine import severity_from_z
    sev = severity_from_z(snap.z_score, snap.deviation_pct)
    if sev in ("warning", "critical"):
        from app.models.alert import Alert
        from app.services.ai_summary import summarize_incident
        ai = await summarize_incident(coin.symbol, snap.deviation_pct, snap.z_score, snap.price_usd)
        alert = Alert(
            stablecoin_id=coin.id,
            triggered_at=datetime.now(timezone.utc).isoformat(),
            severity=sev,
            price_at_trigger=snap.price_usd,
            deviation_pct=snap.deviation_pct,
            z_score=snap.z_score,
            title=f"{coin.symbol} {sev.upper()}: {snap.deviation_pct:+.3f}% off peg",
            summary=f"Price ${snap.price_usd:.4f} on {int(snap.sources_count)} sources. "
            f"Z-score {snap.z_score:+.2f}.",
            ai_summary=ai,
        )
        db.add(alert)
        await db.commit()

    return await engine.current_status(coin.symbol)
