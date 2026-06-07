"""Billing routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from app.config import get_settings
from app.services.stripe import StripeClient

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
    s = get_settings()
    price_map = {
        "audit": s.stripe_price_audit,
        "performance": s.stripe_price_performance,
    }
    price_id = price_map.get(body.plan)
    if not price_id and not s.stripe_secret_key:
        return {
            "url": f"https://app.cloudfinops-copilot.com/billing/success?plan={body.plan}&demo=1",
            "id": "demo_session",
            "dev_mode": True,
        }
    if not price_id:
        raise HTTPException(status_code=400, detail=f"unknown plan or no price id: {body.plan}")
    client = StripeClient(s.stripe_secret_key)
    session = client.create_checkout_session(
        price_id=price_id,
        customer_email="billing@cloudfinops-copilot.com",
        success_url="https://app.cloudfinops-copilot.com/billing/success",
        cancel_url="https://app.cloudfinops-copilot.com/pricing",
    )
    return session


@router.post("/portal")
async def create_portal() -> dict:
    s = get_settings()
    client = StripeClient(s.stripe_secret_key)
    url = client.create_portal_session(
        customer_id="demo_customer",
        return_url="https://app.cloudfinops-copilot.com/dashboard/billing",
    )
    return {"url": url}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str | None, Header(alias="stripe-signature")] = None,
) -> dict:
    s = get_settings()
    if not s.stripe_webhook_secret or not stripe_signature:
        return {"received": False, "reason": "no signature configured"}
    import stripe
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, s.stripe_webhook_secret
        )
    except Exception as exc:
        return {"received": False, "error": str(exc)}
    return {"received": True, "type": event.get("type")}
