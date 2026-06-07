"""Billing (Stripe) routes. Dev-bypass when STRIPE_SECRET_KEY unset."""
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
            "id": "researcher", "name": "Researcher", "price": 199, "interval": "month",
            "features": ["10 notebooks", "100 backtests/mo", "NL→code translator", "Community marketplace"],
        },
        {
            "id": "quant", "name": "Quant", "price": 499, "interval": "month",
            "features": ["Unlimited notebooks", "Unlimited backtests", "Walk-forward + Monte Carlo", "Premium marketplace access", "Alpaca paper trading"],
        },
        {
            "id": "pro", "name": "Pro", "price": 999, "interval": "month",
            "features": ["Everything in Quant", "E2B full sandbox", "Live data feeds (Polygon, FRED)", "Custom data sources", "API access", "Priority support"],
        },
    ]


class CheckoutRequest(BaseModel):
    plan: str  # "researcher" | "quant" | "pro"


@router.post("/checkout")
async def create_checkout(body: CheckoutRequest) -> dict:
    s = get_settings()
    price_map = {
        "researcher": s.stripe_price_researcher,
        "quant": s.stripe_price_quant,
        "pro": s.stripe_price_pro,
    }
    price_id = price_map.get(body.plan)
    if not price_id:
        if not s.stripe_secret_key:
            return {
                "url": f"https://app.quantalab.com/billing/success?plan={body.plan}&demo=1",
                "id": "demo_session",
                "dev_mode": True,
            }
        raise HTTPException(status_code=400, detail=f"unknown plan or no price id: {body.plan}")
    client = StripeClient(s.stripe_secret_key)
    session = client.create_checkout_session(
        price_id=price_id,
        customer_email="billing@quantalab.com",
        success_url="https://app.quantalab.com/billing/success",
        cancel_url="https://app.quantalab.com/pricing",
    )
    return session


@router.post("/portal")
async def create_portal() -> dict:
    s = get_settings()
    client = StripeClient(s.stripe_secret_key)
    url = client.create_portal_session(
        customer_id="demo_customer",
        return_url="https://app.quantalab.com/dashboard/billing",
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
