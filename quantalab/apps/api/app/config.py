"""Application configuration."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "QuantaLab API"
    sentry_dsn: str | None = None
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./quantalab.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3003"]
    stripe_secret_key: str | None = None
    e2b_api_key: str = ""
    auth_bypass: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
