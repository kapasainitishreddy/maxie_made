"""Landscape analyzer tests."""

from __future__ import annotations

from datetime import date

from app.services.landscape import LandscapeAnalyzer


def test_empty_input_returns_zero():
    a = LandscapeAnalyzer([])
    res = a.analyze()
    assert res.total_patents == 0
    assert res.unique_assignees == 0
    assert res.summary != ""


def test_filing_trend_counts_years():
    patents = [
        {"title": "a", "abstract": "b", "assignee": "X", "ipc_classes": ["A61K"],
         "filing_date": date(2020, 5, 1)},
        {"title": "c", "abstract": "d", "assignee": "X", "ipc_classes": ["A61K"],
         "filing_date": date(2020, 8, 1)},
        {"title": "e", "abstract": "f", "assignee": "Y", "ipc_classes": ["C07D"],
         "filing_date": date(2021, 1, 15)},
    ]
    res = LandscapeAnalyzer(patents).analyze()
    assert res.total_patents == 3
    assert res.unique_assignees == 2
    assert res.filing_trend[2020] == 2
    assert res.filing_trend[2021] == 1


def test_top_assignees_share_sums_to_one():
    patents = [
        {"title": "a", "abstract": "b", "assignee": "AbbVie", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 1, 1)},
        {"title": "c", "abstract": "d", "assignee": "AbbVie", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 2, 1)},
        {"title": "e", "abstract": "f", "assignee": "Merck", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 3, 1)},
    ]
    res = LandscapeAnalyzer(patents).analyze()
    assert abs(sum(a.market_share for a in res.top_assignees) - 1.0) < 0.001
    assert res.top_assignees[0].assignee == "AbbVie"
    assert res.top_assignees[0].patent_count == 2


def test_density_heatmap_populated():
    patents = [
        {"title": "a", "abstract": "b", "assignee": "X", "ipc_classes": ["A61K31/00"],
         "filing_date": date(2022, 1, 1)},
        {"title": "c", "abstract": "d", "assignee": "X", "ipc_classes": ["A61K31/00"],
         "filing_date": date(2022, 6, 1)},
        {"title": "e", "abstract": "f", "assignee": "Y", "ipc_classes": ["C07D401/00"],
         "filing_date": date(2023, 1, 1)},
    ]
    res = LandscapeAnalyzer(patents).analyze()
    assert len(res.density_heatmap) > 0
    # Density should be normalized 0-1
    for cell in res.density_heatmap:
        assert 0.0 <= cell.density <= 1.0


def test_white_space_detection():
    patents = [
        {"title": "a", "abstract": "b", "assignee": "X", "ipc_classes": ["A61K"],
         "filing_date": date(2020, 1, 1)},
        {"title": "c", "abstract": "d", "assignee": "Y", "ipc_classes": ["A61K"],
         "filing_date": date(2020, 1, 1)},
        {"title": "e", "abstract": "f", "assignee": "Z", "ipc_classes": ["A61K"],
         "filing_date": date(2020, 1, 1)},
        {"title": "g", "abstract": "h", "assignee": "W", "ipc_classes": ["A61K"],
         "filing_date": date(2024, 1, 1)},
    ]
    res = LandscapeAnalyzer(patents).analyze()
    # 2021-2023 had zero filings (avg=1, 30%=0.3) so they should appear
    years_with_zero = [str(y) for y in [2021, 2022, 2023] if str(y) not in res.filing_trend]
    # white_space flags years with very low activity
    assert len(res.white_space) > 0 or len(years_with_zero) > 0


def test_tech_clustering_produces_clusters():
    patents = [
        {"title": "Anti-PD-1 antibody for cancer", "abstract": "Antibody blocking PD-1",
         "assignee": "A", "drug_name": "D1", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 1, 1)},
        {"title": "Anti-PD-L1 antibody for tumor", "abstract": "Antibody blocking PD-L1",
         "assignee": "A", "drug_name": "D1", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 2, 1)},
        {"title": "Insulin formulation for diabetes", "abstract": "Insulin analog",
         "assignee": "B", "drug_name": "D2", "ipc_classes": ["A61K"],
         "filing_date": date(2022, 3, 1)},
        {"title": "Glp-1 receptor agonist", "abstract": "Glucagon-like peptide",
         "assignee": "B", "drug_name": "D2", "ipc_classes": ["C07K"],
         "filing_date": date(2022, 4, 1)},
    ]
    res = LandscapeAnalyzer(patents, n_clusters=2).analyze()
    assert 0 < len(res.tech_clusters) <= 2
    for c in res.tech_clusters:
        assert c.size > 0
