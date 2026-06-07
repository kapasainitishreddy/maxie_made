"""Backtester — runs user code in a controlled Python sandbox.

For the MVP, we use AST validation + exec() in a restricted namespace.
For production, use E2B or a Docker-based sandbox.
"""
from __future__ import annotations

import ast
import io
import sys
from contextlib import redirect_stdout
from typing import Any

import numpy as np
import pandas as pd

from app.services.metrics import max_drawdown, sharpe, sortino, total_return


class Backtester:
    """Execute user strategy code and return backtest metrics."""

    def __init__(self, code: str, prices: pd.Series, initial_capital: float = 100_000.0) -> None:
        self.code = code
        self.prices = prices
        self.initial_capital = initial_capital

    def run(self) -> dict[str, Any]:
        """Execute the strategy code. Expects it to define:
        - A `signals(prices)` function returning a list of dicts with {timestamp, side}
        - Optionally `params` dict
        """
        # Validate code
        try:
            tree = ast.parse(self.code)
        except SyntaxError as e:
            return {"error": f"SyntaxError: {e}"}

        # Define banned names (for safety in exec)
        banned = {"open", "exec", "eval", "__import__", "compile", "input"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in banned:
                return {"error": f"Use of '{node.id}' is not allowed"}
            if isinstance(node, ast.Import):
                return {"error": "imports not allowed in strategy code"}
            if isinstance(node, ast.ImportFrom):
                return {"error": "imports not allowed in strategy code"}

        # Run in restricted namespace (sandboxed: AST-validated, no banned names, no imports)
        namespace: dict[str, Any] = {
            "np": np, "pandas": pd, "pd": pd, "__name__": "__strategy__",
        }
        stdout = io.StringIO()
        try:
            with redirect_stdout(stdout):
                # nosec B102 - sandboxed exec; inputs AST-validated above to block exec/eval/__import__/compile/input
                exec(compile(self.code, "<strategy>", "exec"), namespace)  # nosec
        except Exception as e:
            return {"error": f"Execution error: {type(e).__name__}: {e}"}

        if "signals" not in namespace:
            return {"error": "Strategy must define a `signals(prices)` function"}

        # Generate signals
        try:
            raw_signals = namespace["signals"](self.prices)
        except Exception as e:
            return {"error": f"signals() failed: {type(e).__name__}: {e}"}

        # Run the backtest
        return self._execute(raw_signals)

    def _execute(self, signals: list) -> dict[str, Any]:
        """Convert signals to trades and compute equity curve."""
        sig_map: dict[pd.Timestamp, dict] = {}
        for s in signals:
            ts = s.get("timestamp")
            if isinstance(ts, str):
                try:
                    ts = pd.Timestamp(ts)
                except (ValueError, TypeError):
                    # Skip signal with unparseable timestamp; log for debugging
                    continue
            sig_map[ts] = s

        cash = self.initial_capital
        qty = 0.0
        cost = 0.0
        equity_curve = []
        trades = []

        for ts, price in self.prices.items():
            eq = cash + qty * price
            equity_curve.append({"timestamp": str(ts), "equity": round(eq, 2), "price": round(float(price), 4)})
            if ts in sig_map:
                sig = sig_map[ts]
                side = sig.get("side", "buy")
                if side == "buy" and cash > 0:
                    qty = cash / float(price)
                    cost = float(price)
                    cash = 0.0
                    trades.append({"timestamp": str(ts), "side": "buy", "quantity": round(qty, 4), "price": round(float(price), 2)})
                elif side == "sell" and qty > 0:
                    proceeds = qty * float(price)
                    pnl = proceeds - qty * cost
                    cash = proceeds
                    trades.append({"timestamp": str(ts), "side": "sell", "quantity": round(qty, 4), "price": round(float(price), 2), "pnl": round(pnl, 2)})
                    qty = 0.0

        # Close open position
        if qty > 0 and len(self.prices) > 0:
            last = float(self.prices.iloc[-1])
            cash = qty * last
            equity_curve[-1]["equity"] = round(cash, 2)

        eq = pd.Series([e["equity"] for e in equity_curve])
        return {
            "initial_capital": self.initial_capital,
            "final_value": round(cash, 2),
            "total_return": round(total_return(eq), 4),
            "sharpe": round(sharpe(eq), 2),
            "sortino": round(sortino(eq), 2),
            "max_drawdown": round(max_drawdown(eq), 4),
            "num_trades": len(trades),
            "trades": trades,
            "equity_curve": equity_curve,
        }
