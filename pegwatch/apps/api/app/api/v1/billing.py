"""Stripe billing endpoints (dev bypasses when STRIPE_SECRET_KEY unset)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.core.errors import PlanLimitError
from app.core.security import CurrentUser, get_current_user
from app.services.stripe import StripeClient

router = APIRouter()

PLANS = [
    {
        "id": "free",
        "name": "Free",
        "price_usd": 0,
        "max_stablecoins": 3,
        "alerts": False,
        "api_access": False,
        "features": ["3 stablecoins", "Hourly refresh", "Public dashboard"],
    },
    {
        "id": "pro",
        "name": "Pro",
        "price_usd": 19,
        "max_stablecoins": 25,
        "alerts": True,
        "api_access": False,
        "features": [
            "25+ stablecoins",
            "1-min refresh",
            "Telegram / Discord / email alerts",
            "30-day history",
            "AI incident summaries",
        ],
    },
    {
        "id": "api",
        "name": "API",
        "price_usd": 99,
        "max_stablecoins": 100,
        "alerts": True,
        "api_access": True,
        "features": [
            "100+ stablecoins",
            "Real-time refresh",
            "REST + WebSocket API",
            "Custom stablecoin registration",
            "1-year history export",
            "Priority support",
        ],
    },
]


class CheckoutRequest(BaseModel):
    plan: str  # pro | api
    success_url: str = "https://pegwatch.dev/dashboard?upgraded=1"
    cancel_url: str = "https://pegwatch.dev/pricing"


class CheckoutResponse(BaseModel):
    url: str
    session_id: str
    dev_mode: bool = False


@router.get("/plans")
async def list_plans() -> list[dict]:
    return PLANS


@router.get("/me")
async def my_billing(
    user: CurrentUser = Depends(get_current_user),
) -> dict:
    return {
        "user_id": user.user_id,
        "email": user.email,
        "plan": user.plan,
        "limits": next(p for p in PLANS if p["id"] == user.plan),
    }


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    req: CheckoutRequest,
    user: CurrentUser = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
) -> CheckoutResponse:
    """Create a Stripe checkout session. In dev mode (no Stripe key), returns
    a fake URL that the frontend handles to 'upgrade' the local user."""
    if req.plan not in ("pro", "api"):
        raise PlanLimitError("Invalid plan. Choose 'pro' or 'api'.")

    client = StripeClient(settings.stripe_secret_key)
    price_id = (
        settings.stripe_price_pro if req.plan == "pro" else settings.stripe_price_api
    )

    # Dev bypass: no key, or no price id configured
    if not settings.stripe_secret_key or not price_id:
        return CheckoutResponse(
            url=f"/dashboard?dev_upgrade={req.plan}",
            session_id=f"dev_session_{user.user_id}_{req.plan}",
            dev_mode=True,
        )

    session = client.create_checkout_session(
        price_id=price_id,
        customer_email=user.email,
        success_url=req.success_url,
        cancel_url=req.cancel_url,
        client_reference_id=user.user_id,
    )
    return CheckoutResponse(
        url=session["url"], session_id=session["id"], dev_mode=False
    )


@router.post("/portal")
async def create_portal(
    user: CurrentUser = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
) -> dict:
    """Create a Stripe customer portal session for managing subscription."""
    client = StripeClient(settings.stripe_secret_key)
    url = client.create_portal_session(
        customer_id=user.user_id,  # In real app: look up stripe_customer_id
        return_url="https://pegwatch.dev/dashboard/billing",
    )
    return {"url": url, "dev_mode": not bool(settings.stripe_secret_key)}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str | None, Header(alias="stripe-signature")] = None,
    settings: Settings = Depends(get_settings),
) -> dict:
    """Verify and process Stripe webhook events."""
    if not settings.stripe_webhook_secret or not stripe_signature:
        return {"received": False, "reason": "no signature configured"}
    import stripe
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.stripe_webhook_secret
        )
    except Exception as exc:
        return {"received": False, "error": str(exc)}
    # Dispatch: subscription updates would update user.plan in DB
    return {"received": True, "type": event.get("type")}
