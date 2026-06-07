"""Sentry integration for the API.

Only initializes if SENTRY_DSN is set. Safe to call in dev (no-op).
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("sentry")


def init_sentry(dsn: str | None, environment: str = "production", release: str | None = None) -> bool:
    """Initialize Sentry. Returns True if initialized, False if skipped (no DSN).

    Usage:
        from app.core.sentry import init_sentry
        if settings.sentry_dsn:
            init_sentry(settings.sentry_dsn, settings.environment, settings.release)
    """
    if not dsn:
        log.info("Sentry DSN not set, skipping initialization")
        return False

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            release=release,
            traces_sample_rate=0.1,  # 10% of transactions
            profiles_sample_rate=0.1,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                StarletteIntegration(),
                SqlalchemyIntegration(),
            ],
            # Don't send PII automatically
            send_default_pii=False,
            # Scrub sensitive data
            before_send=_scrub_event,
        )
        log.info("Sentry initialized for environment=%s", environment)
        return True
    except ImportError:
        log.warning("sentry-sdk not installed, skipping")
        return False
    except Exception as e:
        log.error("Sentry init failed: %s", e)
        return False


def _scrub_event(event: dict[str, Any], hint: dict[str, Any]) -> dict[str, Any] | None:
    """Scrub sensitive data from Sentry events before sending."""
    # Remove Authorization headers
    if "request" in event and "headers" in event["request"]:
        headers = event["request"]["headers"]
        for k in list(headers.keys()):
            if k.lower() in ("authorization", "cookie", "x-api-key", "stripe-signature"):
                headers[k] = "[REDACTED]"

    # Remove password/secret fields from form data
    if "request" in event and "data" in event["request"]:
        data = event["request"]["data"]
        if isinstance(data, dict):
            for k in list(data.keys()):
                if any(s in k.lower() for s in ("password", "secret", "token", "api_key")):
                    data[k] = "[REDACTED]"

    return event
