"""AI incident summaries via local Ollama (no cloud cost, no rate limits, no API keys)."""
from __future__ import annotations

import os

import httpx

DEFAULT_TIMEOUT = 30.0


def _is_ollama_reachable(base_url: str) -> bool:
    """Quick health check - is the local Ollama server up?"""
    try:
        with httpx.Client(timeout=2.0) as client:
            r = client.get(f"{base_url}/api/tags")
            return r.status_code == 200
    except (httpx.HTTPError, httpx.TimeoutException, OSError):
        return False


async def summarize_incident(
    symbol: str,
    deviation_pct: float,
    z_score: float,
    price: float,
    base_url: str | None = None,
    model: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> str:
    """Generate a 2-3 sentence plain-English incident summary using local Ollama.

    Falls back to a deterministic template if Ollama is offline (so the UI
    always has something to show).
    """
    base = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    mdl = model or os.getenv("OLLAMA_MODEL", "qwen3:8b")

    prompt = (
        f"You are a financial risk analyst. A stablecoin depeg event was just detected.\n\n"
        f"Asset: {symbol}\n"
        f"Current price: ${price:.4f}\n"
        f"Deviation from peg: {deviation_pct:+.3f}%\n"
        f"Z-score (vs 7d baseline): {z_score:+.2f}\n\n"
        f"Write a 2-3 sentence summary for a treasury team. Be specific, factual, "
        f"and include a recommendation. No marketing language. Avoid filler words."
    )

    if not _is_ollama_reachable(base):
        return _fallback_summary(symbol, deviation_pct, z_score, price)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(
                f"{base}/api/generate",
                json={"model": mdl, "prompt": prompt, "stream": False},
            )
            r.raise_for_status()
            data = r.json()
            return str(data.get("response", "")).strip() or _fallback_summary(
                symbol, deviation_pct, z_score, price
            )
    except (httpx.HTTPError, httpx.TimeoutException, OSError, ValueError):
        return _fallback_summary(symbol, deviation_pct, z_score, price)


def _fallback_summary(symbol: str, dev_pct: float, z: float, price: float) -> str:
    """Deterministic summary used when Ollama is offline or errors."""
    direction = "below" if dev_pct < 0 else "above"
    severity = (
        "critical"
        if abs(z) >= 3.0
        else "warning"
        if abs(z) >= 2.0
        else "elevated"
        if abs(z) >= 1.5
        else "stable"
    )
    return (
        f"{symbol} is trading {direction} peg at ${price:.4f} "
        f"({dev_pct:+.3f}%, z-score {z:+.2f}). "
        f"Conditions are {severity}. "
        f"Recommendation: monitor Curve/USDC pool depth and confirm CEX-DEX price spread "
        f"before initiating new positions."
    )
