"""Savings routes."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.savings import Savings
from app.schemas.savings import SavingsRead

router = APIRouter()


@router.get("", response_model=list[SavingsRead])
async def list_savings(
    db: Annotated[AsyncSession, Depends(get_db)],
    account_id: uuid.UUID | None = None,
) -> list[SavingsRead]:
    stmt = select(Savings).order_by(Savings.period_start.desc())
    if account_id:
        stmt = stmt.where(Savings.account_id == account_id)
    res = await db.execute(stmt)
    return [SavingsRead.model_validate(s) for s in res.scalars()]


@router.get("/summary")
async def savings_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    res = await db.execute(select(Savings))
    rows = list(res.scalars())
    total = round(sum(s.verified_savings for s in rows), 2)
    by_service: dict[str, float] = {}
    for s in rows:
        by_service[s.service] = by_service.get(s.service, 0.0) + s.verified_savings
    return {
        "total_verified_savings": total,
        "by_service": dict(sorted(by_service.items(), key=lambda x: -x[1])),
        "periods": len(rows),
    }
