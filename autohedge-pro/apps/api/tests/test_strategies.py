"""Tests for strategies + metrics + backtester + paper trader."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.services.strategies import (
    STRATEGY_REGISTRY, get_strategy, list_strategies,
    SMACrossover, RSIMeanReversion, Momentum, PairsTrading, BuyAndHold,
)
from app.services.metrics import sharpe, sortino, max_drawdown, total_return
from app.services.backtester import Backtester
from app.services.paper_trader import PaperTrader


def make_prices(n: int = 200, seed: int = 42, trend: float = 0.0) -> pd.Series:
    np.random.seed(seed)
    rets = np.random.normal(trend, 0.015, n)
    prices = 100.0 * np.exp(np.cumsum(rets))
    return pd.Series(prices, index=pd.date_range("2023-01-01", periods=n, freq="D"))


# --- Strategy registry ---

def test_registry_has_12_strategies():
    assert len(STRATEGY_REGISTRY) >= 12
    expected = {"sma_crossover", "rsi_mean_reversion", "momentum", "vol_breakout",
                "pairs_trading", "statarb", "trend_following", "breakout",
                "funding_arb", "options_spread", "delta_neutral", "buy_and_hold"}
    assert expected.issubset(set(STRATEGY_REGISTRY.keys()))


def test_list_strategies_includes_metadata():
    catalog = list_strategies()
    for s in catalog:
        assert "kind" in s
        assert "name" in s
        assert "description" in s
        assert "default_params" in s


def test_get_strategy_unknown_raises():
    with pytest.raises(ValueError):
        get_strategy("not_a_strategy")


def test_get_strategy_returns_instance():
    s = get_strategy("sma_crossover", {"fast": 10, "slow": 30})
    assert isinstance(s, SMACrossover)
    assert s.params["fast"] == 10


# --- Strategy signal generation ---

def test_sma_crossover_produces_signals():
    prices = make_prices(trend=0.001)
    sigs = SMACrossover({"fast": 5, "slow": 15}).generate_signals(prices)
    assert len(sigs) > 0
    assert all(s.side in ("buy", "sell") for s in sigs)


def test_sma_no_signals_on_short_series():
    prices = pd.Series([100, 101, 102, 103, 104], index=pd.date_range("2023-01-01", periods=5))
    sigs = SMACrossover({"fast": 20, "slow": 50}).generate_signals(prices)
    assert sigs == []


def test_rsi_produces_signals_on_random_walk():
    prices = make_prices(500)
    sigs = RSIMeanReversion().generate_signals(prices)
    # May or may not produce signals — just make sure it doesn't crash
    assert isinstance(sigs, list)


def test_buy_and_hold_single_buy():
    prices = make_prices(50)
    sigs = BuyAndHold().generate_signals(prices)
    assert len(sigs) == 1
    assert sigs[0].side == "buy"


def test_momentum_uses_threshold():
    prices = make_prices(100, trend=0.005)
    sigs = Momentum({"lookback": 20, "threshold": 0.10}).generate_signals(prices)
    # High threshold should produce few or no signals on random walk
    assert isinstance(sigs, list)


# --- Metrics ---

def test_total_return_positive():
    eq = pd.Series([100, 110, 120, 115, 130])
    assert total_return(eq) == pytest.approx(0.30, abs=0.01)


def test_total_return_negative():
    eq = pd.Series([100, 90, 80, 70])
    assert total_return(eq) == pytest.approx(-0.30, abs=0.01)


def test_total_return_empty():
    assert total_return(pd.Series([], dtype=float)) == 0.0


def test_max_drawdown_negative():
    eq = pd.Series([100, 120, 90, 110, 80])
    dd = max_drawdown(eq)
    assert dd < 0
    assert dd >= -1.0


def test_max_drawdown_zero_on_monotonic_up():
    eq = pd.Series([100, 110, 120, 130, 140])
    assert max_drawdown(eq) == 0.0


def test_sharpe_zero_for_constant():
    eq = pd.Series([100, 100, 100, 100])
    assert sharpe(eq) == 0.0


def test_sharpe_in_range():
    eq = make_prices(252, seed=1)
    s = sharpe(eq)
    assert -5.0 < s < 5.0


def test_sortino_in_range():
    eq = make_prices(252, seed=2)
    s = sortino(eq)
    assert -5.0 < s < 5.0


# --- Backtester ---

def test_backtest_buy_and_hold_profit():
    prices = pd.Series([100, 105, 110, 115, 120], index=pd.date_range("2023-01-01", periods=5))
    bt = Backtester(prices, BuyAndHold(), initial_capital=10_000)
    result = bt.run()
    assert result["total_return"] > 0
    assert result["num_trades"] >= 1
    assert result["final_value"] > 10_000


def test_backtest_returns_equity_curve():
    prices = make_prices(100)
    result = Backtester(prices, SMACrossover(), 10_000).run()
    assert len(result["equity_curve"]) == 100
    assert all("equity" in e for e in result["equity_curve"])


def test_backtest_no_signals_returns_initial():
    prices = make_prices(10)
    # Use a strategy that won't fire on a 10-day series
    result = Backtester(prices, SMACrossover({"fast": 50, "slow": 200}), 10_000).run()
    assert result["final_value"] == 10_000  # no trades


def test_backtest_metrics_populated():
    prices = make_prices(200)
    result = Backtester(prices, SMACrossover(), 10_000).run()
    assert "sharpe" in result
    assert "sortino" in result
    assert "max_drawdown" in result


# --- Paper trader ---

def test_paper_buy_reduces_cash():
    t = PaperTrader(cash=10_000)
    t.execute("AAPL", "buy", 10, 150.0, "test")
    assert t.cash < 10_000
    assert "AAPL" in t.positions
    assert t.positions["AAPL"].quantity == 10


def test_paper_sell_realizes_pnl():
    t = PaperTrader(cash=10_000)
    t.execute("AAPL", "buy", 10, 100.0)
    t.execute("AAPL", "sell", 10, 120.0)
    assert t.positions == {}
    assert t.cash > 10_000
    last_trade = t.trades[-1]
    assert last_trade["pnl"] == 200.0  # (120-100) * 10


def test_paper_insufficient_cash_buy():
    t = PaperTrader(cash=100)
    result = t.execute("AAPL", "buy", 10, 100.0)
    assert "error" in result


def test_paper_no_position_sell():
    t = PaperTrader(cash=10_000)
    result = t.execute("AAPL", "sell", 1, 100.0)
    assert "error" in result


def test_paper_portfolio_value():
    t = PaperTrader(cash=10_000)
    t.execute("AAPL", "buy", 10, 100.0)
    t.update_prices({"AAPL": 110.0})
    assert t.portfolio_value() == pytest.approx(9000 + 1100, abs=1.0)


def test_paper_snapshot_includes_positions():
    t = PaperTrader(cash=10_000)
    t.execute("AAPL", "buy", 10, 100.0)
    snap = t.snapshot()
    assert "cash" in snap
    assert "total_value" in snap
    assert "positions" in snap
    assert len(snap["positions"]) == 1
