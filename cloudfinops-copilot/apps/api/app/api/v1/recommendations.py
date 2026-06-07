"""Recommendation routes."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.errors import NotFoundError
from app.models.recommendation import Recommendation, RecommendationStatus
from app.schemas.recommendation import RecommendationRead

router = APIRouter()


@router.get("", response_model=list[RecommendationRead])
async def list_recommendations(
    db: Annotated[AsyncSession, Depends(get_db)],
    account_id: uuid.UUID | None = None,
    status: RecommendationStatus | None = None,
) -> list[RecommendationRead]:
    stmt = select(Recommendation).order_by(Recommendation.monthly_savings.desc())
    if account_id:
        stmt = stmt.where(Recommendation.account_id == account_id)
    if status:
        stmt = stmt.where(Recommendation.status == status)
    res = await db.execute(stmt)
    return [RecommendationRead.model_validate(r) for r in res.scalars()]


@router.get("/{rec_id}", response_model=RecommendationRead)
async def get_recommendation(
    db: Annotated[AsyncSession, Depends(get_db)],
    rec_id: uuid.UUID,
) -> RecommendationRead:
    r = await db.get(Recommendation, rec_id)
    if not r:
        raise NotFoundError("Recommendation not found")
    return RecommendationRead.model_validate(r)


@router.post("/{rec_id}/approve", response_model=RecommendationRead)
async def approve(
    db: Annotated[AsyncSession, Depends(get_db)],
    rec_id: uuid.UUID,
) -> RecommendationRead:
    r = await db.get(Recommendation, rec_id)
    if not r:
        raise NotFoundError("Recommendation not found")
    r.status = RecommendationStatus.APPROVED
    await db.flush()
    return RecommendationRead.model_validate(r)


@router.post("/{rec_id}/reject", response_model=RecommendationRead)
async def reject(
    db: Annotated[AsyncSession, Depends(get_db)],
    rec_id: uuid.UUID,
) -> RecommendationRead:
    r = await db.get(Recommendation, rec_id)
    if not r:
        raise NotFoundError("Recommendation not found")
    r.status = RecommendationStatus.REJECTED
    await db.flush()
    return RecommendationRead.model_validate(r)
