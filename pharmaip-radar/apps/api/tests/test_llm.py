"""LLM client tests (mocked HTTP)."""

from __future__ import annotations

import httpx
import pytest
import respx

from app.services.llm import LLMClient


@pytest.mark.asyncio
@respx.mock
async def test_generate_calls_ollama():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(200, json={"response": "Hello world"})
    )
    client = LLMClient(host="http://localhost:11434", model="qwen3:8b")
    out = await client.generate("hi")
    assert out == "Hello world"


@pytest.mark.asyncio
@respx.mock
async def test_generate_returns_empty_on_error():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(500, text="boom")
    )
    client = LLMClient(host="http://localhost:11434", model="qwen3:8b")
    out = await client.generate("hi")
    assert "unavailable" in out.lower()


@pytest.mark.asyncio
@respx.mock
async def test_structured_parses_json_object():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(200, json={"response": 'Here is the JSON: {"key": "value"} done'})
    )
    client = LLMClient(host="http://localhost:11434", model="qwen3:8b")
    out = await client.structured("prompt", "{key: string}")
    assert out == {"key": "value"}


@pytest.mark.asyncio
@respx.mock
async def test_structured_parses_json_array():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(200, json={"response": "[1, 2, 3]"})
    )
    client = LLMClient(host="http://localhost:11434", model="qwen3:8b")
    out = await client.structured("prompt", "array")
    assert out == [1, 2, 3]


@pytest.mark.asyncio
@respx.mock
async def test_structured_falls_back_to_empty_on_garbage():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(200, json={"response": "I cannot produce JSON"})
    )
    client = LLMClient(host="http://localhost:11434", model="qwen3:8b")
    out = await client.structured("prompt", "schema")
    assert out == {}
