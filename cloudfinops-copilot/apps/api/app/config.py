"""Application configuration."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "CloudFinOps Co-Pilot API"
    sentry_dsn: str | None = None
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./cloudfinops.db"
    redis_url: str = "redis://localhost:6379/0"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    cors_origins: list[str] = ["http://localhost:3001"]
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_price_audit: str | None = None
    stripe_price_performance: str | None = None
    auth_bypass: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
