# QuantaLab

Quant research IDE. Notebooks, NL→code, backtests, marketplace.

## Quick start
```bash
# Backend (port 8003)
cd apps/api && uv sync --all-extras && uv run pytest && uv run uvicorn app.main:app --reload --port 8003
# Frontend (port 3003)
cd apps/web && pnpm install && pnpm dev
```

## Features
- NL→Python code translator via local Ollama
- Restricted Python sandbox (AST validation + banned names)
- Backtester with sharpe/sortino/max-DD
- 5 sample strategies in marketplace
- 17 passing pytest tests
- 3D hero with floating code cells + parallax

## Architecture
- 18+ backend files (FastAPI + Pydantic v2)
- 14+ frontend files (Next.js 15 + Tailwind + framer-motion)
