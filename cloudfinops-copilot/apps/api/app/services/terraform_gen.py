"""Terraform HCL generator from recommendations."""
from __future__ import annotations

from typing import Any


class TerraformGen:
    """Generate valid Terraform HCL for AWS resources."""

    @staticmethod
    def rightsize_instance(resource_id: str, current_type: str, target_type: str) -> str:
        return f"""# Right-size EC2 instance from {current_type} to {target_type}
# Estimated savings: see recommendation metadata

resource "aws_instance" "{resource_id}" {{
  # NOTE: changing instance_type requires a stop/start
  instance_type = "{target_type}"
  # ... (other attrs preserved from current state)
}}

# To apply without downtime, use aws_launch_template or migrate to ASG
"""

    @staticmethod
    def terminate_idle(resource_id: str, resource_type: str) -> str:
        if resource_type == "ec2":
            return f"""# Terminate idle EC2 instance
# IMPORTANT: snapshot any EBS volumes first

resource "null_resource" "snapshot_{resource_id}" {{
  triggers = {{ id = "{resource_id}" }}
}}

# Then run:
# aws ec2 terminate-instances --instance-ids {resource_id}
"""
        elif resource_type == "rds":
            return f"""# Take final snapshot then delete idle RDS instance
resource "aws_db_instance" "{resource_id}_archived" {{
  identifier              = "{resource_id}"
  skip_final_snapshot     = false
  final_snapshot_identifier = "{resource_id}-final-${{formatdate("YYYY-MM-DD", timestamp())}}"
  # Set deletion_protection = false first
}}
"""
        return f"# Manual removal required for {resource_type} {resource_id}\n"

    @staticmethod
    def schedule_nonprod(resource_id: str, schedule: str = "mon-fri-09-18") -> str:
        return f"""# Auto-stop non-prod instance on schedule
# Uses aws_instance_scheduler via SSM Automation

module "scheduler" {{
  source  = "terraform-aws-modules/scheduler/aws"
  version = "~> 1.0"

  schedule_name = "non-prod-schedule"
  tag_key       = "Schedule"
  tag_value     = "{schedule}"

  schedules = {{
    "{resource_id}" = {{
      timezone = "UTC"
      stop     = "19:00"
      start    = "09:00"
      weekdays = ["MON", "TUE", "WED", "THU", "FRI"]
    }}
  }}
}}
"""

    @staticmethod
    def graviton_migration(resource_id: str, current_type: str, target_type: str) -> str:
        return f"""# Migrate from {current_type} (Intel) to {target_type} (Graviton ARM)
# ~20% cost savings + ~40% perf/watt improvement

# Requires recompilation of native code; test thoroughly.
resource "aws_instance" "{resource_id}" {{
  instance_type = "{target_type}"
  # AMI must be arm64-compatible
}}
"""

    @staticmethod
    def for_recommendation(rec: dict[str, Any]) -> str:
        """Dispatch to the right generator based on rec_type."""
        rec_type = rec.get("rec_type", "")
        rid = rec.get("resource_id", "")
        rtype = rec.get("resource_type", "")

        if rec_type == "rightsize":
            return TerraformGen.rightsize_instance(
                rid, rec.get("evidence", {}).get("current_type", ""),
                rec.get("evidence", {}).get("target_type", ""),
            )
        if rec_type == "terminate_idle":
            return TerraformGen.terminate_idle(rid, rtype)
        if rec_type == "schedule":
            return TerraformGen.schedule_nonprod(rid)
        if rec_type == "graviton":
            return TerraformGen.graviton_migration(
                rid, rec.get("evidence", {}).get("current_type", ""),
                rec.get("evidence", {}).get("target_type", ""),
            )
        return f"# No generator for {rec_type}\n"
