#!/usr/bin/env bash
# Common Netlify CLI commands. Run from an app's apps/web directory.
# Usage: netlify-help.sh [command]
# Examples:
#   ./scripts/netlify-help.sh              # show all commands
#   ./scripts/netlify-help.sh env          # show how to set env vars
#   ./scripts/netlify-help.sh logs         # show how to view deploy logs

set -e

print_section() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_section "🚀 First-time setup (run from apps/web/)"
cat <<'EOF'
# 1. Log in to Netlify (opens browser)
netlify login

# 2. Create a new site (or link existing)
netlify sites:create --name pharmaip-radar --ci

# 3. Set environment variables
netlify env:set NEXT_PUBLIC_API_URL https://pharmaip-radar.fly.dev
netlify env:set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY pk_live_xxxxx
netlify env:set NEXT_PUBLIC_PLAUSIBLE_DOMAIN pharmaip-radar.com
netlify env:set SENTRY_DSN https://xxxxx@sentry.io/12345

# 4. Deploy to production
netlify deploy --prod

# 5. Open the site
netlify open:site
EOF

print_section "🔄 Update an existing site"
cat <<'EOF'
# Pull latest from main (triggers auto-deploy if connected to GitHub)
git push origin main

# Or deploy manually
netlify deploy --prod

# View deploy logs
netlify logs

# View recent deploys
netlify deploy:list
EOF

print_section "🔐 Environment variables"
cat <<'EOF'
# List all env vars (values hidden)
netlify env:list

# Set a var
netlify env:set KEY value

# Import from .env file
netlify env:import .env.production

# Pull to local .env
netlify env:get KEY
EOF

print_section "🌐 Custom domains"
cat <<'EOF'
# Add a custom domain
netlify domains:add yourdomain.com

# Set as primary
netlify domains:update yourdomain.com --primary

# Provision HTTPS (auto via Let's Encrypt)
netlify https:enable
EOF

print_section "📊 Monitoring"
cat <<'EOF'
# Real-time function logs
netlify logs --function=...

# Bandwidth & build minutes usage
netlify status

# Open admin dashboard
netlify open
EOF

print_section "🔧 Troubleshooting"
cat <<'EOF'
# Clear cache and rebuild
netlify build --clear-cache

# Test a build locally
netlify dev

# Check deploy status
netlify status

# Disconnect a site (keep site, remove link)
netlify unlink
EOF
