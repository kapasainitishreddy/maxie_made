"""Stablecoin CRUD + list."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUser, get_current_user
from app.db import get_db
from app.models.stablecoin import Stablecoin
from app.schemas.stablecoin import StablecoinCreate, StablecoinRead

router = APIRouter()


@router.get("", response_model=list[StablecoinRead])
async def list_stablecoins(
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
    active_only: bool = Query(default=True),
    tier: int | None = Query(default=None, ge=1, le=3, description="Max tier to include"),
) -> list[Stablecoin]:
    """List all stablecoins visible at the user's plan tier."""
    stmt = select(Stablecoin).order_by(Stablecoin.market_cap_usd.desc())
    if active_only:
        stmt = stmt.where(Stablecoin.is_active.is_(True))
    if tier is not None:
        stmt = stmt.where(Stablecoin.tier <= tier)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{symbol}", response_model=StablecoinRead)
async def get_stablecoin(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
) -> Stablecoin:
    result = await db.execute(select(Stablecoin).where(Stablecoin.symbol == symbol.upper()))
    coin = result.scalar_one_or_none()
    if not coin:
        raise NotFoundError(f"Stablecoin {symbol} not found")
    return coin


@router.post("", response_model=StablecoinRead, status_code=status.HTTP_201_CREATED)
async def create_stablecoin(
    payload: StablecoinCreate,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> Stablecoin:
    """Create a new stablecoin record. API tier only."""
    if user.plan != "api":
        from app.core.errors import PlanLimitError

        raise PlanLimitError("Adding custom stablecoins requires the API tier.")

    payload.symbol = payload.symbol.upper()
    coin = Stablecoin(**payload.model_dump())
    db.add(coin)
    await db.commit()
    await db.refresh(coin)
    return coin
