# CloudFinOps Co-Pilot

**Auto-find and fix AWS/GCP/Azure cost waste. Performance-based pricing — 20% of verified savings.**

> **Target:** 50 clients × $20k saved/mo = **$2.4M ARR**

## Quick start

```bash
# Backend (port 8001)
cd apps/api
uv sync --all-extras
uv run pytest  # 30 tests
uv run uvicorn app.main:app --reload --port 8001

# Frontend (port 3001)
cd apps/web
pnpm install
pnpm dev
# Open http://localhost:3001
```

## Features
- AWS boto3 read-only access (list EC2/RDS, Cost Explorer)
- Right-sizing engine with EC2 instance family mappings
- Idle resource detector (CPU < 5% OR stopped)
- Terraform HCL generator (rightsize, terminate, schedule, graviton)
- Verified savings ledger
- Stripe (performance-based billing)

## Architecture
- 30+ backend files, FastAPI + SQLAlchemy + Pydantic v2
- 14+ frontend files, Next.js 15 + Tailwind + framer-motion
- 3D hero with floating AWS bill cards (parallax mouse follow)
- 30 passing pytest tests
