"""Similarity engine tests — the heart of infringement analysis."""

from __future__ import annotations

import pytest

from app.services.similarity import (
    SimilarityEngine,
    tokenize,
    _split_into_elements,
    bag_of_words_freq,
)


def test_tokenize_lowercases_and_splits():
    assert tokenize("Hello, World! 2024") == ["hello", "world", "2024"]


def test_split_elements_by_semicolon():
    claim = "A compound; wherein the compound is X; comprising Y"
    elems = _split_into_elements(claim)
    assert len(elems) >= 2
    assert "A compound" in elems


def test_split_elements_by_comma_keyword():
    claim = "A method of treating cancer, wherein the dose is 10mg, comprising a step"
    elems = _split_into_elements(claim)
    assert len(elems) >= 2


def test_bow_freq_counts_correctly():
    freq = bag_of_words_freq(["the cat sat", "the dog sat"])
    assert freq["the"] == 2
    assert freq["sat"] == 2
    assert freq["cat"] == 1


def test_pairwise_identity():
    eng = SimilarityEngine()
    sim = eng.pairwise(["hello world", "hello world"])
    assert sim.shape == (2, 2)
    assert sim[0, 1] >= 0.99


def test_pairwise_orthogonal_low():
    eng = SimilarityEngine()
    sim = eng.pairwise(["cat dog", "finance equity bond"])
    assert sim[0, 1] < 0.2


def test_score_pair_in_range():
    eng = SimilarityEngine()
    s = eng.score_pair("Pharmaceutical composition for cancer", "Composition for tumor treatment")
    assert 0.0 <= s <= 1.0


def test_score_pair_identical_is_one():
    eng = SimilarityEngine()
    text = "Anti-PD-1 antibody for treating melanoma"
    s = eng.score_pair(text, text)
    assert s == pytest.approx(1.0, abs=0.01)


def test_jaccard_basic():
    eng = SimilarityEngine()
    assert eng.jaccard("a b c", "b c d") == pytest.approx(0.5, abs=0.01)
    assert eng.jaccard("a b", "c d") == 0.0
    assert eng.jaccard("", "x") == 0.0


def test_element_overlap_full_match():
    eng = SimilarityEngine()
    # A's elements all appear as substrings in B
    a = "compound; antibody; linker; payload"
    b = "compound with antibody, linker, and payload"
    overlap = eng.element_overlap(a, b)
    assert overlap >= 0.75


def test_element_overlap_partial():
    eng = SimilarityEngine()
    a = "compound; antibody; linker; payload"
    b = "compound; small molecule"
    overlap = eng.element_overlap(a, b)
    assert 0.0 < overlap < 1.0


def test_score_claim_pair_combined_score():
    eng = SimilarityEngine()
    res = eng.score_claim_pair(
        "An antibody; a heavy chain; a light chain",
        "An antibody; a heavy chain; a light chain",
    )
    assert "overall" in res
    assert res["overall"] == 1.0
    assert res["element_overlap"] == 1.0


def test_top_matches_orders_by_score():
    eng = SimilarityEngine()
    query = "PD-L1 antibody for cancer immunotherapy"
    candidates = [
        ("1", "PD-L1 antibody composition for treating tumors"),
        ("2", "Small molecule kinase inhibitor for diabetes"),
        ("3", "PD-1 antibody for cancer treatment"),
    ]
    matches = eng.top_matches(query, candidates, top_k=3)
    assert len(matches) == 3
    # The PD-L1 match should rank first
    assert matches[0]["id"] in {"1", "3"}
    assert matches[0]["overall"] >= matches[-1]["overall"]


def test_top_matches_handles_empty():
    eng = SimilarityEngine()
    assert eng.top_matches("query", [], top_k=5) == []


def test_pairwise_single_item():
    eng = SimilarityEngine()
    sim = eng.pairwise(["only"])
    assert sim.shape == (1, 1)
