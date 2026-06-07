"""Application configuration."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "PharmaIP Radar API"
    sentry_dsn: str | None = None
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    # Default to SQLite for zero-setup local dev. Set DATABASE_URL=postgresql+asyncpg://...
    # in .env to use Postgres in production.
    database_url: str = "sqlite+aiosqlite:///./pharmaip.db"
    redis_url: str = "redis://localhost:6379/0"
    clerk_secret_key: str | None = None
    clerk_publishable_key: str = ""
    clerk_jwks_url: str = "https://api.clerk.com/v1/jwks"
    cors_origins: list[str] = ["http://localhost:3000"]
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str = ""
    stripe_price_starter: str | None = None
    stripe_price_pro: str | None = None
    stripe_price_enterprise: str | None = None
    # Set AUTH_BYPASS=true in dev to skip Clerk auth. NEVER use in prod.
    auth_bypass: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
