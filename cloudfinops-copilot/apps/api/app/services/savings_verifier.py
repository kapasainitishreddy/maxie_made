"""Savings verifier — measures actual savings post-execution."""
from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.savings import Savings


class SavingsVerifier:
    """Compute verified savings: baseline - actual cost, post-execution."""

    def compute(
        self,
        baseline_cost: float,
        actual_cost: float,
        period_start: date,
        period_end: date,
    ) -> float:
        return round(max(0.0, baseline_cost - actual_cost), 2)

    async def persist(
        self,
        db: AsyncSession,
        account_id: str,
        period_start: date,
        period_end: date,
        service: str,
        raw_cost: float,
        baseline_cost: float,
    ) -> Savings:
        verified = self.compute(baseline_cost, raw_cost, period_start, period_end)
        s = Savings(
            account_id=account_id,
            period_start=period_start,
            period_end=period_end,
            service=service,
            raw_cost=raw_cost,
            baseline_cost=baseline_cost,
            verified_savings=verified,
        )
        db.add(s)
        await db.flush()
        return s

    async def total_savings_mtd(self, db: AsyncSession, account_id: str) -> float:
        from datetime import date
        start_of_month = date.today().replace(day=1)
        res = await db.execute(
            select(Savings).where(
                Savings.account_id == account_id,
                Savings.period_start >= start_of_month,
            )
        )
        return round(sum(s.verified_savings for s in res.scalars()), 2)
