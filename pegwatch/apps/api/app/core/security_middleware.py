"""Security middleware: rate limiting + OWASP security headers."""
from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# 60 req/min/IP - simple in-memory bucket
_RATE_BUCKET: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT = 60
_RATE_WINDOW = 60.0


class SecurityMiddleware(BaseHTTPMiddleware):
    """Adds OWASP security headers + a simple in-memory rate limiter."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Rate limit (skip health + docs)
        if request.url.path not in ("/health", "/docs", "/openapi.json", "/redoc"):
            ip = request.client.host if request.client else "unknown"
            now = time.time()
            window = _RATE_BUCKET[ip]
            # Drop expired
            while window and now - window[0] > _RATE_WINDOW:
                window.pop(0)
            if len(window) >= _RATE_LIMIT:
                return Response(
                    content='{"detail":"Rate limit exceeded"}',
                    media_type="application/json",
                    status_code=429,
                )
            window.append(now)

        response = await call_next(request)

        # OWASP security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # CSP - allow self + Clerk + Stripe + Ollama (dev only)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://*.clerk.accounts.dev https://js.stripe.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://*.clerk.accounts.dev https://api.stripe.com; "
            "frame-src https://*.clerk.accounts.dev https://js.stripe.com; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
        response.headers["Content-Security-Policy"] = csp

        return response
