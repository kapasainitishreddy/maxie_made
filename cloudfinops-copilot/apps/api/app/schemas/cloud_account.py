"""Cloud account schemas."""
from __future__ import annotations

import uuid

from pydantic import BaseModel

from app.models.cloud_account import CloudProvider


class CloudAccountCreate(BaseModel):
    provider: CloudProvider
    account_id: str
    account_name: str
    role_arn: str | None = None
    region: str = "us-east-1"


class CloudAccountSummary(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    provider: CloudProvider
    account_id: str
    account_name: str
    region: str
    monthly_cost: float
    resource_count: int
    last_scanned_at: str | None
    active: bool


class CloudAccountRead(CloudAccountSummary):
    config: dict
    created_at: str
