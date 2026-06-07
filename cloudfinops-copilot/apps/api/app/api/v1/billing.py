"""Billing routes."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


@router.get("/plans")
async def list_plans() -> list[dict]:
    return [
        {
            "id": "audit",
            "name": "Audit",
            "price": 499,
            "interval": "month",
            "description": "One-time savings audit + monthly report",
            "features": ["1 cloud account", "Monthly audit", "PDF savings report", "Email support"],
        },
        {
            "id": "performance",
            "name": "Performance (20% of savings)",
            "price": None,
            "interval": "month",
            "description": "20% of verified monthly savings, $0 base",
            "features": [
                "Unlimited accounts",
                "Continuous scanning",
                "Auto-generated Terraform PRs",
                "Slack approval flow",
                "Verified savings tracking",
                "Priority support",
            ],
        },
    ]


class CheckoutRequest(BaseModel):
    plan: str


@router.post("/checkout")
async def create_checkout(body: CheckoutRequest) -> dict:
    return {
        "url": f"https://app.cloudfinops-copilot.com/billing/success?plan={body.plan}&demo=1",
        "id": "demo_session",
    }
