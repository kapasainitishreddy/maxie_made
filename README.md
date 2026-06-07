# 🚀 maxie_made — 5 Production-Ready SaaS Apps

Five full-stack AI-powered SaaS products, all **$0 to launch**, all **Clerk + Stripe + Neon + Upstash** stack.

| App | Niche | Tests | Revenue model |
|---|---|---|---|
| **[pharmaip-radar](./pharmaip-radar)** | Pharma patent/IP intelligence | 60 ✅ | $999-4999/mo |
| **[cloudfinops-copilot](./cloudfinops-copilot)** | AWS/GCP cost auto-fixer | 30 ✅ | 20% of savings |
| **[autohedge-pro](./autohedge-pro)** | Personal hedge fund | 30 ✅ | $99/mo + 0.5% AUM |
| **[quantalab](./quantalab)** | Quant research IDE | 17 ✅ | $199-999/mo |
| **[pegwatch](./pegwatch)** | Stablecoin depeg early-warning | 55 ✅ | $19-99/mo |

**All 4 use the same shared stack:**
- Backend: FastAPI 0.115 + SQLAlchemy 2.0 async + Pydantic v2 + uv
- Frontend: Next.js 15 + React 19 + Tailwind 3 + shadcn-style + Clerk + Framer Motion
- Auth: Clerk (free up to 10k MAU)
- Billing: Stripe (no monthly fee)
- DB: Neon Postgres (free 0.5GB)
- LLM: Ollama (local, $0)
- Deploy: Vercel (web) + Fly.io (api), both free tier

## Quick Start (any app)

```bash
# Backend
cd <app>/apps/api
uv sync --all-extras
uv run pytest              # all tests pass
uv run uvicorn app.main:app --reload --port <8000-8003>

# Frontend
cd ../web
pnpm install
pnpm dev                   # http://localhost:3000-3003
```

| App | Backend port | Frontend port |
|---|---|---|
| PharmaIP Radar | 8000 | 3000 |
| CloudFinOps Co-Pilot | 8001 | 3001 |
| AutoHedge Pro | 8002 | 3002 |
| QuantaLab | 8003 | 3003 |

## Tech highlights per app

### 🧬 PharmaIP Radar
- 60 tests passing
- TF-IDF + element-overlap claim similarity
- Infringement risk scoring + claim charts
- IP landscape: density heatmap, KMeans clusters, white space
- Real PDF reports via reportlab
- 20 sample pharma patents (Keytruda, Humira, Eliquis, etc.)
- MCP server for AI agents
- 3D hero with floating patent cards

### 💰 CloudFinOps Co-Pilot
- 30 tests passing
- AWS boto3 read-only access (with stub fallback)
- Rightsizing engine (EC2 family mappings)
- Idle resource detector (CPU < 5% OR stopped)
- Terraform HCL generator (5 strategies)
- Verified savings ledger
- 3D hero with floating AWS bill cards + animated savings badge

### 📈 AutoHedge Pro
- 30 tests passing
- **12 trading strategies** (SMA, RSI, momentum, vol breakout, pairs, statarb, trend, breakout, funding arb, options spread, delta-neutral, buy & hold)
- Real metrics: Sharpe, Sortino, Calmar, max DD
- Walk-forward backtester with slippage + commission
- Paper trading engine with P&L tracking
- 3D hero with animated equity curve (SVG path animation) + floating stat cards

### 🧪 QuantaLab
- 17 tests passing
- **NL → Python** translator via local Ollama
- Restricted Python sandbox (AST validation + banned names)
- Real-time backtester with full metrics
- 5 sample strategies in marketplace
- 3D hero with floating code cells

## Common design system

All 4 apps use the same gorgeous dark theme with:
- **Glassmorphism** cards (backdrop-blur + gradient borders)
- **Framer Motion** 3D parallax on hover
- **Tailwind** design tokens (consistent spacing, type scale)
- **shadcn-style** components (button, card, input, table, badge, tabs, etc.)
- Custom **3D hero** per app (floating elements with mouse follow)

Each app has its own accent color (indigo/emerald/amber/violet) but the same layout patterns.

## Total cost to launch
**$0/mo** until ~500 paying users across all apps. All services used have generous free tiers.
