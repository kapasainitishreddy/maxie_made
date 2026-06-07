"""Webhook receivers (Stripe + alert delivery)."""
from __future__ import annotations

import hmac
import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import PlainTextResponse

from app.config import Settings, get_settings
from app.core.logging import get_logger
from app.db import get_db
from app.models.alert import Alert, AlertChannel

router = APIRouter()
log = get_logger("webhooks")


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="stripe-signature"),
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Handle Stripe subscription events. Verifies signature when secret is set."""
    body = await request.body()

    # Dev bypass
    if not settings.stripe_webhook_secret:
        log.info("stripe_webhook.received (no signature verification in dev)", extra={"body_len": len(body)})
        return {"received": True, "dev_mode": True}

    if not stripe_signature:
        return PlainTextResponse("Missing signature", status_code=400)

    # Verify signature
    expected = hmac.new(
        settings.stripe_webhook_secret.encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, stripe_signature):
        return PlainTextResponse("Invalid signature", status_code=400)

    # Parse event
    import json
    event = json.loads(body)
    event_type = event.get("type", "")
    log.info("stripe_webhook.verified", extra={"type": event_type})

    if event_type == "checkout.session.completed":
        # In real prod: look up user, update plan in DB
        # For now, log and return ok
        pass
    return {"received": True, "type": event_type}


@router.post("/alert-delivery/{channel_id}")
async def deliver_alert(
    channel_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Webhook receiver for outgoing alert delivery (e.g. a Telegram bot posting back).
    In production, the alert engine POSTs to this endpoint to dispatch via the
    appropriate channel. Stub for now — real impl dispatches per channel_type."""
    body = await request.json()
    log.info("alert_delivery.received", extra={"channel_id": channel_id, "data": body})
    return {"received": True, "channel_id": channel_id, "ts": datetime.now(timezone.utc).isoformat()}
