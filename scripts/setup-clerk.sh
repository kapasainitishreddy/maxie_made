#!/usr/bin/env bash
# setup-clerk.sh - Configure Clerk auth for all 4 apps
# Usage: ./scripts/setup-clerk.sh
#
# This will:
# 1. Prompt for your Clerk publishable key + JWKS URL
# 2. Write them to all 4 frontend .env files
# 3. Write the secret to all 4 backend .env files
# 4. Show you a checklist of remaining steps

set -e

log()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m✓ $*\033[0m"; }
warn() { echo -e "\033[1;33m⚠ $*\033[0m"; }
err()  { echo -e "\033[1;31m✗ $*\033[0m" >&2; }

APPS=("pharmaip-radar" "cloudfinops-copilot" "autohedge-pro" "quantalab")

log "🔐 Clerk Setup for Maxie Made"
log ""
log "Get your keys from: https://dashboard.clerk.com/apps → API Keys"
log "  - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: pk_test_... or pk_live_..."
log "  - CLERK_SECRET_KEY: sk_test_... or sk_live_..."
log "  - CLERK_JWKS_URL: https://<app>.clerk.accounts.dev/.well-known/jwks.json"
log ""

# Prompt for keys
read -rp "Publishable key (pk_test_...): " PUBLISHABLE_KEY
read -rp "Secret key (sk_test_...): " SECRET_KEY
read -rp "JWKS URL: " JWKS_URL

if [[ -z "$PUBLISHABLE_KEY" || -z "$SECRET_KEY" || -z "$JWKS_URL" ]]; then
  err "All three keys are required"
  exit 1
fi

# Write to all 4 frontend .env files
for app in "${APPS[@]}"; do
  env_file="$app/apps/web/.env"
  if [[ ! -f "$env_file" ]]; then
    if [[ -f "$app/apps/web/.env.example" ]]; then
      cp "$app/apps/web/.env.example" "$env_file"
    else
      touch "$env_file"
    fi
  fi
  # Remove any existing Clerk lines
  sed -i '/^NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=/d' "$env_file"
  echo "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$PUBLISHABLE_KEY" >> "$env_file"
  ok "Updated: $env_file"
done

# Write to all 4 backend .env files
for app in "${APPS[@]}"; do
  env_file="$app/apps/api/.env"
  if [[ ! -f "$env_file" ]]; then
    if [[ -f "$app/apps/api/.env.example" ]]; then
      cp "$app/apps/api/.env.example" "$env_file"
    else
      touch "$env_file"
    fi
  fi
  sed -i '/^CLERK_SECRET_KEY=/d' "$env_file"
  sed -i '/^CLERK_JWKS_URL=/d' "$env_file"
  echo "CLERK_SECRET_KEY=$SECRET_KEY" >> "$env_file"
  echo "CLERK_JWKS_URL=$JWKS_URL" >> "$env_file"
  ok "Updated: $env_file"
done

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🎉 Clerk configured for all 4 apps"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "Next steps:"
log "  1. Restart your dev servers (cd <app> && pnpm dev / uv run uvicorn ...)"
log "  2. Visit http://localhost:3000 and test sign-in"
log "  3. For production, switch to pk_live_ / sk_live_ keys"
log "  4. Run ./scripts/deploy-fly.sh to deploy with auth enabled"
log ""
log "If you don't see the sign-in button, you may need to wrap your <ClerkProvider> in app/layout.tsx"
log "  (already done for all 4 apps — the wrapper auto-enables when keys are present)"
