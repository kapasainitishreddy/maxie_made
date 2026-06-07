# Deployment & Setup Scripts

Helper scripts for deploying the 4 SaaS apps to production.

## Quick start (full deployment in 5 steps)

```bash
# Step 1: Install CLIs (one time)
npm install -g netlify-cli
curl -L https://fly.io/install.sh | sh  # or use winget on Windows

# Step 2: Authenticate
netlify login
fly auth signup

# Step 3: Set up free services
./scripts/setup-neon.sh      # free Postgres
./scripts/setup-clerk.sh     # free auth (10k MAU)

# Step 4: Deploy
./scripts/deploy-fly.sh      # 4 backends to Fly.io
./scripts/deploy-netlify.sh  # 4 frontends to Netlify
./scripts/connect-frontend-to-backend.sh  # wire them together
```

## Windows (PowerShell equivalents)

```powershell
.\scripts\setup-neon.ps1
.\scripts\setup-clerk.ps1
.\scripts\deploy-fly.ps1
.\scripts\deploy-netlify.ps1
.\scripts\connect-frontend-to-backend.ps1
```

## All scripts

| Script | Windows | What it does |
|---|---|---|
| `deploy-netlify.sh` | `deploy-netlify.ps1` | Deploy all 4 frontends to Netlify |
| `deploy-fly.sh` | `deploy-fly.ps1` | Deploy all 4 backends to Fly.io |
| `connect-frontend-to-backend.sh` | `connect-frontend-to-backend.ps1` | Update Netlify env vars to point to Fly backends |
| `setup-clerk.sh` | `setup-clerk.ps1` | Write Clerk keys to all 4 apps' .env files |
| `setup-neon.sh` | `setup-neon.ps1` | Write Neon connection string to all 4 backends |
| `netlify-help.sh` | `netlify-help.bat` | Common Netlify CLI commands |
| `fly-help.sh` | `fly-help.bat` | Common Fly.io CLI commands |

## Setup guides

- `clerk-setup.md` — Step-by-step Clerk setup
- `neon-setup.md` — Step-by-step Neon Postgres setup

## Dry-run mode

Both deploy scripts support `--dry-run` (bash) or `-DryRun` (PowerShell) to preview changes without making them:

```bash
./scripts/deploy-fly.sh --dry-run
./scripts/deploy-netlify.sh --dry-run
```

## Common workflow

```bash
# 1. Make a code change
# 2. Test locally
cd pharmaip-radar/apps/api && uv run pytest
cd pharmaip-radar/apps/web && pnpm dev

# 3. Commit + push (auto-deploys to Netlify if connected to GitHub)
git add . && git commit -m "feat: new feature"
git push origin main

# 4. For backend changes, redeploy to Fly
cd pharmaip-radar/apps/api && fly deploy

# 5. View logs if something breaks
fly logs
netlify logs
```

## Custom domain setup

After deployment, add a custom domain:

**On Netlify** (frontend):
```bash
cd pharmaip-radar/apps/web
netlify domains:add pharmaip.com
```

**On Fly.io** (backend):
```bash
cd pharmaip-radar/apps/api
fly certs create api.pharmaip.com
```

Then in your DNS provider, point:
- `pharmaip.com` → Netlify (CNAME or A records they give you)
- `api.pharmaip.com` → Fly.io (A or AAAA records they give you)

Free vs paid domains:
- **Free**: `app.netlify.app` subdomain (no custom domain)
- **~$10/yr**: `.com` from Cloudflare Registrar or Porkbun
- **~$15/yr**: `.app` TLD (good for SaaS feel)
- **~$30-50/yr**: `.io` (good for dev tools)
