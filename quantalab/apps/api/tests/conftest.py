"""Pytest fixtures."""
from __future__ import annotations

import os
os.environ.setdefault("ENVIRONMENT", "test")

import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    from httpx import ASGITransport, AsyncClient
    from app.main import app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
