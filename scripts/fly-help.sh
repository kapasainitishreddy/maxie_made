#!/usr/bin/env bash
# Common Fly.io CLI commands. Run from an app's apps/api directory.
# Usage: fly-help.sh

print_section() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_section "🚀 First-time setup"
cat <<'EOF'
# 1. Install fly CLI: https://fly.io/docs/hands-on/install-flyctl/
# 2. Sign up (uses GitHub)
fly auth signup

# 3. Per app:
cd pharmaip-radar/apps/api
fly launch --name pharmaip-radar-api   # creates app, generates fly.toml
# Choose: no Postgres (we use Neon), no Redis

# 4. Set secrets
fly secrets set DATABASE_URL=postgresql+asyncpg://...
fly secrets set CLERK_JWKS_URL=https://...

# 5. Deploy
fly deploy
EOF

print_section "🔄 Deploy updates"
cat <<'EOF'
# Deploy latest code
fly deploy

# View live logs
fly logs

# SSH into the running container
fly ssh console

# Check status
fly status

# List all your apps
fly apps list
EOF

print_section "🔐 Secrets management"
cat <<'EOF'
# List all secrets (values hidden)
fly secrets list

# Set a secret
fly secrets set KEY=value

# Set multiple secrets
fly secrets set KEY1=val1 KEY2=val2

# Unset (delete) a secret
fly secrets unset KEY
EOF

print_section "🌐 Custom domains"
cat <<'EOF'
# Add a custom domain
fly certs create yourdomain.com

# List certificates
fly certs list

# View DNS setup instructions
fly certs show yourdomain.com
EOF

print_section "📊 Monitoring + scaling"
cat <<'EOF'
# Real-time metrics
fly dashboard

# Scale up (free tier max is 1 shared-cpu-1x, 256mb)
fly scale vm shared-cpu-1x --memory 256

# Force stop (machine will auto-start on next request)
fly machines stop

# View machines
fly machines list
EOF

print_section "💾 Persistent storage (for SQLite fallback)"
cat <<'EOF'
# Create a volume (1GB free)
fly volumes create data --size 1

# Mount it in fly.toml under [mounts]
# [[mounts]]
#   source = "data"
#   destination = "/data"
# Then use /data/app.db in DATABASE_URL
EOF

print_section "🔧 Troubleshooting"
cat <<'EOF'
# View build logs
fly logs --build-only

# Restart all machines
fly machines restart

# Roll back to a previous deploy
fly releases list
fly releases rollback <version>

# Check health
fly doctor
EOF
