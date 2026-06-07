"""Billing (Stripe) routes. Dev-bypass when STRIPE_SECRET_KEY unset."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from app.config import get_settings
from app.services.stripe import StripeClient

router = APIRouter()


# ----- Plans -----

@router.get("/plans")
async def list_plans() -> list[dict]:
    return [
        {
            "id": "free", "name": "Free", "price": 0, "interval": "month",
            "description": "Paper trading only",
            "features": ["1 portfolio", "$50k paper", "All 12 strategies"],
        },
        {
            "id": "pro", "name": "Pro", "price": 99, "interval": "month",
            "description": "For active retail traders",
            "features": ["Unlimited paper", "Unlimited backtests", "Walk-forward optimization", "Monte Carlo", "Email support"],
        },
        {
            "id": "aum", "name": "AUM", "price": None, "interval": "year",
            "description": "0.5% of AUM (annual) for live trading",
            "features": ["Live trading via Alpaca/IBKR", "Custom strategies", "Dedicated CSM", "SOC2 + audit logs"],
        },
    ]


# ----- Checkout -----

class CheckoutRequest(BaseModel):
    plan: str  # "pro" | "aum"


@router.post("/checkout")
async def create_checkout(body: CheckoutRequest) -> dict:
    s = get_settings()
    price_map = {
        "pro": s.stripe_price_pro,
        "aum": s.stripe_price_aum,
    }
    price_id = price_map.get(body.plan)
    if not price_id:
        # dev fallback: synthesize a demo URL even without price id
        if not s.stripe_secret_key:
            return {
                "url": f"https://app.autohedge-pro.com/billing/success?plan={body.plan}&demo=1",
                "id": "demo_session",
                "dev_mode": True,
            }
        raise HTTPException(status_code=400, detail=f"unknown plan or no price id configured: {body.plan}")
    client = StripeClient(s.stripe_secret_key)
    session = client.create_checkout_session(
        price_id=price_id,
        customer_email="billing@autohedge-pro.com",
        success_url="https://app.autohedge-pro.com/billing/success",
        cancel_url="https://app.autohedge-pro.com/pricing",
    )
    return session


# ----- Customer portal -----

@router.post("/portal")
async def create_portal() -> dict:
    s = get_settings()
    client = StripeClient(s.stripe_secret_key)
    url = client.create_portal_session(
        customer_id="demo_customer",
        return_url="https://app.autohedge-pro.com/dashboard/billing",
    )
    return {"url": url}


# ----- Webhook -----

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str | None, Header(alias="stripe-signature")] = None,
) -> dict:
    """Verify and process Stripe webhook events."""
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
    # Dispatch hook (no-op placeholder: log only)
    return {"received": True, "type": event.get("type")}
