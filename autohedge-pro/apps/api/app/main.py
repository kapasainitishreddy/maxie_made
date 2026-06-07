"""FastAPI app."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app import __version__
from app.api import api_router
from app.config import get_settings
from app.core.errors import AppError
from app.core.sentry import init_sentry
from pydantic import BaseModel

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] creating tables...")
    from app.db import engine, Base, AsyncSessionLocal
    import app.models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[startup] tables created")
    yield


app = FastAPI(title=settings.app_name, version=__version__, lifespan=lifespan)

# Initialize Sentry (no-op if SENTRY_DSN is not set)
if hasattr(settings, "sentry_dsn") and settings.sentry_dsn:
    init_sentry(settings.sentry_dsn, environment=settings.environment, release=getattr(settings, "version", None))
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3002"], allow_methods=["*"], allow_headers=["*"])

# Install security middleware (rate limit + security headers)
from app.core.security_middleware import add_security_middleware
add_security_middleware(app)


@app.exception_handler(AppError)
async def err(req: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"code": exc.code, "message": exc.message})


class Health(BaseModel):
    status: str = "ok"
    app: str
    version: str
    env: str


@app.get("/health")
async def health() -> Health:
    return Health(app=settings.app_name, version=__version__, env=settings.environment)


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root() -> dict:
    return {"name": settings.app_name, "version": __version__}
