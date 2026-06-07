"""Clerk JWT verification + current-user dependency."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Annotated

import httpx
from fastapi import Depends, Header
from jose import JWTError, jwt

from app.config import get_settings
from app.core.errors import AuthError


@dataclass
class CurrentUser:
    """The authenticated user, derived from a verified Clerk JWT."""

    id: str            # Clerk user id (sub)
    email: str
    full_name: str | None
    org_id: str | None  # active org from the session token
    org_role: str | None


_JWKS_CACHE: dict[str, dict] = {}


async def _get_jwks(url: str) -> dict:
    if url in _JWKS_CACHE:
        return _JWKS_CACHE[url]
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        _JWKS_CACHE[url] = r.json()
        return _JWKS_CACHE[url]


async def verify_clerk_jwt(token: str) -> dict:
    """Verify a Clerk session JWT and return the decoded claims."""
    settings = get_settings()
    if not settings.clerk_jwks_url:
        # Dev mode: skip verification if no JWKS configured
        # In production, this branch is unreachable.
        return {"sub": "dev_user", "email": "dev@local", "org_id": None, "org_role": None}

    try:
        jwks = await _get_jwks(settings.clerk_jwks_url)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
        if not key:
            raise AuthError("Invalid token signing key")
        claims = jwt.decode(
            token,
            key,
            algorithms=[key.get("alg", "RS256")],
            options={"verify_aud": False},
        )
        return claims
    except JWTError as exc:
        raise AuthError(f"Invalid token: {exc}") from exc


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    """FastAPI dependency — extract and verify the Clerk JWT from the Authorization header.

    In dev mode (no CLERK_JWKS_URL configured), returns a stub user with no auth check
    so you can develop locally without setting up Clerk. In production with Clerk set up,
    the Authorization header is required and tokens are verified against Clerk's JWKS.
    """
    settings = get_settings()
    # Dev mode bypass: no Clerk configured → return dev user without auth check
    if not settings.clerk_jwks_url or settings.environment in ("development", "test"):
        if not authorization or not authorization.lower().startswith("bearer "):
            return CurrentUser(
                id="dev_user",
                email="dev@local",
                full_name="Dev User",
                org_id="dev_org",
                org_role="owner",
            )
        # Even in dev, if a token was provided, try to use it
        token = authorization.split(" ", 1)[1]
        claims = await verify_clerk_jwt(token)
        return CurrentUser(
            id=claims.get("sub", "dev_user"),
            email=claims.get("email", "dev@local"),
            full_name=claims.get("name") or claims.get("given_name"),
            org_id=claims.get("org_id", "dev_org"),
            org_role=claims.get("org_role", "owner"),
        )
    # Production: enforce auth
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AuthError("Missing or malformed Authorization header")
    token = authorization.split(" ", 1)[1]
    claims = await verify_clerk_jwt(token)
    return CurrentUser(
        id=claims.get("sub", ""),
        email=claims.get("email", ""),
        full_name=claims.get("name") or claims.get("given_name"),
        org_id=claims.get("org_id"),
        org_role=claims.get("org_role"),
    )


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
