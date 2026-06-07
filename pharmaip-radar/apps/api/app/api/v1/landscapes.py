"""Landscape API routes."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUserDep
from app.db import get_db
from app.models.landscape import Landscape
from app.models.patent import Patent
from app.schemas.landscape import (
    LandscapeAnalysis,
    LandscapeCreate,
    LandscapeRead,
    LandscapeSummary,
)
from app.services.landscape import LandscapeAnalyzer

router = APIRouter()


def _serialize_summary(l: Landscape, count: int) -> LandscapeSummary:
    return LandscapeSummary(
        id=l.id,
        name=l.name,
        description=l.description,
        status=l.status,
        patent_count=count,
        created_at=l.created_at.isoformat(),
    )


@router.get("", response_model=list[LandscapeSummary])
async def list_landscapes(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> list[LandscapeSummary]:
    res = await db.execute(select(Landscape).order_by(Landscape.created_at.desc()))
    out: list[LandscapeSummary] = []
    for l in res.scalars():
        out.append(_serialize_summary(l, 0))
    return out


@router.post("", response_model=LandscapeSummary, status_code=201)
async def create_landscape(
    body: LandscapeCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> LandscapeSummary:
    l = Landscape(
        org_id=uuid.uuid4(),  # In real flow, from user's active org
        name=body.name,
        description=body.description,
        query={
            "therapeutic_area": body.therapeutic_area,
            "drug_name": body.drug_name,
            "keywords": body.keywords,
            **body.query,
        },
        status="pending",
    )
    db.add(l)
    await db.flush()
    return _serialize_summary(l, 0)


@router.get("/{landscape_id}", response_model=LandscapeRead)
async def get_landscape(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    landscape_id: uuid.UUID,
) -> LandscapeRead:
    l = await db.get(Landscape, landscape_id)
    if not l:
        raise NotFoundError("Landscape not found")
    return LandscapeRead.model_validate(l)


@router.get("/{landscape_id}/analysis", response_model=LandscapeAnalysis)
async def get_landscape_analysis(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    landscape_id: uuid.UUID,
) -> LandscapeAnalysis:
    l = await db.get(Landscape, landscape_id)
    if not l:
        raise NotFoundError("Landscape not found")
    # Collect all patents in the landscape's query
    stmt = select(Patent)
    q = l.query or {}
    if q.get("therapeutic_area"):
        stmt = stmt.where(Patent.therapeutic_area == q["therapeutic_area"])
    if q.get("drug_name"):
        stmt = stmt.where(Patent.drug_name.ilike(f"%{q['drug_name']}%"))
    if q.get("keywords"):
        for kw in q["keywords"][:3]:
            stmt = stmt.where(
                Patent.title.ilike(f"%{kw}%") | Patent.abstract.ilike(f"%{kw}%")
            )
    rows = (await db.execute(stmt)).scalars().unique().all()
    patents_dicts = [
        {
            "patent_number": p.patent_number,
            "title": p.title,
            "abstract": p.abstract,
            "assignee": p.assignee,
            "drug_name": p.drug_name,
            "filing_date": p.filing_date,
            "ipc_classes": p.ipc_classes or [],
        }
        for p in rows
    ]
    analyzer = LandscapeAnalyzer(patents_dicts)
    return analyzer.analyze()
