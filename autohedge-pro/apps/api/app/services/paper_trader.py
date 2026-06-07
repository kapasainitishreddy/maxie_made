"""Paper trading engine — executes signals against simulated portfolio."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PaperPosition:
    symbol: str
    quantity: float
    avg_entry: float
    current_price: float = 0.0

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def unrealized_pnl(self) -> float:
        return (self.current_price - self.avg_entry) * self.quantity


@dataclass
class PaperTrader:
    """Simulated broker — fills market orders at last price, no slippage model."""

    cash: float = 100_000.0
    positions: dict[str, PaperPosition] = field(default_factory=dict)
    trades: list[dict] = field(default_factory=list)

    def execute(self, symbol: str, side: str, quantity: float, price: float, reason: str = "") -> dict:
        ts = datetime.now(timezone.utc).isoformat()
        pnl = 0.0

        if side == "buy":
            cost = quantity * price
            if cost > self.cash:
                return {"error": "insufficient cash", "cash": self.cash}
            self.cash -= cost
            if symbol in self.positions:
                p = self.positions[symbol]
                total_qty = p.quantity + quantity
                p.avg_entry = (p.avg_entry * p.quantity + price * quantity) / total_qty
                p.quantity = total_qty
                p.current_price = price
            else:
                self.positions[symbol] = PaperPosition(symbol, quantity, price, price)
        elif side == "sell":
            if symbol not in self.positions:
                return {"error": "no position"}
            p = self.positions[symbol]
            if quantity > p.quantity:
                return {"error": "insufficient shares"}
            proceeds = quantity * price
            pnl = (price - p.avg_entry) * quantity
            self.cash += proceeds
            p.quantity -= quantity
            if p.quantity <= 0:
                del self.positions[symbol]
            else:
                p.current_price = price

        trade = {
            "timestamp": ts, "symbol": symbol, "side": side, "quantity": quantity,
            "price": price, "pnl": round(pnl, 2), "reason": reason,
        }
        self.trades.append(trade)
        return trade

    def portfolio_value(self) -> float:
        return self.cash + sum(p.market_value for p in self.positions.values())

    def update_prices(self, prices: dict[str, float]) -> None:
        for sym, pos in self.positions.items():
            if sym in prices:
                pos.current_price = prices[sym]

    def snapshot(self) -> dict[str, Any]:
        return {
            "cash": round(self.cash, 2),
            "total_value": round(self.portfolio_value(), 2),
            "positions": [
                {
                    "symbol": p.symbol,
                    "quantity": p.quantity,
                    "avg_entry": round(p.avg_entry, 2),
                    "current_price": round(p.current_price, 2),
                    "market_value": round(p.market_value, 2),
                    "unrealized_pnl": round(p.unrealized_pnl, 2),
                }
                for p in self.positions.values()
            ],
            "num_trades": len(self.trades),
        }
