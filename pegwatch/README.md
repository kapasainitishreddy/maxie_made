# PegWatch — Stablecoin Depeg Early-Warning

Real-time stablecoin peg monitor with statistical depeg early-warning, multi-source pricing (Curve + Uniswap + CEX), and Telegram/Discord/webhook alerts. Built so you hear about USDC at $0.9982 *before* it hits $0.99.

> **Why it exists:** USDC depegged to $0.87 in March 2023. FRAX, UST, and others have collapsed without warning. Existing tools show you what already happened. PegWatch tells you it's *about to* happen — based on z-score, liquidity depth, and treasury attestation velocity.

---

## Stack (all free / $0 to run)

| Layer | Tech | Cost |
|---|---|---|
| Backend | FastAPI 0.115 + SQLAlchemy 2.0 async + Pydantic v2 + uv | $0 |
| Frontend | Next.js 15 + React 19 + Tailwind 3 + Framer Motion + Clerk | $0 |
| DB | SQLite (dev) / Neon Postgres (prod) | $0 |
| Auth | Clerk (10k MAU free) | $0 |
| Billing | Stripe (no monthly fee) | per-transaction |
| AI | Ollama (local LLM) for incident report summaries | $0 |
| Data | Curve.fi public API + The Graph (Uniswap) + CCXT (CEX) | $0 |
| Deploy | Vercel + Fly.io free tier | $0 |
| Tests | pytest + bandit + pip-audit | $0 |

---

## Quick start

```bash
# Backend
cd apps/api
uv sync --all-extras
uv run uvicorn app.main:app --port 8004

# Frontend
cd apps/web
pnpm install
pnpm dev
```

Then open http://localhost:3004

---

## What it does (and why it helps)

**The problem:** Stablecoins are supposed to be $1.00. When they break, your treasury, payroll, or DeFi position can lose 5-15% in minutes. By the time CoinDesk writes the headline, the depeg is over.

**What PegWatch does:**
- 📊 **Real-time peg tracking** across Curve, Uniswap, and 5+ CEXs — aggregated median
- 🔔 **Statistical early-warning** — z-score of deviation vs 7-day rolling mean. Alert when |z| > 2.0
- 💧 **Liquidity depth scan** — if exit depth at ±0.5% is < $10M, danger
- 🏛️ **Treasury velocity** — tracks Circle/Tether attestation publication cadence
- 🤖 **AI incident summary** — Ollama (local) generates a plain-English incident report
- 📲 **Alerts** — Telegram, Discord, webhook, email

**Why people pay for this:**
- **Treasury teams** hold millions in stables. A 1% depeg on $5M = $50k gone in 4 minutes.
- **Market makers** need to widen spreads before the crowd notices.
- **DEX LPs** can exit pools before the bank run.
- **Exchanges** can pause trading pairs before arbitrage breaks them.

**Pricing:** Free (3 stables, no alerts) / Pro $19/mo (20+ stables, alerts) / API $99/mo.

---

## Architecture

```
apps/api/   FastAPI backend
apps/web/   Next.js 15 frontend
.github/    CI/CD
scripts/    smoke + security audit
```

See `apps/api/README.md` and `apps/web/README.md` for per-app docs.

---

## License

MIT. See LICENSE.
