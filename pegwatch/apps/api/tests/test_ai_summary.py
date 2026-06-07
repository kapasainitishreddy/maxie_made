"""Tests for AI summary fallback path."""
from app.services.ai_summary import _fallback_summary


def test_fallback_summary_below_peg():
    s = _fallback_summary("USDC", -0.5, -2.5, 0.995)
    assert "USDC" in s
    assert "below" in s
    assert "-0.500" in s
    assert "warning" in s


def test_fallback_summary_above_peg():
    s = _fallback_summary("USDT", 0.2, 1.8, 1.002)
    assert "above" in s
    assert "watch" in s or "elevated" in s


def test_fallback_summary_stable():
    s = _fallback_summary("DAI", 0.01, 0.5, 1.0001)
    assert "stable" in s
    assert "DAI" in s


def test_fallback_summary_critical():
    s = _fallback_summary("FRAX", -3.0, -4.0, 0.97)
    assert "critical" in s


def test_fallback_summary_includes_recommendation():
    s = _fallback_summary("USDC", -1.0, -2.5, 0.99)
    assert "Recommendation" in s or "recommendation" in s or "monitor" in s.lower()
