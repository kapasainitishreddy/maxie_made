"""Stablecoin schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StablecoinBase(BaseModel):
    symbol: str = Field(min_length=1, max_length=16, pattern=r"^[A-Z0-9]+$")
    name: str = Field(min_length=1, max_length=128)
    issuer: str = Field(min_length=1, max_length=128)
    category: str = Field(default="fiat-backed", max_length=32)
    peg_currency: str = Field(default="USD", max_length=8)
    chain: str = Field(default="ethereum", max_length=32)
    contract_address: str | None = Field(default=None, max_length=64)
    market_cap_usd: float = Field(default=0.0, ge=0)
    circulating_supply: float = Field(default=0.0, ge=0)
    tier: int = Field(default=1, ge=1, le=3)


class StablecoinCreate(StablecoinBase):
    pass


class StablecoinRead(StablecoinBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
