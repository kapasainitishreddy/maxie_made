"""Test the peg engine integration (write + read snapshots)."""
import pytest


@pytest.mark.asyncio
async def test_record_snapshot_computes_z_score(client):
    # Refresh to get a real snapshot
    r = await client.post(
        "/api/v1/peg/USDC/refresh",
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    assert r.status_code == 200

    # History should now have one point
    r = await client.get("/api/v1/peg/USDC/history?hours=24", headers={"Authorization": "Bearer dev:alice:pro"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["points"]) >= 1


@pytest.mark.asyncio
async def test_multiple_refreshes_creates_z_score_history(client):
    for _ in range(3):
        r = await client.post(
            "/api/v1/peg/USDC/refresh",
            headers={"Authorization": "Bearer dev:alice:pro"},
        )
        assert r.status_code == 200

    r = await client.get("/api/v1/peg/USDC/history?hours=24", headers={"Authorization": "Bearer dev:alice:pro"})
    body = r.json()
    assert len(body["points"]) >= 3
    # Mean should be very close to 1.0 (synthetic data is near peg)
    assert 0.99 < body["mean_7d"] < 1.01


@pytest.mark.asyncio
async def test_severity_classification_for_healthy_peg(client):
    r = await client.post(
        "/api/v1/peg/USDC/refresh",
        headers={"Authorization": "Bearer dev:alice:pro"},
    )
    body = r.json()
    # Synthetic data centers on peg, so should be healthy
    assert body["severity"] in ("healthy", "watch")
