#!/usr/bin/env bash
# setup-neon.sh - Configure Neon Postgres for all 4 backends
# Usage: ./scripts/setup-neon.sh
#
# Get a free database from https://neon.tech (0.5GB free)

set -e

log()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m✓ $*\033[0m"; }
err()  { echo -e "\033[1;31m✗ $*\033[0m" >&2; }

APPS=("pharmaip-radar" "cloudfinops-copilot" "autohedge-pro" "quantalab")

log "🐘 Neon Setup for Maxie Made"
log ""
log "Get a free database from: https://neon.tech"
log "  1. Sign up with GitHub"
log "  2. Create a project in US East (Ohio) region"
log "  3. Copy the pooled connection string"
log "  4. Add +asyncpg to the URL: postgresql+asyncpg://..."
log ""

read -rp "Database URL (postgresql+asyncpg://...): " DATABASE_URL

if [[ -z "$DATABASE_URL" ]]; then
  err "DATABASE_URL required"
  exit 1
fi

# Validate it looks right
if [[ ! "$DATABASE_URL" =~ ^postgresql(\+asyncpg)?:// ]]; then
  err "URL must start with postgresql:// or postgresql+asyncpg://"
  exit 1
fi

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
  # Remove existing DATABASE_URL
  sed -i '/^DATABASE_URL=/d' "$env_file"
  echo "DATABASE_URL=$DATABASE_URL" >> "$env_file"
  ok "Updated: $env_file"
done

log ""
log "Testing connection..."

# Try to install psycopg2-binary in one app to test
cd "${APPS[0]}/apps/api"
if command -v uv >/dev/null; then
  uv run python -c "
import asyncio
import os
import asyncpg

async def test():
    url = os.environ.get('DATABASE_URL') or '$DATABASE_URL'
    url = url.replace('postgresql+asyncpg://', 'postgresql://')
    try:
        conn = await asyncpg.connect(url)
        v = await conn.fetchval('SELECT version()')
        print(f'✓ Connected: {v[:50]}')
        await conn.close()
    except Exception as e:
        print(f'✗ Connection failed: {e}')
        exit(1)

asyncio.run(test())
" 2>&1
fi

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "🎉 Neon configured for all 4 apps"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "Next steps:"
log "  1. Restart your backend (cd <app>/apps/api && uv run uvicorn ...)"
log "  2. Tables will auto-create on first request"
log "  3. For production, run: ./scripts/deploy-fly.sh"
log "  4. The connection string will be picked up as a Fly.io secret"
