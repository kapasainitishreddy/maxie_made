"""Infringement analyzer tests."""

from __future__ import annotations

import pytest

from app.services.infringement import (
    InfringementAnalyzer,
    SEVERITY_THRESHOLDS,
    severity_for,
)


def test_severity_for_boundaries():
    assert severity_for(0.0) == "low"
    assert severity_for(0.29) == "low"
    assert severity_for(0.30) == "medium"
    assert severity_for(0.54) == "medium"
    assert severity_for(0.55) == "high"
    assert severity_for(0.74) == "high"
    assert severity_for(0.75) == "critical"
    assert severity_for(1.0) == "critical"


def test_severity_thresholds_consistent():
    for name, thr in SEVERITY_THRESHOLDS.items():
        if name != "low":
            assert thr > SEVERITY_THRESHOLDS["low"]


def test_assess_no_target_claims():
    a = InfringementAnalyzer()
    res = a.assess([], [{"claim_number": 1, "text": "x", "is_independent": True}])
    assert res["risk_score"] == 0.0
    assert res["severity"] == "low"
    assert res["claim_chart"] == []


def test_assess_no_candidate_claims():
    a = InfringementAnalyzer()
    res = a.assess([{"claim_number": 1, "text": "x", "is_independent": True}], [])
    assert res["risk_score"] == 0.0


def test_assess_identical_claims_high_risk():
    a = InfringementAnalyzer()
    target = [{
        "claim_number": 1,
        "text": "An anti-PD-1 antibody comprising a heavy chain CDR3 sequence",
        "is_independent": True,
    }]
    candidate = [{
        "claim_number": 1,
        "text": "An anti-PD-1 antibody comprising a heavy chain CDR3 sequence",
        "is_independent": True,
    }]
    res = a.assess(target, candidate)
    assert res["risk_score"] > 0.85
    assert res["severity"] in {"high", "critical"}


def test_assess_orthogonal_claims_low_risk():
    a = InfringementAnalyzer()
    target = [{"claim_number": 1, "text": "Anti-PD-1 antibody for melanoma", "is_independent": True}]
    candidate = [{"claim_number": 1, "text": "Insulin formulation for diabetes treatment", "is_independent": True}]
    res = a.assess(target, candidate)
    assert res["risk_score"] < 0.4


def test_build_claim_chart_uses_independent_only():
    a = InfringementAnalyzer()
    target = [
        {"claim_number": 1, "text": "Antibody for cancer", "is_independent": True},
        {"claim_number": 2, "text": "The antibody of claim 1", "is_independent": False},
    ]
    candidate = [
        {"claim_number": 1, "text": "Antibody for cancer", "is_independent": True},
    ]
    chart = a.build_claim_chart(target, candidate)
    assert len(chart) == 1
    assert chart[0]["claim_number"] == 1


def test_explain_short_strings():
    a = InfringementAnalyzer()
    expl = a.explain({"risk_score": 0.0, "severity": "low", "claim_chart": []})
    assert "No comparable" in expl
    expl2 = a.explain({
        "risk_score": 0.8,
        "severity": "high",
        "claim_chart": [{"overall_similarity": 0.8}],
    })
    assert "HIGH" in expl2 or "high" in expl2.lower()
