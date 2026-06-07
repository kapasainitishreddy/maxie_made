"""Alert schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AlertChannelCreate(BaseModel):
    channel_type: str = Field(pattern=r"^(telegram|discord|webhook|email)$")
    target: str = Field(min_length=1, max_length=512)
    min_severity: str = Field(default="warning", pattern=r"^(info|warning|critical)$")
    min_deviation_pct: float = Field(default=0.5, ge=0, le=50)
    watched_symbols: str = Field(default="USDC,USDT,DAI", max_length=512)

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str, info) -> str:  # type: ignore[no-untyped-def]
        ch = info.data.get("channel_type")
        if ch == "email" and "@" not in v:
            raise ValueError("email target must contain @")
        if ch == "webhook" and not v.startswith(("http://", "https://")):
            raise ValueError("webhook target must be a URL")
        if ch == "telegram" and not v.lstrip("-").isdigit():
            raise ValueError("telegram target must be a chat_id (digits)")
        return v


class AlertChannelRead(AlertChannelCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    is_active: bool
    created_at: datetime


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    stablecoin_id: str
    triggered_at: datetime
    severity: str
    price_at_trigger: float
    deviation_pct: float
    z_score: float
    title: str
    summary: str | None = None
    ai_summary: str | None = None
    resolved: bool
    notification_count: int = 0
