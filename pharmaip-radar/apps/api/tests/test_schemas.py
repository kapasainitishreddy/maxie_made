"""Schemas + basic app tests."""

from __future__ import annotations

from app import __version__
from app.schemas.common import HealthResponse, PageResponse
from app.schemas.patent import (
    PatentSummary,
    Jurisdiction,
    TherapeuticArea,
    PatentSearchRequest,
)


def test_health_response_defaults():
    h = HealthResponse(app="x", version="1", env="test")
    assert h.status == "ok"
    assert h.app == "x"


def test_page_response_builds():
    p = PageResponse.build([1, 2, 3], total=3, page=1, page_size=25)
    assert p.total == 3
    assert p.total_pages == 1


def test_page_response_multi_pages():
    p = PageResponse.build(list(range(50)), total=50, page=1, page_size=20)
    assert p.total_pages == 3


def test_patent_search_request_validates():
    req = PatentSearchRequest(
        query="PD-1",
        therapeutic_area=TherapeuticArea.ONCOLOGY,
        jurisdictions=[Jurisdiction.US, Jurisdiction.EP],
    )
    assert req.therapeutic_area == TherapeuticArea.ONCOLOGY
    assert len(req.jurisdictions) == 2


def test_app_version_present():
    assert __version__ == "0.1.0"


def test_therapeutic_areas_listed():
    expected = {"Oncology", "Immunology", "Neurology", "Cardiology", "Rare Disease"}
    actual = {t.value for t in TherapeuticArea}
    assert expected.issubset(actual)
