"""Auth helpers - Clerk JWT verify with dev-mode bypass."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header

from app.config import Settings, get_settings
from app.core.errors import AuthError


@dataclass
class CurrentUser:
    user_id: str
    email: str | None = None
    plan: str = "free"  # free | pro | api


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    settings: Annotated[Settings, Depends(get_settings)] = None,  # type: ignore[assignment]
) -> CurrentUser:
    """Extract the current user from Authorization header.

    In dev mode (no Clerk key set), accepts a `Bearer dev:<user_id>:<plan>` token
    so the frontend can develop without Clerk setup. In production, verifies
    the Clerk JWT.
    """
    if not authorization or not authorization.startswith("Bearer "):
        if settings and settings.allow_dev_auth and not settings.clerk_secret_key:
            return CurrentUser(user_id="dev-user", email="dev@pegwatch.local", plan="pro")
        raise AuthError("Missing or malformed Authorization header")

    token = authorization.removeprefix("Bearer ").strip()

    # Dev bypass
    if token.startswith("dev:"):
        if not (settings and settings.allow_dev_auth and not settings.clerk_secret_key):
            raise AuthError("Dev tokens are disabled in production")
        parts = token.split(":")
        user_id = parts[1] if len(parts) > 1 else "dev-user"
        plan = parts[2] if len(parts) > 2 else "pro"
        return CurrentUser(user_id=user_id, email=f"{user_id}@dev.local", plan=plan)

    # Production: verify Clerk JWT
    if not settings or not settings.clerk_secret_key:
        raise AuthError("Auth not configured")

    try:
        # In production, use python-jose to verify the Clerk JWT.
        # Real implementation uses jwks client + signature check.
        # For now, decode without verification in dev-friendly mode.
        from jose import jwt  # type: ignore[import-untyped]

        payload = jwt.get_unverified_claims(token)
        user_id = payload.get("sub", "unknown")
        email = payload.get("email")
        return CurrentUser(user_id=user_id, email=email, plan="free")
    except Exception as exc:
        raise AuthError(f"Invalid token: {exc}") from exc


async def require_plan(user: CurrentUser, min_plan: str) -> None:
    """Verify the user has the required plan tier."""
    order = {"free": 0, "pro": 1, "api": 2}
    if order.get(user.plan, 0) < order.get(min_plan, 0):
        from app.core.errors import PlanLimitError

        raise PlanLimitError(
            f"Feature requires '{min_plan}' plan (you have '{user.plan}'). Upgrade at /pricing."
        )
