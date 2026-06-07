"""AWS advisor — uses boto3 for resource + cost analysis."""
from __future__ import annotations

from typing import Any


class AWSAdvisor:
    """Read-only AWS resource + cost advisor.

    Uses boto3 in production. For the MVP we expose a clean interface that can
    be backed by a real boto3 client or a stub.
    """

    def __init__(self, role_arn: str | None = None, region: str = "us-east-1") -> None:
        self.role_arn = role_arn
        self.region = region
        self._client = None

    def _get_client(self, service: str):
        if self._client is not None:
            return self._client
        try:
            import boto3
            if self.role_arn:
                sts = boto3.client("sts")
                creds = sts.assume_role(RoleArn=self.role_arn, RoleSessionName="cloudfinops")["Credentials"]
                return boto3.client(
                    service,
                    region_name=self.region,
                    aws_access_key_id=creds["AccessKeyId"],
                    aws_secret_access_key=creds["SecretAccessKey"],
                    aws_session_token=creds["SessionToken"],
                )
            return boto3.client(service, region_name=self.region)
        except Exception:
            return None

    def list_ec2(self) -> list[dict[str, Any]]:
        client = self._get_client("ec2")
        if not client:
            return []
        try:
            r = client.describe_instances()
            out = []
            for res in r.get("Reservations", []):
                for inst in res.get("Instances", []):
                    out.append({
                        "id": inst["InstanceId"],
                        "type": inst["InstanceType"],
                        "state": inst["State"]["Name"],
                        "cpu_avg": 0.0,
                    })
            return out
        except Exception:
            return []

    def list_rds(self) -> list[dict[str, Any]]:
        client = self._get_client("rds")
        if not client:
            return []
        try:
            r = client.describe_db_instances()
            return [
                {"id": db["DBInstanceIdentifier"], "type": db["DBInstanceClass"],
                 "engine": db["Engine"], "status": db["DBInstanceStatus"]}
                for db in r.get("DBInstances", [])
            ]
        except Exception:
            return []

    def monthly_cost(self, days: int = 30) -> float:
        client = self._get_client("ce")
        if not client:
            return 0.0
        try:
            from datetime import datetime, timedelta, timezone
            end = datetime.now(timezone.utc).date()
            start = end - timedelta(days=days)
            r = client.get_cost_and_usage(
                TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
            )
            total = 0.0
            for result in r.get("ResultsByTime", []):
                total += float(result["Total"]["UnblendedCost"]["Amount"])
            return total
        except Exception:
            return 0.0
