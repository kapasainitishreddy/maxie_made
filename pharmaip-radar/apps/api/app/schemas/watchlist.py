"""Watchlist + alert schemas."""

from __future__ import annotations

import enum
import uuid

from pydantic import BaseModel, Field


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WatchlistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    target_company: str | None = None
    target_drug: str | None = None
    keywords: list[str] = Field(default_factory=list)
    patent_ids: list[str] = Field(default_factory=list)


class WatchlistUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    target_company: str | None = None
    target_drug: str | None = None
    keywords: list[str] | None = None
    patent_ids: list[str] | None = None
    active: bool | None = None


class WatchlistRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    description: str | None
    target_company: str | None
    target_drug: str | None
    keywords: list[str]
    patent_ids: list[str]
    active: bool
    alert_count: int = 0
    created_at: str


class ClaimElementMatch(BaseModel):
    element: str
    matched_text: str
    source: str
    similarity: float


class ClaimChartEntry(BaseModel):
    claim_number: int
    claim_text: str
    matches: list[ClaimElementMatch]
    overall_similarity: float


class InfringementAlertRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    watchlist_id: uuid.UUID
    patent_id: uuid.UUID
    matched_patent_id: uuid.UUID
    severity: RiskLevel
    status: str
    risk_score: float
    claim_chart: list[ClaimChartEntry] = Field(default_factory=list)
    evidence: dict
    summary: str | None
    created_at: str
