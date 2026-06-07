"""Tests for peg math (the heart of PegWatch)."""
from app.services.peg_engine import (
    CRITICAL_DEVIATION_PCT,
    CRITICAL_Z,
    WARNING_DEVIATION_PCT,
    WARNING_Z,
    WATCH_DEVIATION_PCT,
    WATCH_Z,
    deviation_pct,
    median_price,
    rolling_stats,
    severity_from_z,
    z_score_of,
)


def test_deviation_pct_zero_at_peg():
    assert deviation_pct(1.0) == 0.0


def test_deviation_pct_below():
    assert abs(deviation_pct(0.99) - (-1.0)) < 1e-9


def test_deviation_pct_above():
    assert abs(deviation_pct(1.01) - 1.0) < 1e-9


def test_deviation_pct_custom_peg():
    assert abs(deviation_pct(0.95, peg=1.0) - (-5.0)) < 1e-9
    assert abs(deviation_pct(0.95, peg=0.95) - 0.0) < 1e-9


def test_median_price_handles_none():
    assert median_price([1.0, None, 0.99]) == 0.995


def test_median_price_all_none_returns_peg():
    assert median_price([None, None]) == 1.0


def test_median_price_single():
    assert median_price([0.999]) == 0.999


def test_z_score_zero_stddev_returns_zero():
    assert z_score_of(1.0, 1.0, 0.0) == 0.0


def test_z_score_standard_case():
    # (1.02 - 1.0) / 0.01 = 2.0
    assert abs(z_score_of(1.02, 1.0, 0.01) - 2.0) < 1e-9


def test_rolling_stats_empty():
    mean, stddev = rolling_stats([])
    assert mean == 1.0
    assert stddev == 0.0


def test_rolling_stats_single():
    mean, stddev = rolling_stats([1.0])
    assert mean == 1.0
    assert stddev == 0.0


def test_rolling_stats_basic():
    mean, stddev = rolling_stats([1.0, 1.01, 0.99])
    assert abs(mean - 1.0) < 1e-9
    assert stddev > 0


# Severity classification
def test_severity_healthy_at_peg():
    assert severity_from_z(0.5, 0.05) == "healthy"


def test_severity_watch_z_just_above_threshold():
    assert severity_from_z(WATCH_Z + 0.1, 0.05) == "watch"


def test_severity_watch_dev_just_above_threshold():
    assert severity_from_z(0.5, WATCH_DEVIATION_PCT + 0.05) == "watch"


def test_severity_warning_z():
    assert severity_from_z(WARNING_Z + 0.1, 0.05) == "warning"


def test_severity_warning_dev():
    assert severity_from_z(0.5, WARNING_DEVIATION_PCT + 0.05) == "warning"


def test_severity_critical_z():
    assert severity_from_z(CRITICAL_Z + 0.5, 0.05) == "critical"


def test_severity_critical_dev():
    assert severity_from_z(0.5, CRITICAL_DEVIATION_PCT + 0.1) == "critical"


def test_severity_uses_max_of_two_signals():
    # z=warning but dev=critical -> should be critical
    assert severity_from_z(WARNING_Z + 0.1, CRITICAL_DEVIATION_PCT + 0.5) == "critical"


def test_severity_negative_z_and_dev():
    assert severity_from_z(-(CRITICAL_Z + 0.5), -(CRITICAL_DEVIATION_PCT + 0.1)) == "critical"
