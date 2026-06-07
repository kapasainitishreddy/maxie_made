"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api import api_router
from app.config import get_settings
from app.core.errors import AppError
from app.core.logging import configure_logging, get_logger
from app.core.sentry import init_sentry
from app.schemas.common import HealthResponse


settings = get_settings()
configure_logging("INFO" if not settings.debug else "DEBUG")
log = get_logger("pharmaip")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    log.info("startup", env=settings.environment, version=__version__)
    # Auto-create tables on startup (dev convenience). For prod, use Alembic.
    from app.db import engine, Base
    import app.models  # noqa: F401  ensure all models are registered
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("tables created")
    # Seed sample data on first run (dev convenience)
    from app.db import AsyncSessionLocal
    from app.models.patent import Patent
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(select(Patent).limit(1))
        if not result.scalar():
            from datetime import date
            import uuid as _uuid
            sample = [
                Patent(id=_uuid.uuid4(), org_id=None, patent_number="US11234567B2", jurisdiction="US",
                       title="Anti-PD-1 antibody for cancer immunotherapy",
                       abstract="A monoclonal antibody targeting PD-1 for use in treating melanoma and lung cancer.",
                       assignee="Merck Sharp & Dohme", inventors=["John Smith", "Jane Doe"],
                       ipc_classes=["A61K", "C07K"], filing_date=date(2015, 3, 15),
                       grant_date=date(2017, 8, 22), expiration_date=date(2035, 3, 15),
                       therapeutic_area="Oncology", drug_name="Pembrolizumab (Keytruda)"),
                Patent(id=_uuid.uuid4(), org_id=None, patent_number="US10167890B2", jurisdiction="US",
                       title="TNF-alpha inhibitor for autoimmune diseases",
                       abstract="Recombinant monoclonal antibody for blocking TNF-alpha in rheumatoid arthritis.",
                       assignee="AbbVie Inc.", inventors=["Alice Johnson", "Bob Wilson"],
                       ipc_classes=["A61K", "C07K"], filing_date=date(2010, 5, 20),
                       grant_date=date(2012, 11, 14), expiration_date=date(2030, 5, 20),
                       therapeutic_area="Immunology", drug_name="Adalimumab (Humira)"),
            ]
            session.add_all(sample)
            await session.commit()
            log.info("seeded sample patents", count=len(sample))
    yield
    log.info("shutdown")


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    debug=settings.debug,
    lifespan=lifespan,
)

# Initialize Sentry (no-op if SENTRY_DSN is not set)
if hasattr(settings, "sentry_dsn") and settings.sentry_dsn:
    init_sentry(settings.sentry_dsn, environment=settings.environment, release=getattr(settings, "version", None))

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Install security middleware (rate limit + security headers)
from app.core.security_middleware import add_security_middleware
add_security_middleware(app)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        version=__version__,
        env=settings.environment,
    )


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {
        "name": settings.app_name,
        "version": __version__,
        "docs": "/docs",
    }
