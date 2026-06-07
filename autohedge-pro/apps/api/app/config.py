"""Application configuration."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "AutoHedge Pro API"
    sentry_dsn: str | None = None
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./autohedge.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3002"]
    stripe_secret_key: str | None = None
    alpaca_api_key: str = ""
    alpaca_secret_key: str | None = None
    auth_bypass: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
