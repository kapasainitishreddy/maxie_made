"""NL → Python code translator via Ollama."""
from __future__ import annotations

import httpx


class NL2Code:
    """Translate natural-language strategy descriptions to Python code via local Ollama."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen3:8b") -> None:
        self.host = host.rstrip("/")
        self.model = model

    async def translate(self, description: str) -> str:
        """Return Python code with a signals(prices) function."""
        code_block = "def signals(prices): return [{timestamp: prices.index[0], side: buy}] if len(prices) else []"
        prompt = (
            "You are a quant researcher. Convert this strategy description to Python code.\n\n"
            f"Description: {description}\n\n"
            "Return ONLY Python code (no markdown, no explanation). The code must:\n"
            "1. Define a function `signals(prices)` where prices is a pandas Series of close prices\n"
            "2. The function should return a list of dicts: [{timestamp: pd.Timestamp, side: buy or sell}, ...]\n"
            "3. Use only pandas and numpy. No imports needed (they're pre-loaded as `pd` and `np`).\n"
            "4. The strategy should be sensible and implement what was described.\n\n"
            "Example:\n"
            "def signals(prices):\n"
            "    fast = prices.rolling(20).mean()\n"
            "    slow = prices.rolling(50).mean()\n"
            "    out = []\n"
            "    for i in range(1, len(prices)):\n"
            "        if pd.isna(fast.iloc[i]) or pd.isna(slow.iloc[i]):\n"
            "            continue\n"
            "        if fast.iloc[i-1] <= slow.iloc[i-1] and fast.iloc[i] > slow.iloc[i]:\n"
            '            out.append({"timestamp": prices.index[i], "side": "buy"})\n'
            "        elif fast.iloc[i-1] >= slow.iloc[i-1] and fast.iloc[i] < slow.iloc[i]:\n"
            '            out.append({"timestamp": prices.index[i], "side": "sell"})\n'
            "    return out\n\n"
            f"Now write code for: {description}\n"
        )
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(
                    f"{self.host}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}},
                )
                r.raise_for_status()
                return self._clean(r.json().get("response", ""))
        except Exception as e:
            return (
                f"# Error: {e}\n"
                "# Falling back to buy & hold\n"
                "def signals(prices):\n"
                '    return [{"timestamp": prices.index[0], "side": "buy"}] if len(prices) else []\n'
            )

    def _clean(self, raw: str) -> str:
        """Strip markdown code fences if present."""
        raw = raw.strip()
        if raw.startswith("```python"):
            raw = raw[len("```python"):]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        return raw.strip()
