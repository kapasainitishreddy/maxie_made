"""Ollama LLM client — local, $0."""

from __future__ import annotations

import json
from typing import Any

import httpx


class LLMClient:
    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen3:8b") -> None:
        self.host = host.rstrip("/")
        self.model = model

    async def generate(self, prompt: str, system: str = "", temperature: float = 0.3) -> str:
        """Call /api/generate on the local Ollama instance."""
        body: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            body["system"] = system
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(f"{self.host}/api/generate", json=body)
                r.raise_for_status()
                return r.json().get("response", "")
        except (httpx.HTTPError, ValueError) as exc:
            return f"[LLM unavailable: {exc}]"

    async def structured(self, prompt: str, schema_hint: str, system: str = "") -> dict:
        """Best-effort JSON-structured output. Falls back to {} on parse failure."""
        full_prompt = f"{prompt}\n\nReturn strictly valid JSON matching this schema:\n{schema_hint}"
        raw = await self.generate(full_prompt, system=system, temperature=0.1)
        # Extract first JSON object/array
        for opener, closer in [("{", "}"), ("[", "]")]:
            i = raw.find(opener)
            j = raw.rfind(closer)
            if i != -1 and j != -1 and j > i:
                try:
                    return json.loads(raw[i : j + 1])
                except json.JSONDecodeError:
                    continue
        return {}
