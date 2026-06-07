#!/usr/bin/env bash
# deploy-fly.sh - Deploy all 4 SaaS backend APIs to Fly.io from this monorepo
# Usage: ./scripts/deploy-fly.sh [--dry-run]
#
# Prerequisites:
#   - fly CLI installed: https://fly.io/docs/hands-on/install-flyctl/
#   - fly logged in: fly auth signup (uses GitHub)
#   - Optional: Neon Postgres connection string (or use SQLite)

set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🧪 DRY RUN mode"
fi

APPS=(
  "pharmaip-radar:pharmaip-radar-api:8000"
  "cloudfinops-copilot:cloudfinops-copilot-api:8000"
  "autohedge-pro:autohedge-pro-api:8000"
  "quantalab:quantalab-api:8000"
  "pegwatch:pegwatch-api:8000"
)

log()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m✓ $*\033[0m"; }
warn() { echo -e "\033[1;33m⚠ $*\033[0m"; }
err()  { echo -e "\033[1;31m✗ $*\033[0m" >&2; }

# --- Preflight ---
log "🔍 Preflight checks..."
command -v fly >/dev/null 2>&1 || { err "fly CLI not installed. Get it: https://fly.io/docs/hands-on/install-flyctl/"; exit 1; }

FLY_USER=$(fly auth whoami 2>/dev/null || echo "")
if [[ -z "$FLY_USER" ]]; then
  err "Not logged in to Fly.io. Run: fly auth signup"
  exit 1
fi
ok "Logged in to Fly.io as: $FLY_USER"

# --- Optional secrets ---
log "🔑 Database + auth secrets (press Enter to skip)..."

# Database
DATABASE_URL=${DATABASE_URL:-}
if [[ -z "$DATABASE_URL" ]]; then
  warn "No DATABASE_URL set. App will use SQLite (fine for testing, NOT for production)."
  warn "Get a free Postgres from https://neon.tech (0.5GB free)"
fi

# Clerk (optional)
CLERK_JWKS_URL=${CLERK_JWKS_URL:-}
if [[ -z "$CLERK_JWKS_URL" ]]; then
  warn "No CLERK_JWKS_URL set. Dev bypass mode will be used (no auth)."
  warn "Get free Clerk keys: https://clerk.com (10k MAU free)"
fi

# Plausible
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=${NEXT_PUBLIC_PLAUSIBLE_DOMAIN:-}

# Sentry
SENTRY_DSN=${SENTRY_DSN:-}

# --- Deploy ---
log "🚀 Deploying 5 backends to Fly.io..."

for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name fly_app_name _ <<< "$entry"
  api_dir="$app_name/apps/api"

  log ""
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  log "📦 Deploying: $app_name → $fly_app_name"
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [[ ! -d "$api_dir" ]]; then
    err "Directory not found: $api_dir"
    continue
  fi

  cd "$api_dir"

  # Check if app exists on Fly
  if fly apps list 2>/dev/null | grep -q "$fly_app_name"; then
    ok "App already exists: $fly_app_name"
  else
    if $DRY_RUN; then
      echo "[dry-run] fly apps create $fly_app_name"
    else
      log "Creating app: $fly_app_name"
      fly apps create "$fly_app_name" --org personal 2>&1 | tail -3 || {
        err "Failed to create $fly_app_name"
        cd - >/dev/null
        continue
      }
    fi
  fi

  # Set secrets
  log "Setting secrets..."
  declare -A SECRETS=()
  if [[ -n "$DATABASE_URL" ]]; then
    SECRETS["DATABASE_URL"]="$DATABASE_URL"
  fi
  if [[ -n "$CLERK_JWKS_URL" ]]; then
    SECRETS["CLERK_JWKS_URL"]="$CLERK_JWKS_URL"
  fi
  if [[ -n "$SENTRY_DSN" ]]; then
    SECRETS["SENTRY_DSN"]="$SENTRY_DSN"
  fi
  if [[ -n "$NEXT_PUBLIC_PLAUSIBLE_DOMAIN" ]]; then
    SECRETS["PLAUSIBLE_DOMAIN"]="$NEXT_PUBLIC_PLAUSIBLE_DOMAIN"
  fi
  # Always set APP_ENV
  SECRETS["APP_ENV"]="production"

  for key in "${!SECRETS[@]}"; do
    value="${SECRETS[$key]}"
    if $DRY_RUN; then
      echo "[dry-run] fly secrets set $key=***"
    else
      fly secrets set "$key=$value" 2>&1 | tail -1
    fi
  done

  # Deploy
  if $DRY_RUN; then
    echo "[dry-run] fly deploy"
  else
    log "Deploying..."
    fly deploy --remote-only 2>&1 | tail -10
    if fly status 2>&1 | grep -q "running"; then
      ok "Deployed: https://$fly_app_name.fly.dev"
    else
      err "Deploy may have failed. Check: fly logs"
    fi
  fi

  cd - >/dev/null
done

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🎉 All 5 backends deployed"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "📋 Summary:"
for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name fly_app_name _ <<< "$entry"
  log "   • $app_name → https://$fly_app_name.fly.dev"
done
log ""
log "Next: update frontend NEXT_PUBLIC_API_URL env vars to point to these URLs"
