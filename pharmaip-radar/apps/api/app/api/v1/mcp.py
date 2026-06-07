"""Reusable FastAPI integration for MCP (Model Context Protocol) servers.

Mounts an MCP server at /mcp using streamable HTTP transport so any MCP client
(Claude Desktop, Cursor, etc.) can connect via HTTP instead of stdio.

Usage in main.py:
    from app.api.v1.mcp import mcp_router
    app.include_router(mcp_router, prefix="/mcp")

Then register tools in app.services.mcp_tools.
"""
from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from fastapi import APIRouter, Request
from fastapi.responses import Response
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import TextContent, Tool
from starlette.types import Receive, Scope, Send

log = logging.getLogger("mcp")

# Lazy-initialized globals so we don't spin up the MCP server unless /mcp is hit.
_server: Server | None = None
_session_manager: StreamableHTTPSessionManager | None = None


def get_server() -> Server:
    """Return (and lazily build) the global MCP Server, pulling tools from services.mcp_tools."""
    global _server
    if _server is not None:
        return _server

    from app.services.mcp_tools import register_tools

    server: Server = Server("maxie_made")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        # Delegates to the per-app tool registry
        from app.services.mcp_tools import list_registered_tools

        return list_registered_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        from app.services.mcp_tools import call_registered_tool

        try:
            result = await call_registered_tool(name, arguments)
        except Exception as exc:  # surface errors to the client instead of crashing
            log.exception("MCP tool %s failed", name)
            return [TextContent(type="text", text=f"Error: {exc}")]
        # MCP requires list[TextContent] | list[ImageContent] | list[EmbeddedResource]
        # We standardize on a single JSON-encoded TextContent for simplicity.
        return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]

    register_tools(server)
    _server = server
    return _server


def get_session_manager() -> StreamableHTTPSessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = StreamableHTTPSessionManager(
            app=get_server(),
            json_response=False,  # use SSE-style stream so clients can do streaming too
        )
    return _session_manager


mcp_router = APIRouter()


@asynccontextmanager
async def _lifespan(_app: Any) -> AsyncIterator[None]:
    async with get_session_manager():
        yield


@mcp_router.get("/health")
async def mcp_health() -> dict[str, str]:
    """Liveness probe for the MCP endpoint — does not require an MCP session."""
    return {"status": "ok", "transport": "streamable-http"}


@mcp_router.api_route(
    "/",
    methods=["GET", "POST", "DELETE"],
)
@mcp_router.api_route(
    "",
    methods=["GET", "POST", "DELETE"],
)
async def mcp_endpoint_root(request: Request) -> Response:
    return await _dispatch_mcp(request)


@mcp_router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "DELETE"],
)
async def mcp_endpoint(request: Request) -> Response:
    return await _dispatch_mcp(request)


async def _dispatch_mcp(request: Request) -> Response:
    """All MCP traffic flows through here. Streamable HTTP handles its own routing."""
    manager = get_session_manager()
    sent = False
    captured: list[dict] = []

    async def _send(message: Any) -> None:
        nonlocal sent
        sent = True
        # Capture messages so we can return them as a real Response
        if isinstance(message, dict) and message.get("type") == "http.response.start":
            captured.append(message)
        elif isinstance(message, dict) and message.get("type") == "http.response.body":
            captured.append(message)

    # The MCP streamable HTTP transport requires an active task group.
    # We open one per request, handle it, then close.
    async with manager.run():
        await manager.handle_request(
            request.scope,
            request.receive,
            _send,
        )

    if not captured:
        return Response(status_code=404, content=b"MCP endpoint not found")

    # Reconstruct the response from the captured ASGI messages
    headers: list[tuple[bytes, bytes]] = []
    body_chunks: list[bytes] = []
    status_code = 200
    for msg in captured:
        if msg["type"] == "http.response.start":
            status_code = msg["status"]
            for k, v in msg.get("headers", []):
                headers.append((k, v))
        elif msg["type"] == "http.response.body":
            body_chunks.append(msg.get("body", b""))
    return Response(
        status_code=status_code,
        content=b"".join(body_chunks),
        headers={k.decode(): v.decode() for k, v in headers},
    )
