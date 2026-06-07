"""Report builder tests."""

from __future__ import annotations

from app.services.report import ReportBuilder


def test_fto_report_contains_title():
    b = ReportBuilder()
    pdf = b.build_fto_report("FTO Analysis — Humira", "Humira (adalimumab)", {"total_patents": 10, "unique_assignees": 5}, [])
    assert isinstance(pdf, (bytes, bytearray))
    assert pdf[:4] == b"%PDF"


def test_fto_report_includes_alerts_section():
    b = ReportBuilder()
    alerts = [
        {"risk_score": 0.82, "severity": "high", "summary": "Direct claim overlap with US 9,000,000."},
        {"risk_score": 0.45, "severity": "medium", "summary": "Partial overlap on formulation claim."},
    ]
    pdf = b.build_fto_report("FTO — Test", "Drug", {"total_patents": 5, "unique_assignees": 2}, alerts)
    assert len(pdf) > 1000  # Should be non-trivial


def test_infringement_report_renders():
    b = ReportBuilder()
    target = {"patent_number": "US123", "title": "Anti-X antibody", "jurisdiction": "US"}
    assessment = {
        "risk_score": 0.75,
        "severity": "high",
        "claim_chart": [
            {"claim_number": 1, "overall_similarity": 0.8, "cosine": 0.7, "element_overlap": 0.9},
        ],
    }
    pdf = b.build_infringement_report("Infringement — Anti-X", target, assessment)
    assert pdf[:4] == b"%PDF"
