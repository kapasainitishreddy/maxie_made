"""Rightsizing engine — recommend optimal instance types based on usage."""
from __future__ import annotations

from typing import Any


# AWS EC2 instance type pricing (rough, us-east-1 Linux on-demand hourly USD)
INSTANCE_PRICING = {
    "t3.nano": 0.0052, "t3.micro": 0.0104, "t3.small": 0.0208, "t3.medium": 0.0416,
    "t3.large": 0.0832, "t3.xlarge": 0.1664, "t3.2xlarge": 0.3328,
    "m5.large": 0.096, "m5.xlarge": 0.192, "m5.2xlarge": 0.384, "m5.4xlarge": 0.768,
    "c5.large": 0.085, "c5.xlarge": 0.17, "c5.2xlarge": 0.34,
    "r5.large": 0.126, "r5.xlarge": 0.252, "r5.2xlarge": 0.504,
    "t4g.small": 0.0168, "t4g.medium": 0.0336, "t4g.large": 0.0672,
}

# Family equivalence (instance generation downsize if CPU < 25%)
FAMILY_DOWNSIZE = {
    "m5.xlarge": "m5.large", "m5.2xlarge": "m5.xlarge", "m5.4xlarge": "m5.2xlarge",
    "c5.xlarge": "c5.large", "c5.2xlarge": "c5.xlarge",
    "r5.xlarge": "r5.large", "r5.2xlarge": "r5.xlarge",
}


def hourly_to_monthly(h: float) -> float:
    return round(h * 730, 2)


class RightSizer:
    """Recommend right-sizing based on CPU + memory utilization."""

    LOW_CPU_THRESHOLD = 25.0
    HIGH_CPU_THRESHOLD = 80.0

    def recommend(self, resource: dict[str, Any]) -> dict[str, Any] | None:
        """Return a recommendation dict if instance is over/under-provisioned, else None."""
        current_type = resource.get("type")
        if not current_type or current_type not in INSTANCE_PRICING:
            return None
        cpu = resource.get("cpu_avg", 50.0)
        current_hourly = INSTANCE_PRICING[current_type]
        current_monthly = hourly_to_monthly(current_hourly)

        target_type = None
        if cpu < self.LOW_CPU_THRESHOLD:
            target_type = FAMILY_DOWNSIZE.get(current_type)
            if not target_type and current_type in ("m5.2xlarge", "c5.2xlarge", "r5.2xlarge"):
                # Already at 2xlarge, jump to 1 size down within family
                target_type = current_type.replace("2xlarge", "xlarge")
        elif cpu > self.HIGH_CPU_THRESHOLD:
            return None  # under-provisioned, no savings

        if not target_type or target_type not in INSTANCE_PRICING:
            return None

        target_hourly = INSTANCE_PRICING[target_type]
        target_monthly = hourly_to_monthly(target_hourly)
        savings = round(current_monthly - target_monthly, 2)
        if savings < 5:
            return None

        return {
            "current_type": current_type,
            "target_type": target_type,
            "current_cost": current_monthly,
            "projected_cost": target_monthly,
            "monthly_savings": savings,
            "evidence": {"cpu_avg_pct": cpu, "method": "rightsizing"},
        }
