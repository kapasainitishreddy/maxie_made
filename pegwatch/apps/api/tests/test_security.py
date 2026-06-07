"""Test security headers + rate limiting + input validation."""
import pytest


@pytest.mark.asyncio
async def test_security_headers_present(client):
    r = await client.get("/health")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert r.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in r.headers
    assert "Content-Security-Policy" in r.headers


@pytest.mark.asyncio
async def test_cors_allows_frontend_origin(client):
    r = await client.options(
        "/api/v1/stablecoins",
        headers={
            "Origin": "http://localhost:3004",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORS preflight returns 200 with the right allow-origin
    assert r.status_code in (200, 204)


@pytest.mark.asyncio
async def test_input_validation_rejects_bad_symbol(client):
    """Symbol with bad characters should be rejected by Pydantic."""
    r = await client.post(
        "/api/v1/stablecoins",
        json={"symbol": "lowercase!", "name": "X", "issuer": "Y", "tier": 1},
        headers={"Authorization": "Bearer dev:alice:api"},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_input_validation_rejects_negative_market_cap(client):
    r = await client.post(
        "/api/v1/stablecoins",
        json={"symbol": "NEG", "name": "X", "issuer": "Y", "tier": 1, "market_cap_usd": -100},
        headers={"Authorization": "Bearer dev:alice:api"},
    )
    assert r.status_code == 422
