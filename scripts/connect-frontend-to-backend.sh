#!/usr/bin/env bash
# connect-frontend-to-backend.sh - Update Netlify env vars to point to live Fly.io backends
# Usage: ./scripts/connect-frontend-to-backend.sh
#
# This is run AFTER you've deployed the backends to Fly.io.
# It updates NEXT_PUBLIC_API_URL on all 4 Netlify sites and triggers a redeploy.

set -e

log()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m✓ $*\033[0m"; }
err()  { echo -e "\033[1;31m✗ $*\033[0m" >&2; }

APPS=(
  "pharmaip-radar:pharmaip-radar:https://pharmaip-radar-api.fly.dev"
  "cloudfinops-copilot:cloudfinops-copilot:https://cloudfinops-copilot-api.fly.dev"
  "autohedge-pro:autohedge-pro:https://autohedge-pro-api.fly.dev"
  "quantalab:quantalab:https://quantalab-api.fly.dev"
)

log "🔗 Connect Frontends to Backends"
log ""
log "This will update NEXT_PUBLIC_API_URL on all 4 Netlify sites and trigger a redeploy."
log ""

read -rp "Have you already deployed the backends to Fly.io? (y/n) " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
  err "Deploy backends first: ./scripts/deploy-fly.sh"
  exit 1
fi

read -rp "Are the URLs above correct? (y/n) " CONFIRM2
if [[ "$CONFIRM2" != "y" ]]; then
  err "Edit this script to set the correct URLs"
  exit 1
fi

command -v netlify >/dev/null 2>&1 || { err "netlify CLI not installed"; exit 1; }

for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name netlify_name api_url <<< "$entry"
  web_dir="$app_name/apps/web"

  log ""
  log "━━━ $app_name ━━━"

  if [[ ! -d "$web_dir" ]]; then
    err "Missing: $web_dir"
    continue
  fi

  cd "$web_dir"

  # Check linked
  if [[ ! -f ".netlify/state.json" ]]; then
    err "$web_dir is not linked to a Netlify site. Run: cd $web_dir && netlify link"
    cd - >/dev/null
    continue
  fi

  # Set env var
  netlify env:set NEXT_PUBLIC_API_URL "$api_url" 2>&1 | tail -1
  ok "Set NEXT_PUBLIC_API_URL=$api_url"

  # Trigger redeploy
  log "Triggering redeploy..."
  netlify deploy --prod 2>&1 | tail -3
  ok "Redeployed"

  cd - >/dev/null
done

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🎉 All 4 frontends now point to live backends"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "Test each app:"
for entry in "${APPS[@]}"; do
  IFS=':' read -r app_name netlify_name _ <<< "$entry"
  log "  https://${netlify_name}.netlify.app"
done
