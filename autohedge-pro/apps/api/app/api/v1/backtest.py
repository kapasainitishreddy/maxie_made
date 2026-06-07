"""Backtest API."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.errors import NotFoundError, ValidationError
from app.models.backtest import Backtest
from app.models.strategy import Strategy
from app.services.backtester import Backtester
from app.services.data import DataFetcher
from app.services.strategies import get_strategy

router = APIRouter()


class BacktestRequest(BaseModel):
    strategy_kind: str
    asset: str = "SPY"
    start_date: str
    end_date: str
    initial_capital: float = 100000.0
    params: dict = {}


@router.post("/run")
async def run_backtest(
    body: BacktestRequest, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    if body.start_date >= body.end_date:
        raise ValidationError("start_date must be before end_date")
    prices = await DataFetcher.fetch(body.asset, body.start_date, body.end_date)
    if len(prices) < 30:
        raise ValidationError(f"Insufficient price data for {body.asset} (got {len(prices)} bars)")

    strat = get_strategy(body.strategy_kind, body.params)
    result = Backtester(prices, strat, body.initial_capital).run()

    bt = Backtest(
        strategy_id=uuid.uuid4(),
        asset=body.asset,
        start_date=body.start_date,
        end_date=body.end_date,
        initial_capital=body.initial_capital,
        final_value=result["final_value"],
        sharpe=result["sharpe"],
        sortino=result["sortino"],
        max_drawdown=result["max_drawdown"],
        total_return=result["total_return"],
        num_trades=result["num_trades"],
        equity_curve=result["equity_curve"],
        trades=result["trades"],
    )
    db.add(bt)
    await db.flush()
    return {"id": str(bt.id), **result}


@router.get("")
async def list_backtests(db: Annotated[AsyncSession, Depends(get_db)]) -> list[dict]:
    res = await db.execute(select(Backtest).order_by(Backtest.created_at.desc()).limit(20))
    return [
        {
            "id": str(b.id), "asset": b.asset,
            "start_date": b.start_date, "end_date": b.end_date,
            "final_value": b.final_value, "sharpe": b.sharpe,
            "sortino": b.sortino, "max_drawdown": b.max_drawdown,
            "total_return": b.total_return, "num_trades": b.num_trades,
        }
        for b in res.scalars()
    ]


@router.get("/{bt_id}")
async def get_backtest(bt_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    b = await db.get(Backtest, bt_id)
    if not b:
        raise NotFoundError("Backtest not found")
    return {
        "id": str(b.id), "asset": b.asset,
        "start_date": b.start_date, "end_date": b.end_date,
        "initial_capital": b.initial_capital,
        "final_value": b.final_value, "sharpe": b.sharpe,
        "sortino": b.sortino, "max_drawdown": b.max_drawdown,
        "total_return": b.total_return, "num_trades": b.num_trades,
        "equity_curve": b.equity_curve, "trades": b.trades,
    }
