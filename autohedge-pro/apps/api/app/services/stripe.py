"""Stripe client wrapper. Dev-mode safe (returns demo URL if no key)."""
from __future__ import annotations

from typing import Any

import stripe


class StripeClient:
    def __init__(self, secret_key: str | None = None) -> None:
        if secret_key:
            stripe.api_key = secret_key
        self._has_key = bool(secret_key)

    def create_checkout_session(
        self,
        price_id: str,
        customer_email: str,
        success_url: str,
        cancel_url: str,
        org_id: str | None = None,
    ) -> dict[str, Any]:
        if not self._has_key:
            return {"url": f"{success_url}?demo=1", "id": "demo_session", "dev_mode": True}
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            customer_email=customer_email,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"org_id": org_id} if org_id else {},
        )
        return {"url": session.url, "id": session.id, "dev_mode": False}

    def create_portal_session(self, customer_id: str, return_url: str) -> str:
        if not self._has_key:
            return f"{return_url}?demo_portal=1"
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return session.url
