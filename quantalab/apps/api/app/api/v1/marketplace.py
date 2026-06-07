"""Strategy marketplace API."""
from __future__ import annotations

import uuid

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# In-memory marketplace (real app would use DB)
_MARKETPLACE = [
    {"id": "1", "name": "Mean Reversion Sniper", "author": "quant_vik", "description": "Buy oversold RSI, sell overbought. Proven on SPY 2010-2024.",
     "price_cents": 4900, "downloads": 1247, "rating": 4.8, "tags": ["mean-reversion", "rsi"]},
    {"id": "2", "name": "Volatility Crusher", "author": "hedgefund_guy", "description": "Short volatility in calm regimes, long vol in crashes. Uses VIX term structure.",
     "price_cents": 9900, "downloads": 534, "rating": 4.6, "tags": ["volatility", "options"]},
    {"id": "3", "name": "Pairs Trading Pro", "author": "stat_arb_queen", "description": "Cointegration-based pair selection with z-score entry/exit.",
     "price_cents": 7900, "downloads": 892, "rating": 4.9, "tags": ["stat-arb", "pairs"]},
    {"id": "4", "name": "Momentum King", "author": "trend_follower", "description": "Multi-timeframe momentum with regime filter.",
     "price_cents": 0, "downloads": 3421, "rating": 4.5, "tags": ["momentum", "trend"]},
    {"id": "5", "name": "Overnight Edge", "author": "overnight_pro", "description": "Hold SPY overnight only, flat intraday. Academic anomaly.",
     "price_cents": 2900, "downloads": 1823, "rating": 4.7, "tags": ["overnight", "anomaly"]},
]


@router.get("")
async def list_strategies() -> list[dict]:
    return _MARKETPLACE


@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str) -> dict:
    s = next((s for s in _MARKETPLACE if s["id"] == strategy_id), None)
    if not s:
        from app.core.errors import NotFoundError
        raise NotFoundError("Strategy not found")
    return s


class PurchaseRequest(BaseModel):
    strategy_id: str


@router.post("/purchase")
async def purchase(req: PurchaseRequest) -> dict:
    s = next((s for s in _MARKETPLACE if s["id"] == req.strategy_id), None)
    if not s:
        from app.core.errors import NotFoundError
        raise NotFoundError("Strategy not found")
    return {"status": "success", "strategy_id": s["id"], "code": "# purchased strategy code goes here"}
