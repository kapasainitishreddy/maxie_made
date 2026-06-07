#!/usr/bin/env bash
# deploy-netlify.sh - Deploy all 4 SaaS apps to Netlify from this monorepo
# Usage: ./scripts/deploy-netlify.sh [--dry-run]
#
# Prerequisites:
#   - netlify CLI installed: npm install -g netlify-cli
#   - netlify logged in: netlify login
#   - Each app's API deployed to Fly.io (or wherever)
#   - Clerk keys ready (optional, dev bypass works without)
#
# This script is IDEMPOTENT: re-running it updates existing sites.

set -euo pipefail

# --- Config ---
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🧪 DRY RUN mode — no changes will be made"
fi

APPS=(
  "pharmaip-radar:pharmaip-radar:https://pharmaip-radar.fly.dev"
  "cloudfinops-copilot:cloudfinops-copilot:https://cloudfinops-copilot.fly.dev"
  "autohedge-pro:autohedge-pro:https://autohedge-pro.fly.dev"
  "quantalab:quantalab:https://quantalab.fly.dev"
)

# --- Helpers ---
log()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m✓ $*\033[0m"; }
warn() { echo -e "\033[1;33m⚠ $*\033[0m"; }
err()  { echo -e "\033[1;31m✗ $*\033[0m" >&2; }

# --- Preflight ---
log "🔍 Preflight checks..."

command -v netlify >/dev/null 2>&1 || { err "netlify CLI not installed. Run: npm install -g netlify-cli"; exit 1; }
command -v gh      >/dev/null 2>&1 || { warn "gh CLI not found (optional, for repo info)"; }
command -v node    >/dev/null 2>&1 || { err "node not installed"; exit 1; }

NETLIFY_USER=$(netlify status 2>/dev/null | grep -E "Email" | awk '{print $2}' || echo "unknown")
if [[ "$NETLIFY_USER" == "unknown" || -z "$NETLIFY_USER" ]]; then
  err "Not logged in to Netlify. Run: netlify login"
  exit 1
fi
ok "Logged in to Netlify as: $NETLIFY_USER"

# --- Prompt for env vars (if not set) ---
get_or_prompt() {
  local var_name="$1"
  local prompt="$2"
  local current_value="${!var_name:-}"
  if [[ -z "$current_value" ]]; then
    read -rp "$prompt: " current_value
  fi
  echo "$current_value"
}

log "🔑 Environment variables (press Enter to use existing env or skip)..."

# Optional - these have dev-bypass fallbacks
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY:-}
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=${NEXT_PUBLIC_PLAUSIBLE_DOMAIN:-}
SENTRY_DSN=${SENTRY_DSN:-}

if [[ -z "$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" ]]; then
  warn "No NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY set. Dev bypass mode will be used (no auth)."
fi
if [[ -z "$NEXT_PUBLIC_PLAUSIBLE_DOMAIN" ]]; then
  warn "No NEXT_PUBLIC_PLAUSIBLE_DOMAIN set. Analytics will be disabled."
fi

# --- Deploy each app ---
log "🚀 Deploying 4 apps to Netlify..."

for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name netlify_name api_url <<< "$entry"
  netlify_dir="$app_name/apps/web"
  netlify_subdomain="${netlify_name}.netlify.app"

  log ""
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  log "📦 Deploying: $app_name"
  log "   Site name: $netlify_name"
  log "   URL: https://$netlify_subdomain"
  log "   API URL:  $api_url"
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [[ ! -d "$netlify_dir" ]]; then
    err "Directory not found: $netlify_dir"
    continue
  fi

  cd "$netlify_dir"

  # Check if site already linked
  if [[ -f ".netlify/state.json" ]]; then
    SITE_ID=$(netlify status 2>/dev/null | grep -E "Site ID" | awk '{print $3}' || echo "")
    if [[ -n "$SITE_ID" ]]; then
      ok "Site already linked: $SITE_ID"
    fi
  else
    # Create or link the site
    if $DRY_RUN; then
      echo "[dry-run] netlify sites:create --name $netlify_name"
    else
      log "Creating new site: $netlify_name"
      # Use --yes to skip interactive prompts
      netlify sites:create --name "$netlify_name" --with-ci || {
        warn "Site may already exist. Trying to link by name..."
        netlify link --name "$netlify_name" || {
          err "Could not create or link $netlify_name"
          cd - >/dev/null
          continue
        }
      }
    fi
  fi

  # Set environment variables
  log "Setting environment variables..."
  declare -A ENV_VARS=(
    ["NEXT_PUBLIC_API_URL"]="$api_url"
    ["NEXT_PUBLIC_APP_NAME"]="$app_name"
  )
  [[ -n "$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" ]] && ENV_VARS["NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"]="$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"
  [[ -n "$NEXT_PUBLIC_PLAUSIBLE_DOMAIN" ]]      && ENV_VARS["NEXT_PUBLIC_PLAUSIBLE_DOMAIN"]="$NEXT_PUBLIC_PLAUSIBLE_DOMAIN"
  [[ -n "$SENTRY_DSN" ]]                          && ENV_VARS["SENTRY_DSN"]="$SENTRY_DSN"

  for key in "${!ENV_VARS[@]}"; do
    value="${ENV_VARS[$key]}"
    if $DRY_RUN; then
      echo "[dry-run] netlify env:set $key $value"
    else
      netlify env:set "$key" "$value" 2>&1 | tail -1 || warn "Failed to set $key"
    fi
  done

  # Deploy
  if $DRY_RUN; then
    echo "[dry-run] netlify deploy --prod"
  else
    log "Deploying to production..."
    # Clean stale .netlify build cache (fixes EEXIST symlink errors)
    rm -rf .netlify .next/cache 2>/dev/null || true
    netlify deploy --prod --dir=.next 2>&1 | tail -10 || {
      err "Deploy failed for $app_name"
      cd - >/dev/null
      continue
    }
    ok "Deployed: https://$netlify_subdomain"
  fi

  cd - >/dev/null
done

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🎉 All 4 apps deployed (or dry-run complete)"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "📋 Summary:"
for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name netlify_subdomain _ <<< "$entry"
  log "   • $app_name → https://$netlify_subdomain"
done
log ""
log "Next steps:"
log "  1. Add custom domains in Netlify dashboard (optional)"
log "  2. Set up Clerk for real auth (or keep dev bypass)"
log "  3. Configure Plausible analytics (or leave disabled)"
log "  4. Add Sentry for error tracking (or leave disabled)"
