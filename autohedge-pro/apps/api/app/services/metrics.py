"""Performance metrics for backtests."""
from __future__ import annotations

import numpy as np
import pandas as pd


def total_return(equity: pd.Series) -> float:
    if len(equity) < 2 or equity.iloc[0] == 0:
        return 0.0
    return float((equity.iloc[-1] / equity.iloc[0]) - 1)


def daily_returns(equity: pd.Series) -> pd.Series:
    return equity.pct_change().dropna()


def sharpe(equity: pd.Series, risk_free: float = 0.04) -> float:
    """Annualized Sharpe ratio."""
    rets = daily_returns(equity)
    if rets.std() == 0 or len(rets) < 2:
        return 0.0
    excess = rets - (risk_free / 252)
    return float(np.sqrt(252) * excess.mean() / rets.std())


def sortino(equity: pd.Series, risk_free: float = 0.04) -> float:
    """Annualized Sortino ratio (penalizes only downside vol)."""
    rets = daily_returns(equity)
    downside = rets[rets < 0]
    if len(downside) == 0 or downside.std() == 0:
        return 0.0
    excess = rets - (risk_free / 252)
    return float(np.sqrt(252) * excess.mean() / downside.std())


def max_drawdown(equity: pd.Series) -> float:
    """Max drawdown as negative fraction (e.g. -0.25 = 25% drawdown)."""
    if len(equity) < 2:
        return 0.0
    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    return float(drawdown.min())


def calmar(equity: pd.Series) -> float:
    """Calmar ratio = annualized return / abs(max drawdown)."""
    rets = daily_returns(equity)
    if len(rets) < 252:
        return 0.0
    annual_return = (1 + rets.mean()) ** 252 - 1
    dd = abs(max_drawdown(equity))
    if dd == 0:
        return 0.0
    return float(annual_return / dd)
