"""Recommendation schemas."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.recommendation import RecommendationStatus, RecommendationType, RiskLevel


class RecommendationRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    account_id: uuid.UUID
    resource_id: str
    resource_type: str
    rec_type: RecommendationType
    title: str
    description: str
    current_cost: float
    projected_cost: float
    monthly_savings: float
    risk: RiskLevel
    status: RecommendationStatus
    terraform_hcl: str
    evidence: dict
    created_at: datetime
    updated_at: datetime | None = None
