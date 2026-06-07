"""arXiv client tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from app.services.arxiv import ArxivClient


ARXIV_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2401.00001v1</id>
    <title>CRISPR gene editing advances</title>
    <summary>Recent progress in CRISPR-Cas9 technology.</summary>
    <published>2024-01-01T00:00:00Z</published>
    <author><name>Alice Smith</name></author>
    <author><name>Bob Lee</name></author>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2401.00002v1</id>
    <title>mRNA vaccine efficacy</title>
    <summary>Analysis of mRNA vaccine performance.</summary>
    <published>2024-01-08T00:00:00Z</published>
    <author><name>Carol King</name></author>
  </entry>
</feed>"""


@pytest.mark.asyncio
@respx.mock
async def test_arxiv_search_parses_results():
    respx.get("http://export.arxiv.org/api/query").mock(
        return_value=httpx.Response(200, text=ARXIV_XML)
    )
    client = ArxivClient()
    results = await client.search("CRISPR", max_results=5)
    assert len(results) == 2
    assert results[0]["arxiv_id"] == "2401.00001v1"
    assert "CRISPR" in results[0]["title"]
    assert results[0]["authors"] == ["Alice Smith", "Bob Lee"]
    assert results[1]["authors"] == ["Carol King"]


@pytest.mark.asyncio
@respx.mock
async def test_arxiv_search_handles_500():
    respx.get("http://export.arxiv.org/api/query").mock(
        return_value=httpx.Response(500, text="server error")
    )
    client = ArxivClient()
    results = await client.search("test")
    assert results == []


@pytest.mark.asyncio
@respx.mock
async def test_arxiv_search_handles_malformed_xml():
    respx.get("http://export.arxiv.org/api/query").mock(
        return_value=httpx.Response(200, text="not-xml-at-all")
    )
    client = ArxivClient()
    results = await client.search("test")
    assert results == []
