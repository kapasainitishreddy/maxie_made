"""Backtest + NL→Code API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.errors import ValidationError
from app.models.backtest import Backtest
from app.services.backtester import Backtester
from app.services.data import DataFetcher
from app.services.nl2code import NL2Code

router = APIRouter()


class NL2CodeRequest(BaseModel):
    description: str
    asset: str = "SPY"
    start_date: str = "2023-01-01"
    end_date: str = "2024-01-01"


class BacktestCodeRequest(BaseModel):
    code: str
    asset: str = "SPY"
    start_date: str = "2023-01-01"
    end_date: str = "2024-01-01"


@router.post("/nl2code")
async def nl2code(req: NL2CodeRequest) -> dict:
    """Translate NL description to Python, then run a backtest."""
    if not req.description.strip():
        raise ValidationError("description cannot be empty")
    translator = NL2Code()
    code = await translator.translate(req.description)
    prices = await DataFetcher.fetch(req.asset, req.start_date, req.end_date)
    if len(prices) < 30:
        raise ValidationError(f"Insufficient data for {req.asset}")
    result = Backtester(code, prices).run()
    return {"code": code, "result": result}


@router.post("/run")
async def run_code(req: BacktestCodeRequest, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    prices = await DataFetcher.fetch(req.asset, req.start_date, req.end_date)
    if len(prices) < 30:
        raise ValidationError("Insufficient data")
    result = Backtester(req.code, prices).run()
    if "error" not in result:
        bt = Backtest(
            strategy_name="user",
            asset=req.asset,
            sharpe=result.get("sharpe", 0),
            sortino=result.get("sortino", 0),
            max_drawdown=result.get("max_drawdown", 0),
            total_return=result.get("total_return", 0),
            equity_curve=result.get("equity_curve", []),
        )
        db.add(bt)
        await db.flush()
    return result


@router.get("")
async def list_backtests(db: Annotated[AsyncSession, Depends(get_db)]) -> list[dict]:
    res = await db.execute(select(Backtest).order_by(Backtest.created_at.desc()).limit(20))
    return [
        {"id": str(b.id), "strategy_name": b.strategy_name, "asset": b.asset,
         "sharpe": b.sharpe, "total_return": b.total_return, "max_drawdown": b.max_drawdown}
        for b in res.scalars()
    ]
