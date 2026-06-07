"""Landscape schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.schemas.patent import PatentSummary


class LandscapeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    query: dict = Field(default_factory=dict)
    therapeutic_area: str | None = None
    drug_name: str | None = None
    keywords: list[str] = Field(default_factory=list)


class LandscapePatentRead(BaseModel):
    model_config = {"from_attributes": True}
    patent: PatentSummary
    relevance_score: float
    cluster_label: str | None


class DensityCell(BaseModel):
    ipc_class: str
    year: int
    count: int
    density: float


class AssigneeStat(BaseModel):
    assignee: str
    patent_count: int
    market_share: float


class TechCluster(BaseModel):
    cluster_id: int
    label: str
    size: int
    top_assignees: list[str]
    top_drugs: list[str]


class LandscapeAnalysis(BaseModel):
    total_patents: int
    unique_assignees: int
    filing_trend: dict[int, int] = Field(default_factory=dict)
    density_heatmap: list[DensityCell] = Field(default_factory=list)
    top_assignees: list[AssigneeStat] = Field(default_factory=list)
    tech_clusters: list[TechCluster] = Field(default_factory=list)
    white_space: list[str] = Field(default_factory=list)
    summary: str = ""


class LandscapeSummary(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    description: str | None
    status: str
    patent_count: int
    created_at: str


class LandscapeRead(LandscapeSummary):
    query: dict
    summary: dict
    patents: list[LandscapePatentRead] = []
