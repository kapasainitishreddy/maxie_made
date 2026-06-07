"""Trading strategies + metrics + backtester."""
from app.services.strategies import (
    Strategy, Signal, get_strategy, list_strategies, STRATEGY_REGISTRY,
)
from app.services.metrics import (
    sharpe, sortino, max_drawdown, total_return, calmar,
)
from app.services.backtester import Backtester
from app.services.data import DataFetcher
from app.services.paper_trader import PaperTrader

__all__ = [
    "Strategy", "Signal", "get_strategy", "list_strategies", "STRATEGY_REGISTRY",
    "sharpe", "sortino", "max_drawdown", "total_return", "calmar",
    "Backtester", "DataFetcher", "PaperTrader",
]
