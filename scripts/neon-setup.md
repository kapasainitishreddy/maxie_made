# Neon Setup Guide

Neon is the Postgres provider for all 4 apps. Free tier gives you 0.5GB storage + 100 hours of compute per month.

## Quick Start (5 min)

### 1. Sign up at neon.tech
1. Go to https://neon.tech
2. Click "Sign Up" → use GitHub
3. Authorize the Neon GitHub app

### 2. Create a project
1. Click "Create Project"
2. Settings:
   - **Name**: `srb-prod` (or whatever you like)
   - **Region**: `US East (Ohio)` — same as Fly.io's `iad`
   - **Postgres version**: 16 (latest)
3. Click "Create Project"

### 3. Get your connection string
On the project dashboard, click "Connection Details":
- **Branch**: `main` (default)
- **Database**: `neondb` (default)
- **Role**: `neondb_owner` (default)

Copy the **pooled connection** string (looks like):
```
postgresql://neondb_owner:********@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 4. Convert to asyncpg format
The apps use `asyncpg` driver. Change `postgresql://` → `postgresql+asyncpg://`:

```bash
DATABASE_URL=postgresql+asyncpg://neondb_owner:********@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 5. Add to your .env files

**Backend** (`apps/api/.env`):
```bash
DATABASE_URL=postgresql+asyncpg://neondb_owner:********@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

That's it! The app will auto-create tables on first run.

## Auto-setup script

Instead of doing this manually for all 4 apps:

```bash
./scripts/setup-neon.sh
```

The script will:
1. Prompt for your connection string
2. Write it to all 4 backend .env files
3. Test the connection

## Run migrations

The apps auto-create tables on startup (using `Base.metadata.create_all()` in lifespan). For production, you should switch to Alembic:

```bash
cd <app>/apps/api
uv add alembic
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

## Connection pooling

Use the **pooled** connection string (has `-pooler` in the URL) for serverless/Lambda. For Fly.io (long-running), use the **direct** connection string (faster, no pooler overhead).

Both are available in the Neon dashboard.

## Branching (advanced)

Neon lets you create database branches (like git branches). Useful for:
- Dev DB that mirrors prod
- Testing schema changes safely
- Per-developer DBs

```bash
# Create a branch
neonctl branches create --name dev

# Get its connection string
neonctl connection-string dev
```

## Cost

| Tier | Storage | Compute | Price |
|---|---|---|---|
| Free | 0.5 GB | 100 hrs/mo | $0 |
| Launch | 10 GB | 300 hrs/mo | $19/mo |
| Scale | 50 GB | Unlimited | $69/mo |

For 4 apps with low traffic, free tier is plenty. You'll hit the compute limit around 100 hours of active DB time per month.

## Troubleshooting

**"SSL error"** → Make sure `?sslmode=require` is at the end of the URL

**"Connection timeout"** → Check that the region matches Fly.io's region (`us-east-2` for `iad`)

**"Too many connections"** → Use the pooled connection string (`-pooler` in URL)

**"Database does not exist"** → Create a database in Neon dashboard first, or use the default `neondb`

## Resources

- Docs: https://neon.tech/docs
- Connection strings: https://neon.tech/docs/connect/connect-from-any-app
- CLI: https://neon.tech/docs/reference/cli
- Free tier limits: https://neon.tech/pricing
