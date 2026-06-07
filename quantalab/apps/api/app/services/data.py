"""Data fetcher for QuantaLab."""
from __future__ import annotations

import numpy as np
import pandas as pd


class DataFetcher:
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
    def _synthetic(symbol: str, start: str, end: str) -> pd.Series:
        dates = pd.date_range(start=start, end=end, freq="D")
        if len(dates) == 0:
            return pd.Series(dtype=float)
        np.random.seed(42)
        rets = np.random.normal(0.0003, 0.015, len(dates))
        return pd.Series(100.0 * np.exp(np.cumsum(rets)), index=dates, name=symbol)
