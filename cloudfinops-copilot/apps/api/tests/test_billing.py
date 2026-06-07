"""Billing/Stripe route tests.

Tests work in dev-bypass mode (no STRIPE_SECRET_KEY set).
The dev fallback is what makes them safe to run in CI without real Stripe keys.
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_plans_endpoint(client):
    """Plans endpoint should always return a non-empty list."""
    r = await client.get("/api/v1/billing/plans")
    assert r.status_code == 200
    plans = r.json()
    assert isinstance(plans, list)
    assert len(plans) >= 2
    for plan in plans:
        assert "id" in plan
        assert "name" in plan


@pytest.mark.asyncio
async def test_checkout_dev_bypass(client):
    """With no STRIPE_SECRET_KEY, checkout should return a demo URL (dev_mode=True)."""
    plans = (await client.get("/api/v1/billing/plans")).json()
    paid = [p for p in plans if p.get("price") not in (0, None)]
    if not paid:
        pytest.skip("no paid plan available in dev-bypass mode")
    plan_id = paid[0]["id"]
    r = await client.post("/api/v1/billing/checkout", json={"plan": plan_id})
    assert r.status_code == 200, r.text
    body = r.json()
    assert "url" in body
    assert "id" in body


@pytest.mark.asyncio
async def test_webhook_no_signature(client):
    """Webhook with no signature configured should return 200 + reason, not crash."""
    r = await client.post(
        "/api/v1/billing/webhook",
        content=b'{"type": "test"}',
        headers={"content-type": "application/json"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body.get("received") is False
    assert "reason" in body or "error" in body
