"""Patent API routes."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.pagination import PageParams
from app.core.security import CurrentUserDep
from app.db import get_db
from app.models.patent import Patent, PatentStatus
from app.schemas.common import PageResponse
from app.schemas.patent import (
    PatentRead,
    PatentSearchRequest,
    PatentSearchResult,
    PatentSummary,
)
from app.services.uspto import USPTOClient

router = APIRouter()


@router.get("", response_model=PatentSearchResult)
async def list_patents(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    q: str | None = Query(None, description="Free-text query"),
    assignee: str | None = None,
    drug_name: str | None = None,
    therapeutic_area: str | None = None,
    jurisdiction: str | None = None,
    ipc: str | None = Query(None, description="IPC class prefix"),
    status: PatentStatus | None = None,
    filing_from: date | None = None,
    filing_to: date | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
) -> PatentSearchResult:
    stmt = select(Patent)
    if q:
        stmt = stmt.where(Patent.title.ilike(f"%{q}%") | Patent.abstract.ilike(f"%{q}%"))
    if assignee:
        stmt = stmt.where(Patent.assignee.ilike(f"%{assignee}%"))
    if drug_name:
        stmt = stmt.where(Patent.drug_name.ilike(f"%{drug_name}%"))
    if therapeutic_area:
        stmt = stmt.where(Patent.therapeutic_area == therapeutic_area)
    if jurisdiction:
        stmt = stmt.where(Patent.jurisdiction == jurisdiction)
    if status:
        stmt = stmt.where(Patent.status == status)
    if filing_from:
        stmt = stmt.where(Patent.filing_date >= filing_from)
    if filing_to:
        stmt = stmt.where(Patent.filing_date <= filing_to)
    if ipc:
        stmt = stmt.where(Patent.ipc_classes.any(ipc))

    # count
    count_stmt = select(Patent.id).where(*stmt.whereclause.children) if stmt.whereclause is not None else select(Patent.id)  # type: ignore[union-attr]
    total = len((await db.execute(count_stmt)).scalars().all())

    stmt = stmt.order_by(Patent.filing_date.desc().nullslast()).offset((page - 1) * page_size).limit(page_size)
    rows = (await db.execute(stmt)).scalars().unique().all()

    return PatentSearchResult(
        patents=[PatentSummary.model_validate(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{patent_id}", response_model=PatentRead)
async def get_patent(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    patent_id: str,
) -> PatentRead:
    from uuid import UUID
    try:
        pid = UUID(patent_id)
    except ValueError:
        raise NotFoundError("Invalid patent id")
    p = await db.get(Patent, pid)
    if not p:
        raise NotFoundError(f"Patent {patent_id} not found")
    return PatentRead.model_validate(p)


@router.post("/search/external")
async def search_external(
    req: PatentSearchRequest,
    user: CurrentUserDep,
) -> dict:
    """Hit PatentsView for live results — does not persist."""
    from app.config import get_settings
    s = get_settings()
    client = USPTOClient(api_key=s.uspto_api_key)
    results = await client.search_patents(
        query_text=req.query,
        assignee=req.assignees[0] if req.assignees else None,
        drug_name=req.drug_name,
        ipc_class=req.ipc_classes[0] if req.ipc_classes else None,
        limit=req.page_size,
    )
    return {"results": results, "count": len(results)}
