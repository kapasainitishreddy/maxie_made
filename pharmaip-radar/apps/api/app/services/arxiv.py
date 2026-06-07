"""arXiv client for biomedical preprints."""

from __future__ import annotations

from typing import Any

import httpx


ARXIV_URL = "http://export.arxiv.org/api/query"


class ArxivClient:
    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    async def search(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.get(ARXIV_URL, params=params)
                r.raise_for_status()
                text = r.text
        except httpx.HTTPError:
            return []
        return self._parse_atom(text)

    def _parse_atom(self, xml: str) -> list[dict[str, Any]]:
        from defusedxml import ElementTree as DET
        ns = {"a": "http://www.w3.org/2005/Atom"}
        try:
            root = DET.fromstring(xml)
        except DET.ParseError:
            return []
        out: list[dict[str, Any]] = []
        for entry in root.findall("a:entry", ns):
            title_el = entry.find("a:title", ns)
            summary_el = entry.find("a:summary", ns)
            id_el = entry.find("a:id", ns)
            published_el = entry.find("a:published", ns)
            authors: list[str] = []
            for a in entry.findall("a:author", ns):
                name_el = a.find("a:name", ns)
                if name_el is not None and name_el.text:
                    authors.append(name_el.text)
            out.append({
                "arxiv_id": (id_el.text or "").split("/")[-1] if id_el is not None else "",
                "title": (title_el.text or "").strip() if title_el is not None else "",
                "summary": (summary_el.text or "").strip() if summary_el is not None else "",
                "published": published_el.text if published_el is not None else "",
                "authors": authors,
            })
        return out
