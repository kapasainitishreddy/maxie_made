"""Data fetcher — yfinance wrapper with synthetic fallback for tests."""
from __future__ import annotations

import numpy as np
import pandas as pd


class DataFetcher:
    """Fetches OHLCV data; falls back to synthetic GBM for testing."""

    @staticmethod
    async def fetch(symbol: str, start: str, end: str) -> pd.Series:
        try:
            import yfinance as yf
            df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
            if df is None or df.empty:
                return DataFetcher._synthetic(symbol, start, end)
            close = df["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            return close.dropna()
        except Exception:
            return DataFetcher._synthetic(symbol, start, end)

    @staticmethod
    def _synthetic(symbol: str, start: str, end: str, seed: int | None = None) -> pd.Series:
        """GBM random walk — deterministic if seed given."""
        dates = pd.date_range(start=start, end=end, freq="D")
        if len(dates) == 0:
            return pd.Series(dtype=float)
        if seed is not None:
            np.random.seed(seed)
        rets = np.random.normal(0.0003, 0.015, len(dates))
        prices = 100.0 * np.exp(np.cumsum(rets))
        return pd.Series(prices, index=dates, name=symbol)
