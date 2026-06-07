"""Report schemas."""

from __future__ import annotations

import enum
import uuid

from pydantic import BaseModel, Field


class ReportType(str, enum.Enum):
    FTO = "fto"
    LANDSCAPE = "landscape"
    INFRINGEMENT = "infringement"
    PATENTABILITY = "patentability"


class ReportStatus(str, enum.Enum):
    QUEUED = "queued"
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"


class ReportCreate(BaseModel):
    report_type: ReportType
    title: str = Field(min_length=1, max_length=300)
    query: dict = Field(default_factory=dict)
    patent_ids: list[uuid.UUID] = Field(default_factory=list)
    target_drug: str | None = None


class ReportRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    report_type: ReportType
    title: str
    status: ReportStatus
    query: dict
    content: dict
    pdf_path: str | None
    error: str | None
    created_at: str
