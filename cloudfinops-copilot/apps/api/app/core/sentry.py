"""Sentry integration. Only initializes if SENTRY_DSN is set."""
from __future__ import annotations

import logging

log = logging.getLogger("sentry")


def init_sentry(dsn: str | None, environment: str = "production", release: str | None = None) -> bool:
    if not dsn:
        log.info("Sentry DSN not set, skipping")
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
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            integrations=[FastApiIntegration(transaction_style="endpoint"), StarletteIntegration(), SqlalchemyIntegration()],
            send_default_pii=False,
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


def _scrub_event(event, hint):
    if "request" in event and "headers" in event.get("request", {}):
        for k in list(event["request"]["headers"].keys()):
            if k.lower() in ("authorization", "cookie", "x-api-key", "stripe-signature"):
                event["request"]["headers"][k] = "[REDACTED]"
    if "request" in event and isinstance(event["request"].get("data"), dict):
        for k in list(event["request"]["data"].keys()):
            if any(s in k.lower() for s in ("password", "secret", "token", "api_key")):
                event["request"]["data"][k] = "[REDACTED]"
    return event
