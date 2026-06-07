"""Pytest fixtures.

Note: Most tests are unit tests and don't require the FastAPI app.
For integration tests, create a separate conftest in tests/integration/.
"""

from __future__ import annotations

import os

os.environ.setdefault("ENVIRONMENT", "test")

import asyncio
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    """Async HTTP client (only used by integration tests)."""
    from httpx import ASGITransport, AsyncClient
    from app.main import app  # lazy import so unit tests don't pull DB
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
