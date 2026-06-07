# Deployment Scripts

Helper scripts for deploying the 4 SaaS apps to Netlify and managing them.

## Quick start

```bash
# 1. Install Netlify CLI (one time)
npm install -g netlify-cli

# 2. Log in (opens browser)
netlify login

# 3. Deploy all 4 apps at once
./scripts/deploy-netlify.sh
```

## Windows (PowerShell)

```powershell
.\scripts\deploy-netlify.ps1
```

## Dry run (test without deploying)

```bash
./scripts/deploy-netlify.sh --dry-run
```

```powershell
.\scripts\deploy-netlify.ps1 -DryRun
```

## What the script does

For each of the 4 apps (pharmaip-radar, cloudfinops-copilot, autohedge-pro, quantalab):

1. Creates a new Netlify site (or links to existing one)
2. Sets environment variables (API URL, Clerk, Plausible, Sentry)
3. Triggers a production deploy

The script is **idempotent** — re-running it updates existing sites rather than creating duplicates.

## Prerequisites

| Tool | Why | Install |
|---|---|---|
| `netlify` | Netlify CLI | `npm install -g netlify-cli` |
| `node` | Required by Netlify CLI | https://nodejs.org |
| `gh` (optional) | GitHub repo info | `winget install GitHub.cli` |

## Environment variables

Set these before running the script (optional — all have dev-bypass fallbacks):

```bash
export NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_live_xxxxx"
export NEXT_PUBLIC_PLAUSIBLE_DOMAIN="pharmaip-radar.com"
export SENTRY_DSN="https://xxxxx@sentry.io/12345"
```

The script will prompt for any that aren't set.

## Common commands reference

For a quick reference of all Netlify CLI commands, run:

```bash
./scripts/netlify-help.sh           # all sections
./scripts/netlify-help.sh setup     # first-time setup only
./scripts/netlify-help.sh env       # env var commands
./scripts/netlify-help.sh troubleshoot
```

Or on Windows:

```cmd
scripts\netlify-help.bat
scripts\netlify-help.bat env
```

## After deployment

Once deployed, your 4 apps will be live at:

- `https://pharmaip-radar.netlify.app`
- `https://cloudfinops-copilot.netlify.app`
- `https://autohedge-pro.netlify.app`
- `https://quantalab.netlify.app`

Optional next steps:
1. **Custom domains**: `netlify domains:add yourdomain.com`
2. **Connect to GitHub for auto-deploy**: `netlify link` then connect in dashboard
3. **Configure Clerk** (real auth): Set `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
4. **Add Plausible analytics**: Set `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`
5. **Add Sentry error tracking**: Set `SENTRY_DSN`

## Rollback

If a deploy breaks something:

```bash
# List recent deploys
netlify deploy:list

# Roll back to a specific deploy
netlify rollback
```
