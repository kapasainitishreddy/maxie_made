"""FastAPI app entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api import api_router
from app.config import get_settings
from app.core.errors import AppError
from app.core.sentry import init_sentry
from app.schemas.common import HealthResponse

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("[startup] creating tables...")
    from app.db import engine, Base, AsyncSessionLocal
    import app.models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[startup] tables created")
    # Seed sample cloud accounts + recommendations + savings on first run
    from app.models.cloud_account import CloudAccount
    from app.models.recommendation import Recommendation, RecommendationType, RecommendationStatus, RiskLevel
    from app.models.savings import Savings
    from datetime import date as _date
    from sqlalchemy import select
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(CloudAccount).limit(1))
        if not result.scalar():
            import uuid as _uuid
            aws_id = _uuid.uuid4()
            gcp_id = _uuid.uuid4()
            org_id = _uuid.uuid4()
            sample = [
                CloudAccount(id=aws_id, org_id=org_id, account_name="Production AWS",
                             provider="aws", account_id="123456789012", region="us-east-1",
                             monthly_cost=45230.0, resource_count=247, active=True),
                CloudAccount(id=gcp_id, org_id=org_id, account_name="Staging GCP",
                             provider="gcp", account_id="my-project-staging", region="us-central1",
                             monthly_cost=8200.0, resource_count=43, active=True),
            ]
            session.add_all(sample)
            await session.commit()
            # Seed sample recommendations
            recs = [
                Recommendation(id=_uuid.uuid4(), account_id=aws_id, resource_id="i-0abc123",
                    resource_type="ec2_instance", rec_type=RecommendationType.SCHEDULE,
                    title="Schedule 4 dev RDS to run M-F 7am-9pm PT",
                    description="RDS db.t3.medium instances for dev environment running 24/7 but only used during business hours. Estimated savings: 70% of cost.",
                    current_cost=2850.0, projected_cost=855.0, monthly_savings=1995.0, risk=RiskLevel.LOW, status=RecommendationStatus.PENDING,
                    terraform_hcl='resource "aws_db_instance" "dev_rds" {\n  scheduled_actions = {\n    start  = "cron(0 14 ? * MON-FRI *)"\n    stop   = "cron(0 4 ? * SAT-SUN *)"\n  }\n}', evidence={"usage_hours_per_week": 50, "total_hours_possible": 168}),
                Recommendation(id=_uuid.uuid4(), account_id=aws_id, resource_id="i-0def456",
                    resource_type="ec2_instance", rec_type=RecommendationType.RIGHTSIZE,
                    title="Downsize m5.2xlarge to m5.large (3 instances)",
                    description="CPU utilization averaging 12% over 30 days. Right-sized to m5.large with no performance impact.",
                    current_cost=1840.0, projected_cost=460.0, monthly_savings=1380.0, risk=RiskLevel.LOW, status=RecommendationStatus.PENDING,
                    terraform_hcl='resource "aws_instance" "app" {\n  instance_type = "m5.large"  # was m5.2xlarge\n}', evidence={"avg_cpu_pct": 12, "p99_cpu_pct": 31}),
                Recommendation(id=_uuid.uuid4(), account_id=aws_id, resource_id="vol-789xyz",
                    resource_type="ebs_volume", rec_type=RecommendationType.TERMINATE_IDLE,
                    title="Delete 89 GB unattached EBS volumes + 14 old snapshots",
                    description="Volumes detached >90 days ago. Snapshots older than 1 year. Safe to delete after snapshot.",
                    current_cost=920.0, projected_cost=0.0, monthly_savings=920.0, risk=RiskLevel.LOW, status=RecommendationStatus.APPLIED,
                    terraform_hcl='resource "aws_ebs_volume" "old" {\n  # resource will be removed\n}\n', evidence={"volumes": 23, "snapshots": 14, "oldest_days": 412}),
                Recommendation(id=_uuid.uuid4(), account_id=gcp_id, resource_id="gke-cluster-prod",
                    resource_type="gke_cluster", rec_type=RecommendationType.RIGHTSIZE,
                    title="Migrate GKE prod cluster to Spot VMs for batch workloads",
                    description="Batch job nodes can tolerate preemption. Save 60-80% on compute for non-critical workloads.",
                    current_cost=2150.0, projected_cost=645.0, monthly_savings=1505.0, risk=RiskLevel.MEDIUM, status=RecommendationStatus.PENDING,
                    terraform_hcl='resource "google_container_node_pool" "batch" {\n  node_config {\n    spot = true\n  }\n}', evidence={"batch_workload_pct": 65, "preemption_tolerance": "high"}),
                Recommendation(id=_uuid.uuid4(), account_id=aws_id, resource_id="nat-gw-1",
                    resource_type="nat_gateway", rec_type=RecommendationType.RIGHTSIZE,
                    title="Consolidate 3 NAT gateways into 1 with VPC endpoint",
                    description="3 NAT gateways across AZs. Traffic analysis shows <40% utilization. Consolidate + add S3/DynamoDB VPC endpoints to bypass NAT.",
                    current_cost=1080.0, projected_cost=360.0, monthly_savings=720.0, risk=RiskLevel.MEDIUM, status=RecommendationStatus.PENDING,
                    terraform_hcl='# Delete 2 of 3 NAT gateways\n# Add VPC endpoints for s3 + dynamodb', evidence={"nat_gw_count": 3, "avg_utilization_pct": 38}),
            ]
            session.add_all(recs)
            await session.commit()
            # Seed savings events (last 30 days)
            from datetime import timedelta as _td
            today = _date.today()
            events = [
                Savings(id=_uuid.uuid4(), account_id=aws_id,
                    period_start=today - _td(days=30), period_end=today,
                    service="rds", raw_cost=2850.0, baseline_cost=2850.0, verified_savings=1995.0, currency="USD"),
                Savings(id=_uuid.uuid4(), account_id=aws_id,
                    period_start=today - _td(days=30), period_end=today,
                    service="ec2", raw_cost=1840.0, baseline_cost=1840.0, verified_savings=1380.0, currency="USD"),
                Savings(id=_uuid.uuid4(), account_id=aws_id,
                    period_start=today - _td(days=30), period_end=today,
                    service="ebs", raw_cost=920.0, baseline_cost=920.0, verified_savings=920.0, currency="USD"),
                Savings(id=_uuid.uuid4(), account_id=gcp_id,
                    period_start=today - _td(days=30), period_end=today,
                    service="gke", raw_cost=2150.0, baseline_cost=2150.0, verified_savings=0.0, currency="USD"),
            ]
            session.add_all(events)
            await session.commit()
            print(f"[startup] seeded {len(sample)} cloud accounts, {len(recs)} recommendations, {len(events)} savings events")
    yield


app = FastAPI(title=settings.app_name, version=__version__, debug=settings.debug, lifespan=lifespan)

# Initialize Sentry (no-op if SENTRY_DSN is not set)
if hasattr(settings, "sentry_dsn") and settings.sentry_dsn:
    init_sentry(settings.sentry_dsn, environment=settings.environment, release=getattr(settings, "version", None))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Install security middleware (rate limit + security headers)
from app.core.security_middleware import add_security_middleware
add_security_middleware(app)
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"code": exc.code, "message": exc.message})


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name, version=__version__, env=settings.environment)


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {"name": settings.app_name, "version": __version__, "docs": "/docs"}
