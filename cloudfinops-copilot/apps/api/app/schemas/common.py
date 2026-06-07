"""Common schemas."""
from __future__ import annotations
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str
    version: str
    env: str
