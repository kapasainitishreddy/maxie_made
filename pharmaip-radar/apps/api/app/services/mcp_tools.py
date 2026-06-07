"""MCP tool registry for PharmaIP Radar.

Each tool exposes a piece of the app's functionality (patent search, similarity
scoring, infringement detection) to any MCP-compatible AI agent (Claude Desktop,
Cursor, etc.) via the streamable HTTP endpoint at /mcp.
"""
from __future__ import annotations

import logging
from typing import Any

from mcp.server import Server
from mcp.types import Tool

from app.services.uspto import USPTOClient
from app.services.similarity import bag_of_words_freq
from app.services.infringement import InfringementAnalyzer, severity_for

log = logging.getLogger("mcp.pharmaip")


_TOOL_SCHEMAS: list[Tool] = [
    Tool(
        name="search_patents",
        description=(
            "Search the global patent database (USPTO + EPO + WIPO + Google Patents) "
            "for patents matching a free-text query. Returns a list of patents with "
            "number, title, assignee, jurisdiction, and filing date."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search terms — drug name, mechanism, IPC class, assignee, etc.",
                },
                "jurisdiction": {
                    "type": "string",
                    "description": "Optional: filter to a single jurisdiction (US, EP, JP, etc.)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default 10, max 50)",
                    "default": 10,
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="score_infringement_risk",
        description=(
            "Score infringement risk between a candidate patent and a portfolio patent "
            "using the app's element-level claim scoring. Returns a 0-100 risk score, "
            "a severity label, and a 1-sentence plain-English explanation."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "candidate_claim": {
                    "type": "string",
                    "description": "The candidate patent's main claim text",
                },
                "portfolio_claim": {
                    "type": "string",
                    "description": "The portfolio patent's main claim text to compare against",
                },
            },
            "required": ["candidate_claim", "portfolio_claim"],
        },
    ),
    Tool(
        name="compute_similarity_tokens",
        description=(
            "Return bag-of-words token frequencies for a text. Useful for explaining "
            "what terms drive a similarity score."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "texts": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "One or more texts to tokenize",
                },
            },
            "required": ["texts"],
        },
    ),
]


def register_tools(server: Server) -> None:
    log.info("Registered %d MCP tools for PharmaIP Radar", len(_TOOL_SCHEMAS))


def list_registered_tools() -> list[Tool]:
    return _TOOL_SCHEMAS


async def call_registered_tool(name: str, arguments: dict[str, Any]) -> Any:
    if name == "search_patents":
        return await _search_patents(arguments)
    if name == "score_infringement_risk":
        return await _score_infringement_risk(arguments)
    if name == "compute_similarity_tokens":
        return await _compute_similarity_tokens(arguments)
    raise ValueError(f"Unknown tool: {name}")


# ---- Tool implementations ----

async def _search_patents(args: dict[str, Any]) -> dict[str, Any]:
    query = args["query"]
    jurisdiction = args.get("jurisdiction")
    limit = min(args.get("limit", 10), 50)
    client = USPTOClient()
    results = await client.search(query=query, jurisdiction=jurisdiction, limit=limit)
    return {
        "query": query,
        "jurisdiction": jurisdiction,
        "count": len(results),
        "patents": results,
    }


async def _score_infringement_risk(args: dict[str, Any]) -> dict[str, Any]:
    cand = args["candidate_claim"]
    port = args["portfolio_claim"]
    analyzer = InfringementAnalyzer()
    # The analyzer works on claim dicts (number, text, is_independent). Wrap raw strings.
    target_claims = [{"number": "1", "text": port, "is_independent": True}]
    candidate_claims = [{"number": "1", "text": cand, "is_independent": True}]
    assessment = analyzer.assess(target_claims=target_claims, candidate_claims=candidate_claims)
    score_pct = round(assessment["risk_score"] * 100, 1)
    explanation = analyzer.explain(assessment)
    return {
        "risk_score_pct": score_pct,
        "severity": assessment["severity"],
        "explanation": explanation,
    }


async def _compute_similarity_tokens(args: dict[str, Any]) -> dict[str, Any]:
    texts = args["texts"]
    freqs = bag_of_words_freq(texts)
    return {"token_counts": dict(freqs)}
