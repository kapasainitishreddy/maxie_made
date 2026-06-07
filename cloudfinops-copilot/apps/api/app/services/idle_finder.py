"""Idle resource finder — detect resources with no activity."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


class IdleFinder:
    """Find resources that haven't been used in N days."""

    IDLE_CPU_THRESHOLD = 5.0
    IDLE_DAYS = 7

    def find_idle(self, resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return idle resources (CPU < threshold, no recent network activity)."""
        idle = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.IDLE_DAYS)
        for r in resources:
            cpu = r.get("cpu_avg", 50.0)
            last_used = r.get("last_used")
            state = r.get("state", "running")

            is_idle = (
                (cpu < self.IDLE_CPU_THRESHOLD and state == "running")
                or (state == "stopped")
            )
            if isinstance(last_used, str):
                try:
                    lu = datetime.fromisoformat(last_used.replace("Z", "+00:00"))
                    if lu < cutoff:
                        is_idle = True
                except ValueError:
                    pass

            if is_idle:
                idle.append(r)
        return idle

    def estimate_savings(self, resource: dict[str, Any], hourly_cost: float = 0.05) -> float:
        """Estimate monthly savings from terminating an idle resource."""
        return round(hourly_cost * 730, 2)
