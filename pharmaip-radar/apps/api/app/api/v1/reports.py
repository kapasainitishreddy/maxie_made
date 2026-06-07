"""Report API routes."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUserDep
from app.db import get_db
from app.models.landscape import Landscape
from app.models.patent import Patent
from app.models.report import Report, ReportStatus, ReportType
from app.models.watchlist import InfringementAlert, Watchlist
from app.schemas.report import ReportCreate, ReportRead
from app.services.landscape import LandscapeAnalyzer
from app.services.report import ReportBuilder

router = APIRouter()


@router.get("", response_model=list[ReportRead])
async def list_reports(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> list[ReportRead]:
    res = await db.execute(select(Report).order_by(Report.created_at.desc()))
    return [ReportRead.model_validate(r) for r in res.scalars()]


@router.post("", response_model=ReportRead, status_code=201)
async def create_report(
    body: ReportCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
) -> ReportRead:
    r = Report(
        org_id=uuid.uuid4(),
        report_type=body.report_type,
        title=body.title,
        status=ReportStatus.QUEUED,
        query={
            **body.query,
            "target_drug": body.target_drug,
            "patent_ids": [str(p) for p in body.patent_ids],
        },
    )
    db.add(r)
    await db.flush()

    # Generate inline (sync mode for MVP)
    builder = ReportBuilder()
    try:
        if body.report_type == ReportType.LANDSCAPE:
            stmt = select(Patent)
            if body.target_drug:
                stmt = stmt.where(Patent.drug_name.ilike(f"%{body.target_drug}%"))
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
            analysis = LandscapeAnalyzer(patents_dicts).analyze()
            pdf = builder.build_fto_report(
                body.title, body.target_drug, analysis.model_dump(), []
            )
            r.content = analysis.model_dump()
        elif body.report_type == ReportType.FTO:
            stmt = select(Patent)
            if body.target_drug:
                stmt = stmt.where(Patent.drug_name.ilike(f"%{body.target_drug}%"))
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
            analysis = LandscapeAnalyzer(patents_dicts).analyze()
            # Pull alerts for this org's watchlists
            alerts_res = await db.execute(select(InfringementAlert).limit(20))
            alerts_data = [
                {
                    "risk_score": a.risk_score,
                    "severity": a.severity.value,
                    "summary": a.summary,
                }
                for a in alerts_res.scalars()
            ]
            pdf = builder.build_fto_report(
                body.title, body.target_drug, analysis.model_dump(), alerts_data
            )
            r.content = {"analysis": analysis.model_dump(), "alerts": alerts_data}
        else:
            pdf = builder.build_fto_report(body.title, body.target_drug, {}, [])

        r.pdf_path = f"reports/{r.id}.pdf"
        r.status = ReportStatus.READY
        # Store PDF in memory (in prod, S3 or local fs)
        from app.api.v1.reports import _pdf_cache
        _pdf_cache[str(r.id)] = pdf
    except Exception as exc:
        r.status = ReportStatus.FAILED
        r.error = str(exc)

    return ReportRead.model_validate(r)


# In-memory PDF cache (replace with S3 in prod)
_pdf_cache: dict[str, bytes] = {}


@router.get("/{report_id}", response_model=ReportRead)
async def get_report(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    report_id: uuid.UUID,
) -> ReportRead:
    r = await db.get(Report, report_id)
    if not r:
        raise NotFoundError("Report not found")
    return ReportRead.model_validate(r)


@router.get("/{report_id}/pdf")
async def download_pdf(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: CurrentUserDep,
    report_id: uuid.UUID,
) -> Response:
    r = await db.get(Report, report_id)
    if not r:
        raise NotFoundError("Report not found")
    if r.status != ReportStatus.READY:
        return Response(status_code=409, content=f"Report status: {r.status.value}")
    pdf = _pdf_cache.get(str(r.id))
    if not pdf:
        # regenerate if missing
        builder = ReportBuilder()
        pdf = builder.build_fto_report(r.title, None, r.content, [])
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{r.title}.pdf"'},
    )
