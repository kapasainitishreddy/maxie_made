# 🚀 maxie_made — 4 Production-Ready SaaS Apps

Four full-stack SaaS products, all **$0 to launch**, all **FastAPI + Next.js 15 + SQLite/Postgres**.

[![CI](https://github.com/kapasainitishreddy/maxie_made/actions/workflows/ci.yml/badge.svg)](https://github.com/kapasainitishreddy/maxie_made/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## One-click deploy to Netlify

| App | Deploy | Live Demo (after deploy) |
|---|---|---|
| **PharmaIP Radar** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=pharmaip-radar%2Fapps%2Fweb) | `pharmaip-radar.netlify.app` |
| **CloudFinOps Co-Pilot** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=cloudfinops-copilot%2Fapps%2Fweb) | `cloudfinops-copilot.netlify.app` |
| **AutoHedge Pro** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=autohedge-pro%2Fapps%2Fweb) | `autohedge-pro.netlify.app` |
| **QuantaLab** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=quantalab%2Fapps%2Fweb) | `quantalab.netlify.app` |

> Click any button above → it forks this repo to your account and deploys that app's frontend to Netlify. Backend is separate (see [Deployment](#deployment) below).

## All 4 Apps

| App | Niche | Tests | Revenue model |
|---|---|---|---|
| **[pharmaip-radar](./pharmaip-radar)** | Pharma patent/IP intelligence | 60 ✅ | $999-4999/mo |
| **[cloudfinops-copilot](./cloudfinops-copilot)** | AWS/GCP cost auto-fixer | 30 ✅ | 20% of savings |
| **[autohedge-pro](./autohedge-pro)** | Personal hedge fund | 33 ✅ | $99/mo + 0.5% AUM |
| **[quantalab](./quantalab)** | Quant research IDE | 17 ✅ | $199-999/mo |

**Stack (all 4):**
- Backend: FastAPI 0.115 + SQLAlchemy 2.0 async + Pydantic v2 + uv
- Frontend: Next.js 15 + React 19 + Tailwind 3 + Clerk + Framer Motion
- Auth: Clerk (free up to 10k MAU) — dev bypass works without keys
- Billing: Stripe (no monthly fee)
- DB: SQLite (local) / Neon Postgres (prod, free 0.5GB)
- LLM: Ollama (local, $0)
- Deploy: Netlify (web, $0) + Fly.io (api, $0)

## Quick Start (any app)

```bash
# Backend
cd <app>/apps/api
uv sync --all-extras
uv run pytest              # all tests pass
uv run uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd <app>/apps/web
pnpm install
pnpm dev
```

Open http://localhost:3000 for the frontend, http://localhost:8000/docs for the API.

## Deployment

### Frontend → Netlify (free, one click)

**Option A: Use the deploy buttons above** (fastest, no CLI needed)

**Option B: Use the helper script** (after installing [netlify-cli](https://docs.netlify.com/cli/get-started/)):

```bash
cd maxie_made
./scripts/deploy-netlify.sh
```

This deploys all 4 apps at once. See [scripts/README.md](./scripts/README.md) for details.

### Backend → Fly.io (free tier)

```bash
# Install: https://fly.io/docs/hands-on/install-flyctl/
fly auth signup

# Per app:
cd pharmaip-radar/apps/api
fly launch --name pharmaip-radar-api
fly secrets set DATABASE_URL=postgresql://... CLERK_JWKS_URL=https://...
fly deploy
```

The frontend's `NEXT_PUBLIC_API_URL` env var should point to your Fly URL (e.g. `https://pharmaip-radar-api.fly.dev`).

### Database → Neon (free Postgres, 0.5GB)

1. Sign up at https://neon.tech with GitHub
2. Create a project, copy the `postgresql+asyncpg://...` connection string
3. Set it as `DATABASE_URL` in your backend's env (Fly.io secrets)

For local dev, SQLite is used by default (no setup needed).

## What's included

- ✅ **140 backend tests** passing (4 apps × 35 avg tests)
- ✅ **Custom SVG logos** for all 4 apps
- ✅ **3D animated heroes** with floating cards
- ✅ **"How it works"** 4-step process diagrams
- ✅ **"Real case study"** scenario sections
- ✅ **Working dashboards** with real seeded data
- ✅ **Pricing pages** for all 4 apps
- ✅ **Privacy / Terms / Security** pages for all 4 apps
- ✅ **Rate limiting** (100/min read, 30/min write per IP)
- ✅ **OWASP security headers** (HSTS, CSP, X-Frame-Options, etc.)
- ✅ **Sentry** error tracking (no-op when DSN not set)
- ✅ **Plausible** privacy-friendly analytics (no-op when domain not set)
- ✅ **CI/CD** via GitHub Actions (pytest + pip-audit + bandit + pnpm audit)
- ✅ **Weekly security scans** scheduled in CI
- ✅ **netlify.toml** for all 4 apps (one-click deploy)
- ✅ **Helper scripts** for bash and Windows

## License

MIT — see [LICENSE](./LICENSE) (add this file before going public).
