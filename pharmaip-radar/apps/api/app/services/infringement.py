"""Infringement analyzer — claim charts and risk scoring."""

from __future__ import annotations

from typing import Iterable

from app.services.similarity import SimilarityEngine, _split_into_elements


SEVERITY_THRESHOLDS = {
    "low": 0.0,
    "medium": 0.30,
    "high": 0.55,
    "critical": 0.75,
}


def severity_for(score: float) -> str:
    if score >= SEVERITY_THRESHOLDS["critical"]:
        return "critical"
    if score >= SEVERITY_THRESHOLDS["high"]:
        return "high"
    if score >= SEVERITY_THRESHOLDS["medium"]:
        return "medium"
    return "low"


class InfringementAnalyzer:
    """
    Builds claim charts and computes risk scores between a target patent's
    independent claims and a candidate's claims.
    """

    def __init__(self) -> None:
        self.engine = SimilarityEngine()

    def build_claim_chart(
        self,
        target_claims: list[dict],
        candidate_claims: list[dict],
    ) -> list[dict]:
        """
        target_claims: [{claim_number, text, is_independent}, ...]
        candidate_claims: same shape

        Returns a list of claim-chart entries, one per target independent claim,
        with the best matching candidate claim annotated.
        """
        chart: list[dict] = []
        indep = [c for c in target_claims if c.get("is_independent", True)]
        if not indep:
            indep = target_claims

        for tc in indep:
            best = None
            for cc in candidate_claims:
                scores = self.engine.score_claim_pair(tc["text"], cc["text"])
                if best is None or scores["overall"] > best["scores"]["overall"]:
                    best = {
                        "candidate_claim_number": cc["claim_number"],
                        "candidate_text": cc["text"],
                        "scores": scores,
                    }
            if best is None:
                continue

            elements_t = _split_into_elements(tc["text"])
            elements_c = _split_into_elements(best["candidate_text"])
            element_matches = []
            for et in elements_t:
                best_sim, best_match = 0.0, ""
                for ec in elements_c:
                    sim = self.engine.score_pair(et, ec)
                    if sim > best_sim:
                        best_sim, best_match = sim, ec
                element_matches.append({
                    "element": et,
                    "matched_text": best_match,
                    "similarity": float(best_sim),
                })

            chart.append({
                "claim_number": tc["claim_number"],
                "claim_text": tc["text"],
                "matched_claim_number": best["candidate_claim_number"],
                "matched_text": best["candidate_text"],
                "overall_similarity": best["scores"]["overall"],
                "cosine": best["scores"]["cosine"],
                "element_overlap": best["scores"]["element_overlap"],
                "jaccard": best["scores"]["jaccard"],
                "element_matches": element_matches,
            })
        return chart

    def assess(
        self,
        target_claims: list[dict],
        candidate_claims: list[dict],
    ) -> dict:
        """
        Returns overall infringement assessment:
        {
            risk_score: 0-1,
            severity: low/medium/high/critical,
            claim_chart: [...],
            evidence: {key_terms_overlap, ...}
        }
        """
        chart = self.build_claim_chart(target_claims, candidate_claims)
        if not chart:
            return {
                "risk_score": 0.0,
                "severity": "low",
                "claim_chart": [],
                "evidence": {"reason": "no_claims"},
            }
        avg = sum(c["overall_similarity"] for c in chart) / len(chart)
        max_score = max(c["overall_similarity"] for c in chart)
        risk = 0.6 * max_score + 0.4 * avg
        return {
            "risk_score": float(risk),
            "severity": severity_for(risk),
            "claim_chart": chart,
            "evidence": {
                "average_similarity": avg,
                "max_similarity": max_score,
                "num_target_independent_claims": len([c for c in target_claims if c.get("is_independent", True)]),
            },
        }

    def explain(self, assessment: dict) -> str:
        """Generate a short human-readable explanation of the assessment."""
        score = assessment["risk_score"]
        sev = assessment["severity"].upper()
        n = len(assessment["claim_chart"])
        if n == 0:
            return "No comparable claims found."
        max_match = max(c["overall_similarity"] for c in assessment["claim_chart"])
        return (
            f"Risk: {sev} (score={score:.2f}). "
            f"Analyzed {n} independent claim(s). "
            f"Highest claim-level similarity: {max_match:.2f}. "
            f"Recommend legal review." if score >= 0.55 else
            f"Risk: {sev} (score={score:.2f}). Low overlap across {n} claim(s). "
            f"Continue monitoring."
        )
