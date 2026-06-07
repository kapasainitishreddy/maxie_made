"""Savings schemas."""
from __future__ import annotations

import uuid
from datetime import date

from pydantic import BaseModel


class SavingsRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    account_id: uuid.UUID
    period_start: date
    period_end: date
    service: str
    raw_cost: float
    baseline_cost: float
    verified_savings: float
    currency: str
