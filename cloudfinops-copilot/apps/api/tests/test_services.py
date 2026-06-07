"""RightSizer + IdleFinder + TerraformGen + SavingsVerifier tests."""

from __future__ import annotations

from datetime import date

import pytest

from app.services.right_sizer import RightSizer, INSTANCE_PRICING, hourly_to_monthly
from app.services.idle_finder import IdleFinder
from app.services.terraform_gen import TerraformGen
from app.services.savings_verifier import SavingsVerifier


# ---- RightSizer ----

def test_hourly_to_monthly():
    assert hourly_to_monthly(0.10) == 73.0


def test_rightsize_low_cpu_recommends_downsize():
    rs = RightSizer()
    r = {"id": "i-1234", "type": "m5.xlarge", "cpu_avg": 15.0}
    rec = rs.recommend(r)
    assert rec is not None
    assert rec["target_type"] == "m5.large"
    assert rec["monthly_savings"] > 0


def test_rightsize_high_cpu_no_savings():
    rs = RightSizer()
    r = {"id": "i-1234", "type": "m5.xlarge", "cpu_avg": 90.0}
    rec = rs.recommend(r)
    assert rec is None


def test_rightsize_normal_cpu_no_rec():
    rs = RightSizer()
    r = {"id": "i-1234", "type": "m5.xlarge", "cpu_avg": 50.0}
    rec = rs.recommend(r)
    assert rec is None


def test_rightsize_unknown_type():
    rs = RightSizer()
    assert rs.recommend({"id": "x", "type": "z9.unknown", "cpu_avg": 5.0}) is None


def test_rightsize_minimum_savings_threshold():
    rs = RightSizer()
    # Already at the smallest type — should not recommend
    r = {"id": "x", "type": "t3.nano", "cpu_avg": 5.0}
    assert rs.recommend(r) is None


# ---- IdleFinder ----

def test_idle_low_cpu_running():
    f = IdleFinder()
    resources = [{"id": "i-1", "cpu_avg": 2.0, "state": "running"}]
    assert len(f.find_idle(resources)) == 1


def test_idle_stopped_instance():
    f = IdleFinder()
    resources = [{"id": "i-1", "cpu_avg": 50.0, "state": "stopped"}]
    assert len(f.find_idle(resources)) == 1


def test_idle_normal_not_flagged():
    f = IdleFinder()
    resources = [{"id": "i-1", "cpu_avg": 50.0, "state": "running"}]
    assert f.find_idle(resources) == []


def test_idle_old_last_used_string():
    f = IdleFinder()
    from datetime import datetime, timedelta, timezone
    old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    resources = [{"id": "i-1", "cpu_avg": 50.0, "state": "running", "last_used": old}]
    assert len(f.find_idle(resources)) == 1


def test_idle_savings_estimate():
    f = IdleFinder()
    assert f.estimate_savings({}, 0.10) == 73.0


# ---- TerraformGen ----

def test_terraform_rightsize_includes_both_types():
    hcl = TerraformGen.rightsize_instance("i-1", "m5.xlarge", "m5.large")
    assert "m5.xlarge" in hcl
    assert "m5.large" in hcl
    assert "resource" in hcl


def test_terraform_terminate_ec2():
    hcl = TerraformGen.terminate_idle("i-1", "ec2")
    assert "i-1" in hcl
    assert "snapshot" in hcl.lower() or "terminate" in hcl.lower()


def test_terraform_terminate_rds():
    hcl = TerraformGen.terminate_idle("db-1", "rds")
    assert "snapshot" in hcl.lower()


def test_terraform_schedule():
    hcl = TerraformGen.schedule_nonprod("i-1")
    assert "scheduler" in hcl.lower()
    assert "stop" in hcl.lower()


def test_terraform_graviton():
    hcl = TerraformGen.graviton_migration("i-1", "m5.large", "t4g.large")
    assert "t4g.large" in hcl


def test_terraform_dispatch():
    rec = {"rec_type": "rightsize", "resource_id": "i-1", "resource_type": "ec2",
           "evidence": {"current_type": "m5.xlarge", "target_type": "m5.large"}}
    hcl = TerraformGen.for_recommendation(rec)
    assert "m5.large" in hcl


def test_terraform_unknown_type_returns_comment():
    hcl = TerraformGen.for_recommendation({"rec_type": "weird_thing"})
    assert hcl.startswith("#")


# ---- SavingsVerifier ----

def test_savings_compute_positive():
    v = SavingsVerifier()
    assert v.compute(100.0, 70.0, date(2024, 1, 1), date(2024, 1, 31)) == 30.0


def test_savings_compute_clamps_zero():
    v = SavingsVerifier()
    # Actual > baseline (cost went up): no savings
    assert v.compute(100.0, 130.0, date(2024, 1, 1), date(2024, 1, 31)) == 0.0


def test_savings_compute_zero_baseline():
    v = SavingsVerifier()
    assert v.compute(0.0, 0.0, date(2024, 1, 1), date(2024, 1, 31)) == 0.0


def test_savings_compute_rounded():
    v = SavingsVerifier()
    assert v.compute(100.555, 70.123, date(2024, 1, 1), date(2024, 1, 31)) == 30.43
