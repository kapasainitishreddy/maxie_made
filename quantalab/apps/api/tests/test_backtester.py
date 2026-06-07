"""Tests for backtester + metrics + NL2Code."""
import numpy as np
import pandas as pd
import pytest
from app.services.backtester import Backtester
from app.services.metrics import sharpe, sortino, max_drawdown, total_return
from app.services.nl2code import NL2Code


def make_prices(n=200, seed=42, trend=0.0):
    np.random.seed(seed)
    rets = np.random.normal(trend, 0.015, n)
    return pd.Series(100.0 * np.exp(np.cumsum(rets)), index=pd.date_range("2023-01-01", periods=n, freq="D"))


# --- Metrics ---

def test_total_return_positive():
    eq = pd.Series([100, 110, 120])
    assert total_return(eq) == pytest.approx(0.20, abs=0.01)


def test_sharpe_zero_constant():
    eq = pd.Series([100, 100, 100, 100])
    assert sharpe(eq) == 0.0


def test_max_drawdown():
    eq = pd.Series([100, 120, 90, 110, 80])
    assert max_drawdown(eq) < 0


def test_sortino_in_range():
    eq = make_prices(252)
    assert -5 < sortino(eq) < 5


# --- Backtester ---

VALID_SMA = """
def signals(prices):
    fast = prices.rolling(20).mean()
    slow = prices.rolling(50).mean()
    out = []
    for i in range(1, len(prices)):
        if pd.isna(fast.iloc[i]) or pd.isna(slow.iloc[i]):
            continue
        if fast.iloc[i-1] <= slow.iloc[i-1] and fast.iloc[i] > slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "buy"})
        elif fast.iloc[i-1] >= slow.iloc[i-1] and fast.iloc[i] < slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "sell"})
    return out
"""


def test_backtest_valid_sma():
    prices = make_prices(200)
    result = Backtester(VALID_SMA, prices, 10_000).run()
    assert "error" not in result
    assert result["final_value"] > 0
    assert len(result["equity_curve"]) == 200


def test_backtest_syntax_error():
    result = Backtester("def signals(:", make_prices(50)).run()
    assert "error" in result
    assert "SyntaxError" in result["error"]


def test_backtest_missing_signals():
    code = "x = 1"
    result = Backtester(code, make_prices(50)).run()
    assert "error" in result
    assert "signals" in result["error"]


def test_backtest_banned_open():
    code = """
def signals(prices):
    f = open('/etc/passwd', 'r')
    return []
"""
    result = Backtester(code, make_prices(50)).run()
    assert "error" in result
    assert "open" in result["error"]


def test_backtest_banned_import():
    code = """
import os
def signals(prices): return []
"""
    result = Backtester(code, make_prices(50)).run()
    assert "error" in result
    assert "import" in result["error"].lower()


def test_backtest_buy_and_hold():
    code = """
def signals(prices):
    return [{"timestamp": prices.index[0], "side": "buy"}] if len(prices) else []
"""
    prices = pd.Series([100, 110, 120, 130, 140], index=pd.date_range("2023-01-01", periods=5))
    result = Backtester(code, prices, 1000).run()
    assert "error" not in result
    assert result["total_return"] > 0
    assert result["num_trades"] >= 1


def test_backtest_metrics_populated():
    prices = make_prices(200)
    result = Backtester(VALID_SMA, prices).run()
    for k in ("sharpe", "sortino", "max_drawdown", "total_return", "num_trades"):
        assert k in result


# --- NL2Code ---

@pytest.mark.asyncio
async def test_nl2code_clean_strips_markdown():
    n = NL2Code()
    cleaned = n._clean("```python\ndef signals(): pass\n```")
    assert "```" not in cleaned
    assert "def signals" in cleaned


@pytest.mark.asyncio
async def test_nl2code_falls_back_on_ollama_failure():
    """When Ollama is unavailable, fall back to a buy & hold strategy."""
    n = NL2Code(host="http://localhost:1", model="x")
    code = await n.translate("Buy and hold SPY")
    assert "def signals" in code
    assert "buy" in code


@pytest.mark.asyncio
async def test_nl2code_preserves_function_name():
    n = NL2Code(host="http://localhost:1", model="x")
    code = await n.translate("Test")
    assert "signals" in code
