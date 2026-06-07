"""Pytest fixtures."""
from __future__ import annotations

import asyncio
import os
import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Force test mode BEFORE importing the app
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ALLOW_DEV_AUTH"] = "true"

from app.config import get_settings  # noqa: E402
from app.db import Base, get_db  # noqa: E402
from app.main import SEED_STABLECOINS, app  # noqa: E402
from app.models.stablecoin import Stablecoin  # noqa: E402

settings = get_settings()


@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the whole test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        import app.models  # noqa: F401

        await conn.run_sync(Base.metadata.create_all)
    # Seed sample data (so endpoints that need stablecoins have them)
    TestSession = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with TestSession() as session:
        result = await session.execute(select(Stablecoin).limit(1))
        if not result.scalar_one_or_none():
            for s in SEED_STABLECOINS:
                session.add(Stablecoin(id=str(uuid.uuid4()), **s))
            await session.commit()
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)
    async with TestSession() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_engine):
    """HTTP client backed by the in-memory test engine with seeded data."""

    async def _override_get_db():
        TestSession = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Warm up the app (no lifespan - we created tables manually)
        await ac.get("/health")
        yield ac
    app.dependency_overrides.clear()
