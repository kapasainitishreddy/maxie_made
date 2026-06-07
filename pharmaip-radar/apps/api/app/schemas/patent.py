"""Patent schemas."""

from __future__ import annotations

import enum
import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class Jurisdiction(str, enum.Enum):
    US = "US"
    EP = "EP"
    WO = "WO"
    JP = "JP"
    CN = "CN"
    KR = "KR"
    CA = "CA"
    AU = "AU"
    IN = "IN"


THERAPEUTIC_AREAS = [
    "Oncology",
    "Immunology",
    "Neurology",
    "Cardiology",
    "Endocrinology",
    "Infectious Disease",
    "Rare Disease",
    "Ophthalmology",
    "Dermatology",
    "Respiratory",
    "Gastroenterology",
    "Hematology",
]


class TherapeuticArea(str, enum.Enum):
    ONCOLOGY = "Oncology"
    IMMUNOLOGY = "Immunology"
    NEUROLOGY = "Neurology"
    CARDIOLOGY = "Cardiology"
    ENDOCRINOLOGY = "Endocrinology"
    INFECTIOUS_DISEASE = "Infectious Disease"
    RARE_DISEASE = "Rare Disease"
    OPHTHALMOLOGY = "Ophthalmology"
    DERMATOLOGY = "Dermatology"
    RESPIRATORY = "Respiratory"
    GASTROENTEROLOGY = "Gastroenterology"
    HEMATOLOGY = "Hematology"


class PatentClaimRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    claim_number: int
    claim_type: str
    text: str
    is_independent: bool
    depends_on: list[int]


class PatentSummary(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    patent_number: str
    jurisdiction: str
    title: str
    assignee: str | None
    drug_name: str | None
    therapeutic_area: str | None
    status: str
    filing_date: date | None
    grant_date: date | None


class PatentRead(PatentSummary):
    abstract: str | None
    inventors: list[str]
    ipc_classes: list[str]
    expiration_date: date | None
    raw_data: dict
    claims: list[PatentClaimRead] = []


class PatentSearchRequest(BaseModel):
    query: str | None = None
    drug_name: str | None = None
    therapeutic_area: TherapeuticArea | None = None
    jurisdictions: list[Jurisdiction] | None = None
    assignees: list[str] | None = None
    ipc_classes: list[str] | None = None
    filing_date_from: date | None = None
    filing_date_to: date | None = None
    status: Literal["pending", "granted", "expired", "abandoned", "withdrawn"] | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)


class PatentSearchResult(BaseModel):
    patents: list[PatentSummary]
    total: int
    page: int
    page_size: int
    facets: dict = Field(default_factory=dict)
