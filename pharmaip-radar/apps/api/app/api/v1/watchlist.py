"""Watchlist API routes."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUserDep
from app.db import get_db
from app.models.patent import Patent
from app.models.watchlist import InfringementAlert, Watchlist
from app.schemas.watchlist import (
    InfringementAlertRead,
    WatchlistCreate,
    WatchlistRead,
    WatchlistUpdate,
)
from app.services.infringement import InfringementAnalyzer

router = APIRouter()


@router.get("", response_model=list[WatchlistRead])
async def list_watchlists(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> list[WatchlistRead]:
    res = await db.execute(select(Watchlist).order_by(Watchlist.created_at.desc()))
    out: list[WatchlistRead] = []
    for w in res.scalars():
        n = len(w.alerts) if w.alerts else 0
        out.append(WatchlistRead(
            id=w.id,
            name=w.name,
            description=w.description,
            target_company=w.target_company,
            target_drug=w.target_drug,
            keywords=w.keywords or [],
            patent_ids=w.patent_ids or [],
            active=w.active,
            alert_count=n,
            created_at=w.created_at.isoformat(),
        ))
    return out


@router.post("", response_model=WatchlistRead, status_code=201)
async def create_watchlist(
    body: WatchlistCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> WatchlistRead:
    w = Watchlist(
        org_id=uuid.uuid4(),
        name=body.name,
        description=body.description,
        target_company=body.target_company,
        target_drug=body.target_drug,
        keywords=body.keywords,
        patent_ids=body.patent_ids,
    )
    db.add(w)
    await db.flush()
    return WatchlistRead(
        id=w.id,
        name=w.name,
        description=w.description,
        target_company=w.target_company,
        target_drug=w.target_drug,
        keywords=w.keywords or [],
        patent_ids=w.patent_ids or [],
        active=w.active,
        alert_count=0,
        created_at=w.created_at.isoformat(),
    )


@router.get("/{watchlist_id}", response_model=WatchlistRead)
async def get_watchlist(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    watchlist_id: uuid.UUID,
) -> WatchlistRead:
    w = await db.get(Watchlist, watchlist_id)
    if not w:
        raise NotFoundError("Watchlist not found")
    return WatchlistRead(
        id=w.id,
        name=w.name,
        description=w.description,
        target_company=w.target_company,
        target_drug=w.target_drug,
        keywords=w.keywords or [],
        patent_ids=w.patent_ids or [],
        active=w.active,
        alert_count=len(w.alerts) if w.alerts else 0,
        created_at=w.created_at.isoformat(),
    )


@router.patch("/{watchlist_id}", response_model=WatchlistRead)
async def update_watchlist(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    watchlist_id: uuid.UUID,
    body: WatchlistUpdate,
) -> WatchlistRead:
    w = await db.get(Watchlist, watchlist_id)
    if not w:
        raise NotFoundError("Watchlist not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(w, k, v)
    await db.flush()
    return WatchlistRead(
        id=w.id,
        name=w.name,
        description=w.description,
        target_company=w.target_company,
        target_drug=w.target_drug,
        keywords=w.keywords or [],
        patent_ids=w.patent_ids or [],
        active=w.active,
        alert_count=len(w.alerts) if w.alerts else 0,
        created_at=w.created_at.isoformat(),
    )


@router.delete("/{watchlist_id}", status_code=204)
async def delete_watchlist(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    watchlist_id: uuid.UUID,
) -> None:
    w = await db.get(Watchlist, watchlist_id)
    if not w:
        raise NotFoundError("Watchlist not found")
    await db.delete(w)


@router.post("/{watchlist_id}/scan")
async def scan_watchlist(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    watchlist_id: uuid.UUID,
) -> dict:
    """Run an infringement scan against the watchlist's target patents."""
    w = await db.get(Watchlist, watchlist_id)
    if not w:
        raise NotFoundError("Watchlist not found")

    # For each patent in watchlist, compare against all other patents in DB
    target_ids = [uuid.UUID(p) for p in (w.patent_ids or []) if p]
    if not target_ids:
        return {"alerts_created": 0, "scanned": 0, "message": "No patents in watchlist"}

    targets = []
    for pid in target_ids:
        p = await db.get(Patent, pid)
        if p:
            targets.append(p)

    if not targets:
        return {"alerts_created": 0, "scanned": 0, "message": "Watchlist patents not found"}

    # Get candidate set: patents with same drug or therapeutic area, or matching keywords
    stmt = select(Patent)
    conditions = []
    if w.target_drug:
        conditions.append(Patent.drug_name.ilike(f"%{w.target_drug}%"))
    if w.keywords:
        for kw in w.keywords[:3]:
            conditions.append(
                Patent.title.ilike(f"%{kw}%") | Patent.abstract.ilike(f"%{kw}%")
            )
    if conditions:
        from sqlalchemy import or_
        stmt = stmt.where(or_(*conditions))
    candidates = (await db.execute(stmt)).scalars().unique().all()

    analyzer = InfringementAnalyzer()
    created = 0
    for t in targets:
        t_claims = [
            {
                "claim_number": c.claim_number,
                "text": c.text,
                "is_independent": c.is_independent,
            }
            for c in (t.claims or [])
        ]
        if not t_claims:
            continue
        for c in candidates:
            if c.id == t.id:
                continue
            c_claims = [
                {
                    "claim_number": cc.claim_number,
                    "text": cc.text,
                    "is_independent": cc.is_independent,
                }
                for cc in (c.claims or [])
            ]
            if not c_claims:
                continue
            assessment = analyzer.assess(t_claims, c_claims)
            if assessment["risk_score"] >= 0.30:
                alert = InfringementAlert(
                    watchlist_id=w.id,
                    patent_id=t.id,
                    matched_patent_id=c.id,
                    severity=assessment["severity"],
                    risk_score=assessment["risk_score"],
                    claim_chart={"entries": assessment["claim_chart"]},
                    evidence=assessment["evidence"],
                    summary=analyzer.explain(assessment),
                )
                db.add(alert)
                created += 1

    await db.flush()
    return {"alerts_created": created, "scanned": len(targets), "candidates_considered": len(candidates)}


@router.get("/{watchlist_id}/alerts", response_model=list[InfringementAlertRead])
async def list_alerts(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    watchlist_id: uuid.UUID,
) -> list[InfringementAlertRead]:
    res = await db.execute(
        select(InfringementAlert)
        .where(InfringementAlert.watchlist_id == watchlist_id)
        .order_by(InfringementAlert.risk_score.desc())
    )
    return [InfringementAlertRead.model_validate(a) for a in res.scalars()]
