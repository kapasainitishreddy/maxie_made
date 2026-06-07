"""MCP server exposing pharma IP tools to any MCP-compatible client.

Exposes:
  - search_patents
  - get_patent
  - analyze_infringement
  - generate_report
  - semantic_search
"""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any

# Lightweight stdio MCP server implementation.
# Compatible with the Model Context Protocol spec.

TOOLS = [
    {
        "name": "search_patents",
        "description": "Search the patent database by query, drug, therapeutic area, jurisdiction, or assignee.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "drug_name": {"type": "string"},
                "therapeutic_area": {"type": "string"},
                "assignee": {"type": "string"},
                "limit": {"type": "integer", "default": 10},
            },
        },
    },
    {
        "name": "get_patent",
        "description": "Retrieve a single patent with full claims.",
        "inputSchema": {
            "type": "object",
            "properties": {"patent_id": {"type": "string"}},
            "required": ["patent_id"],
        },
    },
    {
        "name": "analyze_infringement",
        "description": "Compare two patents and return a risk assessment + claim chart.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_patent_id": {"type": "string"},
                "candidate_patent_id": {"type": "string"},
            },
            "required": ["target_patent_id", "candidate_patent_id"],
        },
    },
    {
        "name": "generate_report",
        "description": "Generate an FTO or landscape report PDF.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "report_type": {"type": "string", "enum": ["fto", "landscape", "infringement", "patentability"]},
                "title": {"type": "string"},
                "target_drug": {"type": "string"},
            },
            "required": ["report_type", "title"],
        },
    },
    {
        "name": "semantic_search",
        "description": "Semantic search across patent claims using TF-IDF.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    },
]


async def handle_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    # Lazy imports so the MCP server can start even if app isn't initialized
    from app.db import AsyncSessionLocal
    from sqlalchemy import select
    from app.models.patent import Patent, PatentClaim
    from app.services.similarity import SimilarityEngine
    from app.services.infringement import InfringementAnalyzer

    if name == "search_patents":
        async with AsyncSessionLocal() as db:
            stmt = select(Patent)
            if arguments.get("query"):
                stmt = stmt.where(
                    Patent.title.ilike(f"%{arguments['query']}%")
                    | Patent.abstract.ilike(f"%{arguments['query']}%")
                )
            if arguments.get("drug_name"):
                stmt = stmt.where(Patent.drug_name.ilike(f"%{arguments['drug_name']}%"))
            if arguments.get("therapeutic_area"):
                stmt = stmt.where(Patent.therapeutic_area == arguments["therapeutic_area"])
            if arguments.get("assignee"):
                stmt = stmt.where(Patent.assignee.ilike(f"%{arguments['assignee']}%"))
            stmt = stmt.limit(arguments.get("limit", 10))
            rows = (await db.execute(stmt)).scalars().unique().all()
            return {
                "patents": [
                    {
                        "id": str(p.id),
                        "patent_number": p.patent_number,
                        "title": p.title,
                        "assignee": p.assignee,
                        "drug_name": p.drug_name,
                        "therapeutic_area": p.therapeutic_area,
                    }
                    for p in rows
                ]
            }

    if name == "get_patent":
        async with AsyncSessionLocal() as db:
            p = await db.get(Patent, uuid.UUID(arguments["patent_id"]))
            if not p:
                return {"error": "not found"}
            return {
                "id": str(p.id),
                "patent_number": p.patent_number,
                "jurisdiction": p.jurisdiction,
                "title": p.title,
                "abstract": p.abstract,
                "assignee": p.assignee,
                "drug_name": p.drug_name,
                "therapeutic_area": p.therapeutic_area,
                "filing_date": p.filing_date.isoformat() if p.filing_date else None,
                "claims": [
                    {"number": c.claim_number, "text": c.text, "independent": c.is_independent}
                    for c in (p.claims or [])
                ],
            }

    if name == "analyze_infringement":
        async with AsyncSessionLocal() as db:
            t = await db.get(Patent, uuid.UUID(arguments["target_patent_id"]))
            c = await db.get(Patent, uuid.UUID(arguments["candidate_patent_id"]))
            if not t or not c:
                return {"error": "patent(s) not found"}
            t_claims = [{"claim_number": c.claim_number, "text": c.text, "is_independent": c.is_independent} for c in (t.claims or [])]
            c_claims = [{"claim_number": c.claim_number, "text": c.text, "is_independent": c.is_independent} for c in (c.claims or [])]
            analyzer = InfringementAnalyzer()
            return analyzer.assess(t_claims, c_claims)

    if name == "semantic_search":
        async with AsyncSessionLocal() as db:
            rows = (await db.execute(select(Patent))).scalars().unique().all()
            candidates = []
            claim_to_patent: dict[str, Patent] = {}
            for p in rows:
                for c in (p.claims or []):
                    cid = f"{p.id}#{c.claim_number}"
                    candidates.append((cid, c.text))
                    claim_to_patent[cid] = p
            eng = SimilarityEngine()
            matches = eng.top_matches(arguments["query"], candidates, top_k=arguments.get("top_k", 5))
            out = []
            for m in matches:
                p = claim_to_patent.get(m["id"])
                if p:
                    out.append({
                        "patent_id": str(p.id),
                        "patent_number": p.patent_number,
                        "title": p.title,
                        "drug_name": p.drug_name,
                        "claim_text": m["text"],
                        "score": m["overall"],
                    })
            return {"matches": out}

    if name == "generate_report":
        return {
            "status": "queued",
            "report_type": arguments["report_type"],
            "title": arguments["title"],
            "message": "Use POST /api/v1/reports to generate. Coming soon via MCP bridge.",
        }

    return {"error": f"unknown tool: {name}"}


async def stdio_loop() -> None:
    """Minimal stdio JSON-RPC MCP server."""
    import sys
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        msg_id = req.get("id")
        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "pharmaip-radar-mcp", "version": "0.1.0"},
                    "capabilities": {"tools": {}},
                },
            }
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            result = await handle_tool(name, args)
            resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}
        else:
            resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"method not found: {method}"}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(stdio_loop())
