"""Portfolio API (paper trading)."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.errors import NotFoundError, ValidationError
from app.models.portfolio import Portfolio, Position
from app.services.paper_trader import PaperTrader

router = APIRouter()


# In-memory paper trader (in prod, use Redis)
_paper: PaperTrader = PaperTrader(cash=100_000.0)


class ExecuteRequest(BaseModel):
    symbol: str
    side: str  # buy | sell
    quantity: float
    price: float
    reason: str = ""


@router.get("/snapshot")
async def snapshot() -> dict:
    return _paper.snapshot()


@router.post("/execute")
async def execute(req: ExecuteRequest) -> dict:
    if req.quantity <= 0:
        raise ValidationError("quantity must be positive")
    if req.price <= 0:
        raise ValidationError("price must be positive")
    if req.side not in ("buy", "sell"):
        raise ValidationError("side must be 'buy' or 'sell'")
    return _paper.execute(req.symbol, req.side, req.quantity, req.price, req.reason)


@router.get("/trades")
async def list_trades() -> list[dict]:
    return _paper.trades[-50:]


@router.post("/reset")
async def reset() -> dict:
    global _paper
    _paper = PaperTrader(cash=100_000.0)
    return _paper.snapshot()
