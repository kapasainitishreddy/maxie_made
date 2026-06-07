"""PubMed client tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from app.services.pubmed import PubMedClient


@pytest.mark.asyncio
@respx.mock
async def test_pubmed_search_returns_normalized():
    esearch = respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi").mock(
        return_value=httpx.Response(
            200,
            json={"esearchresult": {"idlist": ["12345", "67890"]}},
        )
    )
    esummary = respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi").mock(
        return_value=httpx.Response(
            200,
            json={
                "result": {
                    "uids": ["12345", "67890"],
                    "12345": {
                        "title": "PD-1 inhibitor trial",
                        "authors": [{"name": "Smith J"}, {"name": "Doe A"}],
                        "fulljournalname": "Nature Medicine",
                        "pubdate": "2024 Jan",
                        "articleids": [{"idtype": "doi", "value": "10.1038/test"}],
                    },
                    "67890": {
                        "title": "Cancer immunotherapy review",
                        "authors": [{"name": "Lee K"}],
                        "fulljournalname": "Lancet",
                        "pubdate": "2024 Feb",
                        "articleids": [],
                    },
                }
            },
        )
    )

    client = PubMedClient()
    results = await client.search("PD-1 cancer", max_results=5)
    assert esearch.called
    assert esummary.called
    assert len(results) == 2
    assert results[0]["pmid"] == "12345"
    assert results[0]["title"] == "PD-1 inhibitor trial"
    assert results[0]["doi"] == "10.1038/test"
    assert results[1]["doi"] is None


@pytest.mark.asyncio
@respx.mock
async def test_pubmed_search_empty_on_404():
    respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi").mock(
        return_value=httpx.Response(500, text="server error")
    )
    client = PubMedClient()
    results = await client.search("anything")
    assert results == []


@pytest.mark.asyncio
@respx.mock
async def test_pubmed_search_empty_idlist():
    respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi").mock(
        return_value=httpx.Response(200, json={"esearchresult": {"idlist": []}})
    )
    client = PubMedClient()
    results = await client.search("nothing")
    assert results == []
