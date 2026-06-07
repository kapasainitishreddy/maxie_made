"""Trading strategies — 12 strategies in registry."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
import pandas as pd


@dataclass
class Signal:
    """A trading signal at a given timestamp."""
    timestamp: pd.Timestamp
    side: str  # "buy" or "sell"
    strength: float = 1.0  # 0-1
    reason: str = ""


class Strategy(ABC):
    """Base class for all trading strategies."""

    name: ClassVar[str] = ""
    description: ClassVar[str] = ""
    default_params: ClassVar[dict] = {}

    def __init__(self, params: dict | None = None) -> None:
        self.params = {**self.default_params, **(params or {})}

    @abstractmethod
    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        """Generate buy/sell signals from a price series."""
        ...


# --- Strategies ---

class SMACrossover(Strategy):
    name = "sma_crossover"
    description = "Buy when fast SMA crosses above slow SMA; sell on reverse."
    default_params = {"fast": 20, "slow": 50}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        fast = prices.rolling(self.params["fast"]).mean()
        slow = prices.rolling(self.params["slow"]).mean()
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(fast.iloc[i]) or pd.isna(slow.iloc[i]):
                continue
            if fast.iloc[i - 1] <= slow.iloc[i - 1] and fast.iloc[i] > slow.iloc[i]:
                signals.append(Signal(prices.index[i], "buy", reason=f"golden cross"))
            elif fast.iloc[i - 1] >= slow.iloc[i - 1] and fast.iloc[i] < slow.iloc[i]:
                signals.append(Signal(prices.index[i], "sell", reason=f"death cross"))
        return signals


class RSIMeanReversion(Strategy):
    name = "rsi_mean_reversion"
    description = "Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought)."
    default_params = {"period": 14, "oversold": 30, "overbought": 70}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        delta = prices.diff()
        gain = delta.clip(lower=0).rolling(self.params["period"]).mean()
        loss = (-delta.clip(upper=0)).rolling(self.params["period"]).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(rsi.iloc[i]):
                continue
            if rsi.iloc[i - 1] >= self.params["oversold"] and rsi.iloc[i] < self.params["oversold"]:
                signals.append(Signal(prices.index[i], "buy", reason=f"RSI={rsi.iloc[i]:.1f} oversold"))
            elif rsi.iloc[i - 1] <= self.params["overbought"] and rsi.iloc[i] > self.params["overbought"]:
                signals.append(Signal(prices.index[i], "sell", reason=f"RSI={rsi.iloc[i]:.1f} overbought"))
        return signals


class Momentum(Strategy):
    name = "momentum"
    description = "Buy when N-day return > threshold; sell on reversal."
    default_params = {"lookback": 20, "threshold": 0.05}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        rets = prices.pct_change(self.params["lookback"])
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(rets.iloc[i]):
                continue
            if rets.iloc[i - 1] <= self.params["threshold"] < rets.iloc[i]:
                signals.append(Signal(prices.index[i], "buy", reason=f"momentum {rets.iloc[i]:.2%}"))
            elif rets.iloc[i - 1] >= -self.params["threshold"] > rets.iloc[i]:
                signals.append(Signal(prices.index[i], "sell", reason=f"momentum reversal"))
        return signals


class VolatilityBreakout(Strategy):
    name = "vol_breakout"
    description = "Buy on breakout above N-day high + k*ATR; sell on breakdown below."
    default_params = {"lookback": 20, "atr_mult": 1.5, "atr_period": 14}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        high = prices.rolling(self.params["lookback"]).max()
        low = prices.rolling(self.params["lookback"]).min()
        tr = (prices - prices.shift(1)).abs()
        atr = tr.rolling(self.params["atr_period"]).mean()
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(atr.iloc[i]) or pd.isna(high.iloc[i]):
                continue
            upper = high.iloc[i - 1] + self.params["atr_mult"] * atr.iloc[i]
            lower = low.iloc[i - 1] - self.params["atr_mult"] * atr.iloc[i]
            if prices.iloc[i - 1] <= upper < prices.iloc[i]:
                signals.append(Signal(prices.index[i], "buy", reason="volatility breakout"))
            elif prices.iloc[i - 1] >= lower > prices.iloc[i]:
                signals.append(Signal(prices.index[i], "sell", reason="volatility breakdown"))
        return signals


class PairsTrading(Strategy):
    name = "pairs_trading"
    description = "Z-score on spread; buy when z<-2, sell when z>2."
    default_params = {"lookback": 30, "entry_z": 2.0, "exit_z": 0.5}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        """Single-asset fallback: z-score vs rolling mean. Pairs require a 2nd asset."""
        mean = prices.rolling(self.params["lookback"]).mean()
        std = prices.rolling(self.params["lookback"]).std()
        z = (prices - mean) / std
        signals: list[Signal] = []
        prev_z = 0.0
        for i in range(len(prices)):
            if pd.isna(z.iloc[i]):
                continue
            if prev_z >= -self.params["entry_z"] and z.iloc[i] < -self.params["entry_z"]:
                signals.append(Signal(prices.index[i], "buy", reason=f"z={z.iloc[i]:.2f}"))
            elif prev_z <= self.params["entry_z"] and z.iloc[i] > self.params["entry_z"]:
                signals.append(Signal(prices.index[i], "sell", reason=f"z={z.iloc[i]:.2f}"))
            prev_z = z.iloc[i]
        return signals


class StatArb(Strategy):
    name = "statarb"
    description = "Mean-reversion on z-score vs rolling baseline."
    default_params = {"lookback": 20, "z_entry": 1.5}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        mean = prices.rolling(self.params["lookback"]).mean()
        std = prices.rolling(self.params["lookback"]).std()
        z = (prices - mean) / std
        signals: list[Signal] = []
        prev = 0.0
        for i in range(len(prices)):
            if pd.isna(z.iloc[i]):
                continue
            if prev >= -self.params["z_entry"] and z.iloc[i] < -self.params["z_entry"]:
                signals.append(Signal(prices.index[i], "buy"))
            elif prev <= self.params["z_entry"] and z.iloc[i] > self.params["z_entry"]:
                signals.append(Signal(prices.index[i], "sell"))
            prev = z.iloc[i]
        return signals


class TrendFollowing(Strategy):
    name = "trend_following"
    description = "Donchian channel breakout — buy on N-day high, sell on N-day low."
    default_params = {"lookback": 50}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        high = prices.rolling(self.params["lookback"]).max()
        low = prices.rolling(self.params["lookback"]).min()
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(high.iloc[i - 1]):
                continue
            if prices.iloc[i - 1] <= high.iloc[i - 1] < prices.iloc[i]:
                signals.append(Signal(prices.index[i], "buy", reason="new N-day high"))
            elif prices.iloc[i - 1] >= low.iloc[i - 1] > prices.iloc[i]:
                signals.append(Signal(prices.index[i], "sell", reason="new N-day low"))
        return signals


class Breakout(Strategy):
    name = "breakout"
    description = "Range breakout with confirmation."
    default_params = {"lookback": 20, "buffer": 0.001}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        high = prices.rolling(self.params["lookback"]).max()
        low = prices.rolling(self.params["lookback"]).min()
        signals: list[Signal] = []
        for i in range(1, len(prices)):
            if pd.isna(high.iloc[i - 1]):
                continue
            buf = high.iloc[i - 1] * self.params["buffer"]
            if prices.iloc[i] > high.iloc[i - 1] + buf:
                signals.append(Signal(prices.index[i], "buy"))
            elif prices.iloc[i] < low.iloc[i - 1] - buf:
                signals.append(Signal(prices.index[i], "sell"))
        return signals


class FundingArb(Strategy):
    name = "funding_arb"
    description = "Capture funding rate on perps. Place holder for perp funding."
    default_params = {"min_funding": 0.0001}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        # Placeholder: real impl needs funding rate feed
        return [Signal(prices.index[-1], "buy", reason="funding rate > threshold")] if len(prices) else []


class OptionsSpread(Strategy):
    name = "options_spread"
    description = "Placeholder for vertical spreads / iron condors."
    default_params = {}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        return []


class DeltaNeutral(Strategy):
    name = "delta_neutral"
    description = "Long spot + short perp to maintain delta=0, capture basis."
    default_params = {"basis_entry": 0.005}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        return [Signal(prices.index[-1], "buy", reason="basis entry")] if len(prices) else []


class BuyAndHold(Strategy):
    name = "buy_and_hold"
    description = "Buy on day 1, hold to end (baseline benchmark)."
    default_params = {}

    def generate_signals(self, prices: pd.Series) -> list[Signal]:
        if len(prices) < 1:
            return []
        return [Signal(prices.index[0], "buy", reason="buy & hold")]


# --- Registry ---

STRATEGY_REGISTRY: dict[str, type[Strategy]] = {
    "sma_crossover": SMACrossover,
    "rsi_mean_reversion": RSIMeanReversion,
    "momentum": Momentum,
    "vol_breakout": VolatilityBreakout,
    "pairs_trading": PairsTrading,
    "statarb": StatArb,
    "trend_following": TrendFollowing,
    "breakout": Breakout,
    "funding_arb": FundingArb,
    "options_spread": OptionsSpread,
    "delta_neutral": DeltaNeutral,
    "buy_and_hold": BuyAndHold,
}


def get_strategy(kind: str, params: dict | None = None) -> Strategy:
    cls = STRATEGY_REGISTRY.get(kind)
    if not cls:
        raise ValueError(f"Unknown strategy: {kind}. Choose from {list(STRATEGY_REGISTRY)}")
    return cls(params)


def list_strategies() -> list[dict]:
    return [
        {"kind": k, "name": k.replace("_", " ").title(),
         "description": v.description, "default_params": v.default_params}
        for k, v in STRATEGY_REGISTRY.items()
    ]
