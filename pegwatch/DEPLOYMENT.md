# Deployment guide

PegWatch is designed to deploy to **Vercel** (frontend) + **Fly.io** (backend), both free tiers.

## Backend → Fly.io

```bash
cd apps/api

# One-time: install flyctl and sign up
# https://fly.io/docs/hands-on/install-flyctl/

fly launch --name pegwatch-api --region sjc --no-deploy
fly secrets set \
  CLERK_SECRET_KEY=*** \
  STRIPE_SECRET_KEY=sk_*** \
  STRIPE_WEBHOOK_SECRET=whsec_*** \
  STRIPE_PRICE_PRO=price_*** \
  STRIPE_PRICE_API=price_*** \
  SECRET_KEY=$(openssl rand -hex 32) \
  ALLOWED_ORIGINS=https://pegwatch.dev,https://www.pegwatch.dev \
  ENVIRONMENT=production \
  ALLOW_DEV_AUTH=false
fly deploy
```

After deploy: `https://pegwatch-api.fly.dev`

## Frontend → Vercel

```bash
cd apps/web
vercel --prod
```

Set these env vars in Vercel:
- `NEXT_PUBLIC_API_URL` = `https://pegwatch-api.fly.dev`
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (if using Clerk)
- `CLERK_SECRET_KEY` (server-side)

## Database → Neon Postgres (free)

1. Sign up at https://neon.tech
2. Create a project
3. Copy the connection string
4. Set `DATABASE_URL=postgresql+asyncpg://...` on Fly.io:

```bash
fly secrets set DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.us-east-2.aws.neon.tech/pegwatch
```

Then update `app/models/*.py` to swap `String(36)` UUID → `UUID(as_uuid=True)` for full Postgres-native UUIDs (optional — String works in both).

## One-time: Stripe webhook

In Stripe dashboard → Webhooks → Add endpoint:
- URL: `https://pegwatch-api.fly.dev/api/v1/webhooks/stripe`
- Events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
- Copy signing secret → set as `STRIPE_WEBHOOK_SECRET`

## One-time: Clerk

In Clerk dashboard → create application, copy keys to env vars on both Vercel and Fly.io.

## Custom domain

Vercel dashboard → Add domain `pegwatch.dev`. Point your DNS `CNAME` to `cname.vercel-dns.com`.
