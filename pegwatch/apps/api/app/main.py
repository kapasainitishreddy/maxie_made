"""FastAPI app entrypoint."""
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app import __version__
from app.api.v1 import api_router
from app.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.security_middleware import SecurityMiddleware
from app.db import AsyncSessionLocal, Base, engine
from app.models import Alert, AlertChannel, PegSnapshot, Stablecoin  # noqa: F401  # register models
from app.schemas.common import HealthResponse

settings = get_settings()
configure_logging(settings.log_level)
log = get_logger("pegwatch")


# Sample data for first-run dev experience.
SEED_STABLECOINS = [
    {
        "symbol": "USDC",
        "name": "USD Coin",
        "issuer": "Circle",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 33_000_000_000,
        "circulating_supply": 33_000_000_000,
        "tier": 1,
    },
    {
        "symbol": "USDT",
        "name": "Tether",
        "issuer": "Tether Limited",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 110_000_000_000,
        "circulating_supply": 110_000_000_000,
        "tier": 1,
    },
    {
        "symbol": "DAI",
        "name": "Dai Stablecoin",
        "issuer": "MakerDAO",
        "category": "crypto-backed",
        "chain": "ethereum",
        "market_cap_usd": 5_300_000_000,
        "circulating_supply": 5_300_000_000,
        "tier": 1,
    },
    {
        "symbol": "FRAX",
        "name": "Frax",
        "issuer": "Frax Finance",
        "category": "algorithmic",
        "chain": "ethereum",
        "market_cap_usd": 650_000_000,
        "circulating_supply": 650_000_000,
        "tier": 2,
    },
    {
        "symbol": "TUSD",
        "name": "TrueUSD",
        "issuer": "TrustToken",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 500_000_000,
        "circulating_supply": 500_000_000,
        "tier": 2,
    },
    {
        "symbol": "USDP",
        "name": "Pax Dollar",
        "issuer": "Paxos",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 400_000_000,
        "circulating_supply": 400_000_000,
        "tier": 2,
    },
    {
        "symbol": "GUSD",
        "name": "Gemini Dollar",
        "issuer": "Gemini",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 80_000_000,
        "circulating_supply": 80_000_000,
        "tier": 3,
    },
    {
        "symbol": "PYUSD",
        "name": "PayPal USD",
        "issuer": "PayPal / Paxos",
        "category": "fiat-backed",
        "chain": "ethereum",
        "market_cap_usd": 700_000_000,
        "circulating_supply": 700_000_000,
        "tier": 2,
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    """Auto-create tables + seed on first run."""
    log.info("startup.begin", version=__version__, env=settings.environment)
    # Import all models so Base.metadata knows about them
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("startup.tables_ready")

    # Seed if empty
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Stablecoin).limit(1))
        if not result.scalar_one_or_none():
            for s in SEED_STABLECOINS:
                session.add(Stablecoin(id=str(uuid.uuid4()), **s))
            await session.commit()
            log.info("startup.seeded", count=len(SEED_STABLECOINS))

    yield
    await engine.dispose()
    log.info("shutdown.complete")


app = FastAPI(
    title="PegWatch API",
    description="Real-time stablecoin depeg early-warning.",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware (order matters: CORS first, then security headers + rate limit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityMiddleware)


@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler so unhandled errors never leak stack traces."""
    log.error("unhandled_exception", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> HealthResponse:
    """Liveness + DB connectivity check."""
    db_status = "ok"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(select(1))
    except Exception as e:
        db_status = f"error: {type(e).__name__}"
    return HealthResponse(
        status="ok",
        version=__version__,
        environment=settings.environment,
        db=db_status,
    )


app.include_router(api_router, prefix=settings.api_v1_prefix)
