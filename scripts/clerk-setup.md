# Clerk Setup Guide

Clerk is the authentication provider for all 4 apps. It gives you login/signup flows, social auth (Google, GitHub, etc.), and user management for free up to 10,000 monthly active users.

## Quick Start (5 min)

### 1. Sign up at clerk.com
1. Go to https://clerk.com and click "Sign Up"
2. Sign up with GitHub (easiest)
3. Create a new application for **each of the 4 apps** (or 1 app with 4 paths)

### 2. Get your keys
In the Clerk dashboard, go to **API Keys** in the sidebar. You'll see:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` — starts with `pk_test_...` or `pk_live_...`
- `CLERK_SECRET_KEY` — starts with `sk_test_...` or `sk_live_...`
- `CLERK_JWKS_URL` — for backend verification, looks like `https://your-app.clerk.accounts.dev/.well-known/jwks.json`

### 3. Add to your .env files

**Frontend** (`apps/web/.env`):
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxx
```

**Backend** (`apps/api/.env`):
```bash
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
CLERK_JWKS_URL=https://your-app.clerk.accounts.dev/.well-known/jwks.json
```

### 4. (Optional) Configure sign-in methods
In Clerk dashboard → **User & Authentication** → enable:
- Email + password
- Google OAuth
- GitHub OAuth
- LinkedIn (for B2B apps)

### 5. (Optional) Customize sign-in UI
- Clerk dashboard → **Customization** → themes, logo, colors
- Set `appearance={{ baseTheme: dark }}` in your `<ClerkProvider>`

## Auto-deploy to Fly.io

Once you have your keys, the deploy scripts will pick them up automatically:

```bash
# Set once in your shell
export CLERK_JWKS_URL="https://your-app.clerk.accounts.dev/.well-known/jwks.json"

# Then run deploy scripts
./scripts/deploy-fly.sh    # backend
./scripts/deploy-netlify.sh # frontend
```

Or use the `setup-clerk.sh` script (auto-fills .env files):

```bash
./scripts/setup-clerk.sh
```

## How the dev bypass works (no Clerk needed for testing)

The apps are built to work **without** Clerk keys. When `CLERK_JWKS_URL` is empty or `APP_ENV=development`:
- Backend skips JWT verification
- Frontend hides the `<ClerkProvider>` wrapper
- All endpoints return mock user `dev-user`

This is great for local dev. When you add real Clerk keys, auth automatically activates.

## Production checklist

Before going live with Clerk:
- [ ] Switch from `pk_test_` to `pk_live_` keys
- [ ] Switch from `sk_test_` to `sk_live_` keys
- [ ] Set up custom domain in Clerk dashboard
- [ ] Configure email templates (Clerk dashboard → Emails)
- [ ] Set up MFA requirement (Clerk dashboard → Multi-factor)
- [ ] Set up SCIM provisioning (for B2B, Clerk dashboard → Enterprise)
- [ ] Add webhook endpoint to sync users to your DB (optional)

## Cost

| Tier | MAU | Price |
|---|---|---|
| Free | 10,000 | $0/mo |
| Pro | 100,000 | $25/mo |
| Enterprise | Unlimited | Custom |

For your 4 apps, you can get to 10k users per app before paying anything.

## Resources

- Docs: https://clerk.com/docs
- Next.js quickstart: https://clerk.com/docs/quickstarts/nextjs
- FastAPI JWT verification: https://clerk.com/docs/backend-requests/overview
- Discord: https://clerk.com/discord
