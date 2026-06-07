"""Performance metrics."""
import numpy as np
import pandas as pd
def total_return(eq): return float((eq.iloc[-1] / eq.iloc[0]) - 1) if len(eq) >= 2 and eq.iloc[0] != 0 else 0.0
def daily_returns(eq): return eq.pct_change().dropna()
def sharpe(eq, rf=0.04):
    r = daily_returns(eq)
    if r.std() == 0 or len(r) < 2: return 0.0
    return float(np.sqrt(252) * (r - rf/252).mean() / r.std())
def sortino(eq, rf=0.04):
    r = daily_returns(eq)
    d = r[r < 0]
    if len(d) == 0 or d.std() == 0: return 0.0
    return float(np.sqrt(252) * (r - rf/252).mean() / d.std())
def max_drawdown(eq):
    if len(eq) < 2: return 0.0
    return float(((eq - eq.cummax()) / eq.cummax()).min())
