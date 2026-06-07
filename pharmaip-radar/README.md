# PharmaIP Radar

**Pharmaceutical IP & patent intelligence platform** — scans global patent registries (USPTO, EPO, WIPO) and biomedical literature (PubMed, arXiv), maps overlapping IP patterns, flags infringement risk, and drafts formal compliance reports.

> **Pricing:** $999-4,999/mo per legal team · **Target:** 50 clients = **$1.5M+ ARR**

## Features

- 🔍 **Patent search** — query 100M+ patents via PatentsView + USPTO APIs
- 🗺️ **IP landscapes** — density heatmaps, top assignees, tech clusters, white space detection
- ⚠️ **Infringement alerts** — element-level claim analysis, claim charts, risk scoring
- 📄 **PDF reports** — FTO, landscape, infringement, patentability
- 🔌 **MCP server** — Claude/agents can call `search_patents`, `analyze_infringement`, etc.
- 🔐 **Clerk auth** + orgs, **Stripe** tiered billing

## Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind 3, shadcn/ui, Clerk, Recharts, Framer Motion |
| Backend | FastAPI 0.115+, SQLAlchemy 2.0 async, asyncpg, Pydantic v2, scikit-learn, reportlab |
| DB | Neon Postgres (free) |
| Cache | Upstash Redis (free) |
| LLM | Ollama (local, $0) — optional Claude API for premium users |
| Auth | Clerk (10k MAU free) |
| Billing | Stripe (no monthly fee) |
| Hosting | Vercel (web) + Fly.io (api) — both free tier |

**Total cost to launch: $0/mo until ~500 paying users.**

## Quick start

```bash
# Backend
cd apps/api
uv sync --all-extras
cp .env.example .env  # fill in keys
uv run pytest          # 41 tests, all passing
uv run uvicorn app.main:app --reload --port 8000

# Seed sample data
uv run python scripts/seed.py

# Frontend
cd ../web
pnpm install
cp .env.example .env.local
pnpm dev

# Or full stack via Docker
cd ../..
docker compose up
```

Open:
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

## Architecture

```
pharmaip-radar/
├── apps/
│   ├── api/      # FastAPI backend (port 8000)
│   │   ├── app/
│   │   │   ├── api/v1/        # REST endpoints
│   │   │   ├── core/          # security, errors, logging
│   │   │   ├── db.py, config.py, main.py
│   │   │   ├── models/        # SQLAlchemy ORM
│   │   │   ├── schemas/       # Pydantic v2
│   │   │   ├── services/      # USPTO, PubMed, similarity, infringement, PDF
│   │   │   └── mcp/           # MCP server
│   │   ├── alembic/           # migrations
│   │   ├── scripts/seed.py    # 20 sample pharma patents
│   │   └── tests/             # 41 pytest tests
│   └── web/      # Next.js 15 frontend (port 3000)
└── docker-compose.yml
```

## MCP Server (for AI agents)

Start the MCP server:
```bash
cd apps/api
uv run python -m app.mcp
```

Tools exposed:
- `search_patents(query, drug_name, therapeutic_area, assignee, limit)`
- `get_patent(patent_id)`
- `analyze_infringement(target_patent_id, candidate_patent_id)` → risk_score, severity, claim_chart
- `semantic_search(query, top_k)` → ranked patents by claim similarity
- `generate_report(report_type, title, target_drug)`

## Pricing tiers

| Tier | Price | Patents/mo | Landscapes | Watchlists | Features |
|---|---|---|---|---|---|
| **Starter** | $999/mo | 5,000 | 3 | 1 | Email alerts |
| **Pro** | $2,499/mo | 50,000 | ∞ | 10 | Infringement alerts, PDF reports, priority support |
| **Enterprise** | $4,999/mo | ∞ | ∞ | ∞ | API, SSO, audit logs, dedicated CSM |

## ICP & sales

- **Pharma IP attorneys** at Am Law 100 firms (lifetime value $50k+/yr)
- **In-house IP counsel** at top-50 pharma companies
- **Biotech innovation labs** needing landscape analysis
- **Generic manufacturers** running FTO before ANDA filing

**Outreach hook:** "Run a free FTO analysis on your top drug — see what we'd catch in 24 hours."

## Deploy

### Backend (Fly.io, free tier)
```bash
cd apps/api
fly launch
fly secrets set DATABASE_URL=... STRIPE_SECRET_KEY=...
fly deploy
```

### Frontend (Vercel)
```bash
cd apps/web
vercel --prod
# Add env: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, etc.
```

## Testing

```bash
cd apps/api
uv run pytest               # 41 tests
uv run pytest --cov=app     # coverage
```

Tested:
- Similarity engine (TF-IDF + element overlap)
- Infringement analyzer (claim chart, risk scoring)
- Landscape analyzer (density, clusters, top assignees, white space)
- PubMed client (respx mocks)
- PDF report builder (real PDFs, valid headers)
- Schema validation
