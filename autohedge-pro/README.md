# AutoHedge Pro

Personal hedge fund in a terminal. 12-strategy swarm. Paper + live. 0.5% AUM.

## Quick start
```bash
# Backend (port 8002)
cd apps/api && uv sync --all-extras && uv run pytest && uv run uvicorn app.main:app --reload --port 8002
# Frontend (port 3002)
cd apps/web && pnpm install && pnpm dev
```

## Features
- 12 trading strategies (SMA, RSI, momentum, vol breakout, pairs, statarb, trend, breakout, funding arb, options spread, delta-neutral, buy & hold)
- Real metrics: Sharpe, Sortino, Calmar, max drawdown
- Walk-forward backtester with slippage + commission
- Paper trading engine with P&L tracking
- 33 passing pytest tests
- 3D hero with animated equity curve

## Architecture
- 30+ backend files (FastAPI + SQLAlchemy + Pydantic v2)
- 14+ frontend files (Next.js 15 + Tailwind + framer-motion)
