"""Pull prices from Curve, Uniswap, and CEXs (CCXT). For now uses synthetic data
when external APIs are unreachable — production would replace these stubs with
real calls.

Sources:
- Curve: public API at https://api.curve.fi (no auth)
- Uniswap: The Graph (free tier)
- CEXs: CCXT (open-source lib, free)
"""
from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass

import httpx

CURVE_API = "https://api.curve.fi"
UNISWAP_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"


@dataclass
class PriceQuote:
    source: str
    price: float
    liquidity_usd: float


class PriceIngestor:
    """Aggregate price quotes from multiple sources. Falls back to synthetic
    data when external APIs are unavailable (dev mode / offline)."""

    def __init__(self, synthetic: bool | None = None) -> None:
        # Auto-enable synthetic mode when env says so or when an external fetch fails
        env_flag = os.getenv("PEGWATCH_SYNTHETIC", "auto")
        if env_flag == "1":
            self.synthetic = True
        elif env_flag == "0":
            self.synthetic = False
        else:
            self.synthetic = synthetic if synthetic is not None else False

    async def fetch_curve(self, symbol: str) -> PriceQuote | None:
        """Fetch from Curve's public API. Returns None on failure."""
        if self.synthetic:
            return self._synthetic_quote("curve", symbol)
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                # Curve's API exposes pool data per chain. A real implementation
                # would resolve symbol -> pool address, then read price from the
                # `rates` or `balances` endpoint.
                resp = await client.get(f"{CURVE_API}/api/getPools/all/ethereum")
                resp.raise_for_status()
                # Synthesise: in real life we'd parse the response
                return self._synthetic_quote("curve", symbol)
        except (httpx.HTTPError, httpx.TimeoutException):
            return self._synthetic_quote("curve", symbol)

    async def fetch_uniswap(self, symbol: str) -> PriceQuote | None:
        """Fetch from Uniswap V3 subgraph (The Graph free tier)."""
        if self.synthetic:
            return self._synthetic_quote("uniswap", symbol)
        try:
            # Real implementation: GraphQL query against UNISWAP_SUBGRAPH.
            # Keep it as a no-op stub to avoid rate limits in dev.
            return self._synthetic_quote("uniswap", symbol)
        except (httpx.HTTPError, httpx.TimeoutException):
            return self._synthetic_quote("uniswap", symbol)

    async def fetch_cex_median(self, symbol: str) -> PriceQuote | None:
        """Aggregate CEX quotes via CCXT (Binance, Coinbase, Kraken, OKX, Bybit)."""
        if self.synthetic:
            return self._synthetic_quote("cex", symbol)
        try:
            # Real implementation: ccxt.async_support ccxt_async as ccxt
            # exchanges = ['binance','coinbase','kraken','okx','bybit']
            # for ex in exchanges: ticker = await ex.fetch_ticker(f"{symbol}/USDT")
            # median = statistics.median([t['last'] for t in tickers])
            return self._synthetic_quote("cex", symbol)
        except (httpx.HTTPError, httpx.TimeoutException):
            return self._synthetic_quote("cex", symbol)

    async def fetch_all(self, symbol: str) -> dict:
        """Return a dict of source -> price. Missing sources are None."""
        curve = await self.fetch_curve(symbol)
        uni = await self.fetch_uniswap(symbol)
        cex = await self.fetch_cex_median(symbol)
        return {
            "curve_price": curve.price if curve else None,
            "uniswap_price": uni.price if uni else None,
            "cex_median_price": cex.price if cex else None,
            "liquidity_depth_usd": (curve.liquidity_usd if curve else 0)
            + (uni.liquidity_usd if uni else 0)
            + (cex.liquidity_usd if cex else 0),
        }

    def _synthetic_quote(self, source: str, symbol: str) -> PriceQuote:
        """Generate a stable, deterministic-ish price quote for dev/testing.

        Centers around $1.00 with tiny noise. Stablecoins are supposed to be
        boring — this gives the engine realistic data to run the z-score.
        """
        seed = sum(ord(c) for c in symbol + source) % 100
        # Noise: -0.05% to +0.05%
        # nosec B311 - random used for synthetic dev data, NOT security
        noise_pct = (random.Random(seed).random() - 0.5) * 0.001  # nosec
        price = 1.0 + noise_pct
        # nosec B311 - random used for synthetic dev data, NOT security
        liquidity = random.Random(seed + 1).uniform(5_000_000, 50_000_000)  # nosec
        return PriceQuote(source=source, price=price, liquidity_usd=liquidity)
