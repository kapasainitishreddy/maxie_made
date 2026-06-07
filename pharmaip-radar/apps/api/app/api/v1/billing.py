"""Billing (Stripe) routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from pydantic import BaseModel

from app.config import get_settings
from app.core.security import CurrentUserDep
from app.services.stripe import StripeClient

router = APIRouter()


class CheckoutRequest(BaseModel):
    plan: str  # "starter" | "pro" | "enterprise"


@router.post("/checkout")
async def create_checkout(
    body: CheckoutRequest,
    user: CurrentUserDep,
) -> dict:
    s = get_settings()
    price_map = {
        "starter": s.stripe_price_starter,
        "pro": s.stripe_price_pro,
        "enterprise": s.stripe_price_enterprise,
    }
    price_id = price_map.get(body.plan)
    if not price_id:
        return {"error": f"unknown plan: {body.plan}"}, 400
    client = StripeClient(s.stripe_secret_key)
    session = client.create_checkout_session(
        price_id=price_id,
        customer_email=user.email,
        success_url="https://app.pharmaip-radar.com/billing/success",
        cancel_url="https://app.pharmaip-radar.com/pricing",
        org_id=user.org_id,
    )
    return session


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

    # In real app: dispatch on event["type"] to update org subscription
    return {"received": True, "type": event.get("type")}


@router.get("/plans")
async def list_plans() -> list[dict]:
    return [
        {
            "id": "starter",
            "name": "Starter",
            "price": 999,
            "interval": "month",
            "features": [
                "5,000 patent searches / month",
                "3 saved landscapes",
                "1 watchlist",
                "Email alerts",
            ],
        },
        {
            "id": "pro",
            "name": "Pro",
            "price": 2499,
            "interval": "month",
            "features": [
                "50,000 patent searches / month",
                "Unlimited landscapes",
                "10 watchlists",
                "Infringement alerts",
                "PDF reports",
                "Priority support",
            ],
        },
        {
            "id": "enterprise",
            "name": "Enterprise",
            "price": 4999,
            "interval": "month",
            "features": [
                "Unlimited searches",
                "Unlimited everything",
                "API access",
                "SSO + audit logs",
                "Custom integrations",
                "Dedicated CSM",
            ],
        },
    ]
