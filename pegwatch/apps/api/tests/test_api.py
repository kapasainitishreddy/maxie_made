"""Tests for the FastAPI app endpoints."""
import pytest


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert body["db"] == "ok"


@pytest.mark.asyncio
async def test_list_stablecoins_seeded(client):
    r = await client.get("/api/v1/stablecoins", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    coins = r.json()
    assert len(coins) >= 7
    symbols = {c["symbol"] for c in coins}
    assert "USDC" in symbols
    assert "USDT" in symbols
    assert "DAI" in symbols


@pytest.mark.asyncio
async def test_list_stablecoins_free_tier_filter(client):
    """Free tier should only see tier-1 coins by default."""
    r = await client.get("/api/v1/stablecoins?tier=1", headers={"Authorization": "Bearer dev:bob:free"})
    assert r.status_code == 200
    coins = r.json()
    for c in coins:
        assert c["tier"] == 1


@pytest.mark.asyncio
async def test_get_stablecoin(client):
    r = await client.get("/api/v1/stablecoins/USDC", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    assert r.json()["symbol"] == "USDC"


@pytest.mark.asyncio
async def test_get_stablecoin_404(client):
    r = await client.get("/api/v1/stablecoins/FAKEXYZ", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_stablecoin_pro_blocked(client):
    """Pro plan cannot create custom stablecoins (API tier only)."""
    r = await client.post(
        "/api/v1/stablecoins",
        json={
            "symbol": "TEST",
            "name": "Test Coin",
            "issuer": "Test Inc",
            "category": "fiat-backed",
            "chain": "ethereum",
            "market_cap_usd": 0,
            "circulating_supply": 0,
            "tier": 1,
        },
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 402


@pytest.mark.asyncio
async def test_peg_status_unknown_symbol(client):
    r = await client.get("/api/v1/peg/UNKNOWN/status", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_peg_status_seeded_coin(client):
    r = await client.get("/api/v1/peg/USDC/status", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    body = r.json()
    assert body["symbol"] == "USDC"
    assert "price_usd" in body
    assert "severity" in body
    assert body["severity"] in ("healthy", "watch", "warning", "critical")


@pytest.mark.asyncio
async def test_peg_status_all(client):
    r = await client.get("/api/v1/peg/status", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) >= 3
    for entry in body:
        assert "symbol" in entry
        assert "severity" in entry


@pytest.mark.asyncio
async def test_peg_history(client):
    r = await client.get("/api/v1/peg/USDC/history?hours=24", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    body = r.json()
    assert body["symbol"] == "USDC"
    assert "points" in body
    assert "mean_7d" in body
    assert "stddev_7d" in body


@pytest.mark.asyncio
async def test_refresh_snapshot_free_blocked(client):
    r = await client.post(
        "/api/v1/peg/USDC/refresh",
        headers={"Authorization": "Bearer dev:bob:free"},
    )
    assert r.status_code == 402


@pytest.mark.asyncio
async def test_refresh_snapshot_pro_works(client):
    r = await client.post(
        "/api/v1/peg/USDC/refresh",
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["symbol"] == "USDC"
    assert "price_usd" in body


@pytest.mark.asyncio
async def test_alert_channels_free_blocked(client):
    r = await client.post(
        "/api/v1/alerts/channels",
        json={"channel_type": "telegram", "target": "123456"},
        headers={"Authorization": "Bearer dev:bob:free"},
    )
    assert r.status_code == 402


@pytest.mark.asyncio
async def test_alert_channels_pro_works(client):
    r = await client.post(
        "/api/v1/alerts/channels",
        json={"channel_type": "telegram", "target": "123456789", "min_severity": "warning"},
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["channel_type"] == "telegram"
    assert body["target"] == "123456789"


@pytest.mark.asyncio
async def test_alert_channels_invalid_email(client):
    r = await client.post(
        "/api/v1/alerts/channels",
        json={"channel_type": "email", "target": "not-an-email"},
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_alert_channels_invalid_webhook(client):
    r = await client.post(
        "/api/v1/alerts/channels",
        json={"channel_type": "webhook", "target": "ftp://nope"},
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_list_alerts(client):
    r = await client.get("/api/v1/alerts", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_billing_plans(client):
    r = await client.get("/api/v1/billing/plans")
    assert r.status_code == 200
    plans = r.json()
    assert len(plans) == 3
    ids = {p["id"] for p in plans}
    assert ids == {"free", "pro", "api"}


@pytest.mark.asyncio
async def test_billing_me(client):
    r = await client.get("/api/v1/billing/me", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    body = r.json()
    assert body["plan"] == "pro"


@pytest.mark.asyncio
async def test_billing_checkout_dev_mode(client):
    """In dev (no Stripe key) checkout returns a dev_mode response."""
    r = await client.post(
        "/api/v1/billing/checkout",
        json={"plan": "pro"},
        headers={"Authorization": "Bearer dev:alice:free"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["dev_mode"] is True
    assert "dev_upgrade=pro" in body["url"]


@pytest.mark.asyncio
async def test_billing_checkout_invalid_plan(client):
    r = await client.post(
        "/api/v1/billing/checkout",
        json={"plan": "enterprise"},
        headers={"Authorization": "Bearer dev:alice:free"},
    )
    assert r.status_code == 402


@pytest.mark.asyncio
async def test_missing_auth_in_production(client, monkeypatch):
    """When Clerk is configured, dev tokens are rejected."""
    # Simulate production by setting allow_dev_auth=False
    from app.config import get_settings
    from app.core.security import get_current_user

    settings = get_settings()
    monkeypatch.setattr(settings, "allow_dev_auth", False)
    monkeypatch.setattr(settings, "clerk_secret_key", "fake-key")

    # Re-trigger the dep with the new settings
    r = await client.get("/api/v1/stablecoins")
    assert r.status_code == 401
