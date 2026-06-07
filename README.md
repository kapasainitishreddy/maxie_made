# 🚀 maxie_made — 5 Production-Ready SaaS Apps

Five full-stack SaaS products, all **$0 to launch**, all **FastAPI + Next.js 15 + SQLite/Postgres**.

[![CI](https://github.com/kapasainitishreddy/maxie_made/actions/workflows/ci.yml/badge.svg)](https://github.com/kapasainitishreddy/maxie_made/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## One-click deploy to Netlify

| App | Deploy | Live URL (after deploy) |
|---|---|---|
| **PharmaIP Radar** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=pharmaip-radar%2Fapps%2Fweb) | `pharmaip-radar.netlify.app` |
| **CloudFinOps Co-Pilot** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=cloudfinops-copilot%2Fapps%2Fweb) | `cloudfinops-copilot.netlify.app` |
| **AutoHedge Pro** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=autohedge-pro%2Fapps%2Fweb) | `autohedge-pro.netlify.app` |
| **QuantaLab** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https%3A%2F%2Fgithub.com%2Fkapasainitishreddy%2Fmaxie_made&base=quantalab%2Fapps%2Fweb) | `quantalab.netlify.app` |

> Click any button → forks repo → Netlify deploys that app's frontend. Backend (Fly.io) is separate, see [Deployment](#deployment).

## All 4 Apps

| App | Niche | Tests | Revenue model |
|---|---|---|---|
| **[pharmaip-radar](./pharmaip-radar)** | Pharma patent/IP intelligence | 63 ✅ | $999-4999/mo |
| **[cloudfinops-copilot](./cloudfinops-copilot)** | AWS/GCP cost auto-fixer | 33 ✅ | 20% of savings |
| **[autohedge-pro](./autohedge-pro)** | Personal hedge fund | 36 ✅ | $99/mo + 0.5% AUM |
| **[quantalab](./quantalab)** | Quant research IDE | 20 ✅ | $199-999/mo |
| **[pegwatch](./pegwatch)** | Stablecoin depeg early-warning | 57 ✅ | $19-99/mo |

**Stack:**
- Backend: FastAPI 0.115 + SQLAlchemy 2.0 async + Pydantic v2 + uv
- Frontend: Next.js 15 + React 19 + Tailwind 3 + Clerk + Framer Motion
- Auth: Clerk (free 10k MAU) — dev bypass works without keys
- DB: SQLite (local) / Neon Postgres (prod, free 0.5GB)
- Deploy: **Netlify** (frontend, $0) + **Fly.io** (backend, $0)

## Quick Start (local)

```bash
# Backend
cd <app>/apps/api
uv sync --all-extras
uv run pytest
uv run uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd <app>/apps/web
pnpm install
pnpm dev
```

Open http://localhost:3000 (frontend), http://localhost:8000/docs (API).

## Deployment (free)

### 1. Frontend → Netlify (one click or script)

```bash
npm install -g netlify-cli
netlify login
./scripts/deploy-netlify.sh
```

This deploys all 4 frontends. Each gets a free `*.netlify.app` URL.

### 2. Backend → Fly.io (one command for all 4)

```bash
curl -L https://fly.io/install.sh | sh  # install
fly auth signup
./scripts/deploy-fly.sh
```

This deploys all 4 backends to `*.fly.dev`. Free tier: 3 shared VMs, 256MB RAM each, auto-stops when idle.

### 3. Database → Neon (free 0.5GB Postgres)

```bash
# Sign up at https://neon.tech (GitHub OAuth, 2 min)
./scripts/setup-neon.sh
```

Paste your connection string when prompted. Auto-configures all 4 backends.

### 4. Auth → Clerk (free 10k MAU)

```bash
# Sign up at https://clerk.com (GitHub OAuth, 2 min)
./scripts/setup-clerk.sh
```

Paste your keys when prompted. The dev bypass auto-disables when keys are present.

### 5. Wire it all together

```bash
./scripts/connect-frontend-to-backend.sh
```

Updates the frontend env vars to point to the live backends, triggers a redeploy.

## Custom domains — cost guide

| Option | Cost | Notes |
|---|---|---|
| Free `*.netlify.app` subdomain | $0 | Fine for testing/portfolio |
| Free `*.fly.dev` subdomain | $0 | For backend |
| `.com` domain | $9-15/yr | Buy from Cloudflare Registrar or Porkbun |
| `.app` domain | $15/yr | Good for SaaS feel |
| `.io` domain | $30-50/yr | Premium dev tool feel |
| 1 `.com` + 15 subdomains | $10/yr total | Cheapest real-launch option |

**My pick for 15 apps**: Buy 1 `.com` (e.g. `yourcompany.com`), use subdomains: `pharmaip.yourcompany.com`, `cloud.yourcompany.com`, etc. **$10/yr total.**

Free alternatives if you really want $0:
- `pharmaip.netlify.app` (works, looks decent)
- `pharmaip.onrender.com` (less pro)
- Use just the GitHub Pages URL

## What's included

- ✅ **209 backend tests** passing (was 140, +69 from billing tests + 5th app)
- ✅ **Custom SVG logos** for all 4 apps
- ✅ **3D animated heroes** with floating cards
- ✅ **"How it works"** + **"Real case study"** sections
- ✅ **Working dashboards** with real seeded data
- ✅ **Pricing pages** + **Privacy/Terms/Security** pages
- ✅ **Rate limiting** (100/min read, 30/min write per IP)
- ✅ **OWASP security headers** (HSTS, CSP, X-Frame-Options, etc.)
- ✅ **Sentry** error tracking (no-op when DSN not set)
- ✅ **Plausible** privacy-friendly analytics (no-op when domain not set)
- ✅ **CI/CD** via GitHub Actions (pytest + pip-audit + bandit + pnpm audit)
- ✅ **Weekly security scans** scheduled in CI
- ✅ **Custom SVG logos** for all 5 apps
- ✅ **netlify.toml** for all 5 apps (one-click deploy)
- ✅ **fly.toml** for all 5 apps (one-command deploy)
- ✅ **Auto-deploy to Netlify** on push to main (5 sites)
- ✅ **Post-deploy health checks** every 6h + weekly dep audit
- ✅ **Stripe billing** integrated in all 5 apps (checkout + portal + webhook)
- ✅ **Helper scripts** for bash and Windows
- ✅ **Auto-setup scripts** for Clerk + Neon

## Cost summary (per month, until you scale)

| Service | Free tier | Where you pay |
|---|---|---|
| Netlify (frontend) | 100GB bandwidth, unlimited sites | Never, for indie |
| Fly.io (backend) | 3 VMs, 256MB each, 100GB egress | Never, for indie |
| Neon (database) | 0.5GB storage, 100 hrs compute | Never, for indie |
| Clerk (auth) | 10,000 monthly active users | $25/mo after 10k MAU |
| Plausible (analytics) | Self-host free, or $9/mo hosted | Optional |
| Sentry (errors) | 5,000 events/mo | $26/mo after 5k events |
| Stripe (payments) | Pay per transaction (2.9% + 30¢) | Only when you earn |
| **TOTAL** | **$0** until you get paying users | Scales with success |

## License

MIT — see [LICENSE](./LICENSE).
