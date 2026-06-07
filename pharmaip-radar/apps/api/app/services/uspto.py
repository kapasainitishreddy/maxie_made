"""USPTO client — PatentsView + USPTO Open Data APIs."""

from __future__ import annotations

from typing import Any

import httpx


PATENTSVIEW_BASE = "https://api.patentsview.org/patents/query"
USPTO_ODP_BASE = "https://api.uspto.gov/patent/v1"


class USPTOClient:
    """Lightweight async client for the public PatentsView + USPTO APIs."""

    def __init__(self, api_key: str = "", timeout: float = 30.0) -> None:
        self.api_key = api_key
        self.timeout = timeout

    async def search_patents(
        self,
        query_text: str | None = None,
        assignee: str | None = None,
        drug_name: str | None = None,
        ipc_class: str | None = None,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """
        Search PatentsView. Returns normalized patent dicts.
        On any upstream error, returns an empty list (caller handles fallback).
        """
        clauses: list[dict] = []
        if query_text:
            clauses.append({"_text_any": {"patent_title": query_text}})
        if assignee:
            clauses.append({"_contains": {"assignee_organization": assignee}})
        if ipc_class:
            clauses.append({"_begins": {"ipc_class": ipc_class}})

        if not clauses:
            clauses = [{"_all": [{"_text_any": {"patent_title": "pharma"}}]}]
            query = {"_and": clauses}
        else:
            query = {"_and": clauses} if len(clauses) > 1 else clauses[0]

        body = {
            "q": query,
            "f": [
                "patent_number",
                "patent_title",
                "patent_abstract",
                "patent_date",
                "inventor_first_name",
                "inventor_last_name",
                "assignee_organization",
                "ipc_class",
            ],
            "o": {"per_page": min(limit, 100)},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(PATENTSVIEW_BASE, json=body)
                r.raise_for_status()
                data = r.json()
        except (httpx.HTTPError, ValueError):
            return []

        patents = []
        for row in data.get("patents", []):
            patents.append(self._normalize_patentsview(row, drug_name))
        return patents

    def _normalize_patentsview(self, row: dict, drug_hint: str | None) -> dict:
        inventors = [
            f"{i.get('inventor_first_name', '')} {i.get('inventor_last_name', '')}".strip()
            for i in row.get("inventors", [])
        ]
        assignees = [
            a.get("assignee_organization", "")
            for a in row.get("assignees", [])
            if a.get("assignee_organization")
        ]
        ipc = row.get("ipc_classes", []) or row.get("ipc_class", [])
        if isinstance(ipc, str):
            ipc = [ipc]
        return {
            "patent_number": row.get("patent_number", ""),
            "jurisdiction": "US",
            "title": row.get("patent_title", ""),
            "abstract": row.get("patent_abstract"),
            "filing_date": row.get("patent_date"),
            "grant_date": row.get("patent_date"),
            "assignee": assignees[0] if assignees else None,
            "inventors": [i for i in inventors if i],
            "ipc_classes": ipc,
            "drug_name": drug_hint,
            "status": "granted",
        }

    async def fetch_patent(self, patent_number: str) -> dict | None:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(
                    PATENTSVIEW_BASE,
                    json={
                        "q": {"patent_number": patent_number},
                        "f": ["patent_number", "patent_title", "patent_abstract",
                              "patent_date", "assignee_organization", "ipc_class"],
                    },
                )
                r.raise_for_status()
                data = r.json()
        except (httpx.HTTPError, ValueError):
            return None
        rows = data.get("patents", [])
        if not rows:
            return None
        return self._normalize_patentsview(rows[0], None)
