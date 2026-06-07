"""Application configuration. Uses Pydantic Settings for env-based config.

CRITICAL: keep a blank line between string fields and the @lru_cache decorator
below. If they merge into one line, you'll get a SyntaxError on startup.
"""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Core
    app_name: str = "PegWatch API"
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite+aiosqlite:///./pegwatch.db"

    # Auth (Clerk) — None = dev bypass mode
    clerk_secret_key: str | None = None
    clerk_publishable_key: str | None = None
    allow_dev_auth: bool = True

    # Stripe billing — None = dev bypass
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_price_pro: str | None = None
    stripe_price_api: str | None = None

    # Ollama local LLM for incident summaries
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"

    # Alert delivery (all optional)
    telegram_bot_token: str | None = None
    discord_webhook_url: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    alert_from_email: str = "alerts@pegwatch.dev"

    # Security
    secret_key: str | None = None
    allowed_origins: str = "http://localhost:3004,https://pegwatch.dev"

    # Observability
    sentry_dsn: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
