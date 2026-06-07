"""Security middleware: rate limiting, security headers, request validation."""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)


# === Security headers (OWASP recommended) ===
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    # CSP: allow self + inline styles (Tailwind), Plausible analytics
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://plausible.io; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https://plausible.io; "
        "frame-ancestors 'none'"
    ),
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter (per-IP, per-endpoint).

    Production: replace with Redis-backed limiter (slowapi + redis).
    Free tier: 100 req/min per IP, 10 req/min for write endpoints.
    """

    def __init__(self, app, requests_per_minute: int = 100, write_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.write_per_minute = write_per_minute
        self.buckets: dict[str, list[datetime]] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        # In production behind a proxy, use X-Forwarded-For
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _clean_bucket(self, bucket: list[datetime], window: timedelta) -> list[datetime]:
        cutoff = datetime.utcnow() - window
        return [t for t in bucket if t > cutoff]

    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)
        method = request.method
        path = request.url.path

        # Skip rate limiting for health checks
        if path.endswith("/health") or path == "/":
            return await call_next(request)

        # Stricter limit for write operations
        is_write = method in ("POST", "PUT", "PATCH", "DELETE")
        limit = self.write_per_minute if is_write else self.requests_per_minute
        window = timedelta(minutes=1)

        key = f"{client_ip}:{method}:{path}"
        bucket = self._clean_bucket(self.buckets[key], window)

        if len(bucket) >= limit:
            logger.warning(f"Rate limit hit: {key} ({len(bucket)}/{limit})")
            return JSONResponse(
                status_code=429,
                content={
                    "code": "rate_limit_exceeded",
                    "message": f"Too many requests. Limit: {limit}/min. Try again later.",
                },
                headers={"Retry-After": "60"},
            )

        bucket.append(datetime.utcnow())
        self.buckets[key] = bucket

        return await call_next(request)


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Block obviously malicious requests (SQL injection patterns in URLs, oversized payloads)."""

    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB

    SUSPICIOUS_PATTERNS = [
        "union select",
        "drop table",
        "<script",
        "javascript:",
        "onerror=",
        "onload=",
    ]

    async def dispatch(self, request: Request, call_next):
        # Check URL for suspicious patterns
        url = str(request.url).lower()
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in url:
                logger.warning(f"Suspicious URL blocked: {url[:200]}")
                return JSONResponse(
                    status_code=400,
                    content={"code": "bad_request", "message": "Suspicious request pattern detected."},
                )

        # Check body size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_BODY_SIZE:
            return JSONResponse(
                status_code=413,
                content={"code": "payload_too_large", "message": "Request body too large."},
            )

        return await call_next(request)


def add_security_middleware(app: FastAPI) -> None:
    """Register all security middleware on a FastAPI app.

    Order matters: validation -> rate limit -> security headers.
    """
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=100, write_per_minute=30)
    app.add_middleware(RequestValidationMiddleware)
    logger.info("Security middleware enabled: rate limit + security headers + request validation")
