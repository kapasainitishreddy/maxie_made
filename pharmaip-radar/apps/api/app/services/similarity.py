"""Patent similarity + claim scoring."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tokenize(text: str) -> list[str]:
    """Lowercase + split on non-alphanumeric."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _split_into_elements(claim: str) -> list[str]:
    """
    Split a claim string into atomic elements separated by semicolons or 'comprising' clauses.
    Falls back to sentence split if no delimiters.
    """
    if ";" in claim:
        return [s.strip() for s in claim.split(";") if s.strip()]
    parts = re.split(r",\s+(?:wherein|where|in which|comprising)", claim, flags=re.IGNORECASE)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()]
    return [claim.strip()]


class SimilarityEngine:
    """
    Claim similarity using TF-IDF cosine similarity with element-level matching.

    No external models needed — works fully offline.
    """

    def __init__(self, ngram_range: tuple[int, int] = (1, 2), min_df: int = 1) -> None:
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            min_df=min_df,
            stop_words="english",
        )

    def _vectorize(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 1))
        return self.vectorizer.fit_transform(texts).toarray()  # type: ignore[no-any-return]

    def pairwise(self, texts: list[str]) -> np.ndarray:
        """Return an NxN cosine-similarity matrix."""
        if len(texts) < 2:
            return np.eye(len(texts))
        vecs = self._vectorize(texts)
        return cosine_similarity(vecs)

    def score_pair(self, text_a: str, text_b: str) -> float:
        """Cosine similarity between two strings in [0, 1]."""
        if not text_a or not text_b:
            return 0.0
        sim = self.pairwise([text_a, text_b])
        return float(np.clip(sim[0, 1], 0.0, 1.0))

    def element_overlap(self, claim_a: str, claim_b: str) -> float:
        """
        Element-level recall: fraction of A's claim elements found (as substrings) in B.
        """
        elements_a = _split_into_elements(claim_a)
        if not elements_a:
            return 0.0
        b_lower = claim_b.lower()
        hits = sum(1 for e in elements_a if e.lower() in b_lower)
        return hits / len(elements_a)

    def jaccard(self, text_a: str, text_b: str) -> float:
        a, b = set(tokenize(text_a)), set(tokenize(text_b))
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def score_claim_pair(self, claim_a: str, claim_b: str) -> dict:
        """
        Combined infringement risk score for a claim pair.
        Returns: {overall, cosine, element_overlap, jaccard}
        """
        cosine = self.score_pair(claim_a, claim_b)
        overlap = self.element_overlap(claim_a, claim_b)
        jacc = self.jaccard(claim_a, claim_b)
        # Weighted combination — element overlap matters most for infringement
        overall = 0.5 * overlap + 0.35 * cosine + 0.15 * jacc
        return {
            "overall": float(np.clip(overall, 0.0, 1.0)),
            "cosine": cosine,
            "element_overlap": overlap,
            "jaccard": jacc,
        }

    def top_matches(
        self,
        query_claim: str,
        candidates: list[tuple[str, str]],  # [(id, text), ...]
        top_k: int = 5,
    ) -> list[dict]:
        """Return top-k candidates ranked by combined similarity to the query."""
        if not candidates:
            return []
        texts = [query_claim] + [c[1] for c in candidates]
        sims = self.pairwise(texts)[0, 1:]
        scored = []
        for (cid, ctext), sim in zip(candidates, sims):
            overlap = self.element_overlap(query_claim, ctext)
            overall = 0.5 * overlap + 0.35 * float(sim) + 0.15 * self.jaccard(query_claim, ctext)
            scored.append({
                "id": cid,
                "text": ctext,
                "cosine": float(sim),
                "element_overlap": overlap,
                "overall": float(np.clip(overall, 0.0, 1.0)),
            })
        scored.sort(key=lambda x: x["overall"], reverse=True)
        return scored[:top_k]


def bag_of_words_freq(texts: Iterable[str]) -> Counter[str]:
    """Small utility: word frequency across a corpus."""
    out: Counter[str] = Counter()
    for t in texts:
        out.update(tokenize(t))
    return out
