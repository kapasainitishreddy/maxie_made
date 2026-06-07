"""Backtester — runs a strategy over a price series, returns equity curve + trades."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

from app.services.metrics import (
    max_drawdown,
    sharpe,
    sortino,
    total_return,
)
from app.services.strategies import Strategy, Signal, get_strategy


@dataclass
class Trade:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    price: float
    pnl: float = 0.0
    reason: str = ""


class Backtester:
    """
    Simple long-only backtester with full equity reinvestment.
    For real production: support shorting, margin, slippage, commissions.
    """

    def __init__(
        self,
        prices: pd.Series,
        strategy: Strategy,
        initial_capital: float = 100_000.0,
        commission: float = 0.001,
        slippage: float = 0.0005,
    ) -> None:
        self.prices = prices
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def run(self) -> dict[str, Any]:
        signals = self.strategy.generate_signals(self.prices)
        return self._execute(signals)

    def _execute(self, signals: list[Signal]) -> dict[str, Any]:
        cash = self.initial_capital
        position_qty = 0.0
        position_cost = 0.0
        equity_curve: list[dict] = []
        trades: list[Trade] = []
        sig_map = {s.timestamp: s for s in signals}

        for ts, price in self.prices.items():
            # Mark-to-market equity
            position_value = position_qty * price
            equity = cash + position_value
            equity_curve.append({"timestamp": str(ts), "equity": round(equity, 2), "price": round(price, 4)})

            # Process signal at this timestamp
            if ts in sig_map:
                sig = sig_map[ts]
                if sig.side == "buy" and cash > 0:
                    fill_price = price * (1 + self.slippage)
                    qty = (cash * (1 - self.commission)) / fill_price
                    cash = 0.0
                    position_qty = qty
                    position_cost = fill_price
                    trades.append(Trade(ts, "ASSET", "buy", qty, fill_price, 0.0, sig.reason))
                elif sig.side == "sell" and position_qty > 0:
                    fill_price = price * (1 - self.slippage)
                    proceeds = position_qty * fill_price * (1 - self.commission)
                    pnl = proceeds - (position_qty * position_cost)
                    cash = proceeds
                    trades.append(Trade(ts, "ASSET", "sell", position_qty, fill_price, pnl, sig.reason))
                    position_qty = 0.0
                    position_cost = 0.0

        # Close any open position at end
        if position_qty > 0 and len(self.prices) > 0:
            last_ts, last_price = self.prices.index[-1], float(self.prices.iloc[-1])
            proceeds = position_qty * last_price * (1 - self.commission)
            pnl = proceeds - (position_qty * position_cost)
            cash = proceeds
            trades.append(Trade(last_ts, "ASSET", "sell", position_qty, last_price, pnl, "end-of-backtest close"))
            equity_curve[-1]["equity"] = round(cash, 2)

        # Compute metrics
        eq = pd.Series([e["equity"] for e in equity_curve])
        return {
            "initial_capital": self.initial_capital,
            "final_value": round(float(cash), 2),
            "total_return": round(total_return(eq), 4),
            "sharpe": round(sharpe(eq), 2),
            "sortino": round(sortino(eq), 2),
            "max_drawdown": round(max_drawdown(eq), 4),
            "num_trades": len(trades),
            "trades": [
                {
                    "timestamp": str(t.timestamp),
                    "side": t.side,
                    "quantity": round(t.quantity, 4),
                    "price": round(t.price, 2),
                    "pnl": round(t.pnl, 2),
                    "reason": t.reason,
                }
                for t in trades
            ],
            "equity_curve": equity_curve,
        }
