"""PubMed E-utilities client."""

from __future__ import annotations

from typing import Any

import httpx


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


class PubMedClient:
    def __init__(self, api_key: str = "", timeout: float = 30.0) -> None:
        self.api_key = api_key
        self.timeout = timeout

    async def search(self, term: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Search PubMed and return a list of normalized article summaries."""
        params = {
            "db": "pubmed",
            "term": term,
            "retmax": max_results,
            "retmode": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.get(f"{EUTILS}/esearch.fcgi", params=params)
                r.raise_for_status()
                ids = r.json().get("esearchresult", {}).get("idlist", [])
                if not ids:
                    return []
                r2 = await client.get(
                    f"{EUTILS}/esummary.fcgi",
                    params={
                        "db": "pubmed",
                        "id": ",".join(ids),
                        "retmode": "json",
                        **({"api_key": self.api_key} if self.api_key else {}),
                    },
                )
                r2.raise_for_status()
                result = r2.json().get("result", {})
        except (httpx.HTTPError, ValueError):
            return []

        out: list[dict[str, Any]] = []
        for pmid in ids:
            article = result.get(pmid)
            if not article or not isinstance(article, dict):
                continue
            out.append({
                "pmid": pmid,
                "title": article.get("title", ""),
                "authors": [a.get("name", "") for a in article.get("authors", [])],
                "journal": article.get("fulljournalname") or article.get("source", ""),
                "pubdate": article.get("pubdate", ""),
                "doi": next(
                    (a.get("value") for a in article.get("articleids", [])
                     if a.get("idtype") == "doi"),
                    None,
                ),
            })
        return out
