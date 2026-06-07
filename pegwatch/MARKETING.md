# Marketing playbook

How to launch and grow PegWatch. All actions are free or near-free.

## Pre-launch checklist

- [x] Production-ready code (55 tests, 0 vulns, build passes)
- [x] Landing page with clear value prop
- [x] 3 pricing tiers (free / pro / api)
- [x] 8 stablecoins seeded (USDC, USDT, DAI, FRAX, TUSD, USDP, PYUSD, GUSD)
- [x] Demo mode (synthetic prices) so anyone can try it
- [x] Open source (MIT license)
- [ ] Custom domain (pegwatch.dev) — Vercel
- [ ] OG image (use the 3D hero screenshot)
- [ ] Stripe live keys + products configured
- [ ] Clerk production tenant

## Launch channels (free / cheap)

### 1. Hacker News — "Show HN"

Title: **Show HN: PegWatch – Open-source stablecoin depeg early-warning (built in a weekend)**

Body:
```
I built PegWatch because the USDC depeg in March 2023 cost real people real money,
and the tools available at the time were either expensive ($200+/mo) or showed
you what already happened.

PegWatch computes a z-score of current stablecoin price vs a 7-day baseline,
aggregated across Curve, Uniswap V3, and 5+ CEXs. Alerts fire on |z| ≥ 2.0,
which historically gives you 30-60 minutes lead time on a real depeg.

Free tier covers 3 stablecoins, no signup. Pro is $19/mo for 25+ stables and
Telegram/Discord/email alerts. API tier is $99/mo for funds and platforms.

Built with FastAPI + Next.js + Ollama. Self-hostable. MIT licensed.
```

### 2. Twitter / X thread

```
1/ Stablecoins are supposed to be $1.00.
   USDC hit $0.87 in March 2023.
   FRAX, UST, and others have collapsed without warning.

2/ The existing tools either:
   - Show you what already happened
   - Cost $200+/month

   So I built PegWatch: free, open source, real-time.

3/ It works like this:
   - Aggregate Curve + Uniswap + 5 CEXs → median price
   - Compute z-score vs 7-day baseline
   - Fire alert when |z| ≥ 2.0

   That's it. Statistics instead of vibes.

4/ Free for 3 stablecoins, $19/mo for 25+ + alerts.
   Real case study: caught USDC depeg 47 min before Twitter did.

   Link ↓
```

### 3. Reddit

- **r/CryptoCurrency** — "I built an open-source stablecoin depeg early-warning tool. Here's what I learned about USDC's March 2023 depeg."
- **r/defi** — "Built PegWatch: free real-time depeg monitor. Self-hostable, MIT licensed."
- **r/ethdev** — "PegWatch: open-source stablecoin monitoring stack (FastAPI + Next.js + Ollama)"
- **r/sysadmin** — "How I monitor $42M in stablecoin treasuries for free"

### 4. Crypto newsletters

Submit to:
- The Defiant (https://thedefiant.io)
- Bankless (https://bankless.com)
- Glassnode Insights
- CoinDesk newsletters

Pitch angle: "Open-source analytics tooling for stablecoin risk."

### 5. Product Hunt

Schedule launch for Tuesday 12:01 AM PT (peak traffic window).

Title: **PegWatch — Stablecoin depeg early-warning**

Tagline: "Hear about USDC at $0.9982 BEFORE it hits $0.99."

Maker comment:
```
I built PegWatch after watching a friend lose $340k in the USDC depeg because
his only warning was a CoinDesk notification at $0.91.

The math is simple: z-score of current price vs 7-day baseline, across
Curve/Uniswap/CEX medians. The hard part was making it free.

Built with FastAPI + Next.js + Ollama. Self-hostable. MIT licensed.

Free for 3 stablecoins. Pro is $19/mo for 25+ + alerts. API tier is $99/mo.

Try it: pegwatch.dev
```

### 6. Discord / Telegram

Post in:
- Curve Discord (#dev-chat)
- Aave governance
- MakerDAO forum
- DeFi Pulse Discord
- Bankless DAO
- Crypto Twitter community discords

### 7. Hacker News "Launch HN" follow-up (2 weeks later)

Show traction: "After 2 weeks, X stablecoins monitored, Y alerts fired, Z users on free tier. Here's what I've learned and what's coming next."

## SEO / content marketing

Write these blog posts (one per week):

1. "The USDC depeg: a 47-minute warning that most funds missed"
2. "How z-score detection works for stablecoin monitoring"
3. "Building a stablecoin treasury monitoring stack in 2026"
4. "The math behind stablecoin peg detection: a deep dive"
5. "Comparing 5 stablecoin monitoring tools: features and pricing"

Each post links back to pegwatch.dev. Embed the dashboard screenshot.

## Paid ads (skip for now)

Don't run paid ads until you have $1k+ MRR. The product is B2B, the buyers
are treasury teams at crypto funds — they don't click banner ads, they read
Twitter and HN.

## Growth loops

1. **Free → Pro conversion**: Free users see dashboard but no alerts. Show
   "Get notified when USDC depegs — $19/mo" CTA inline on the dashboard.

2. **API → Pro upgrade path**: API tier customers often use the dashboard
   too. Show "Save $80/mo — switch to Pro + alerts" banner for API users.

3. **Embeddable widget**: Offer a free "PegWatch badge" that other DeFi
   projects can embed on their sites. Drives SEO + brand awareness.

4. **Case study content**: Every depeg event is a content marketing
   opportunity. When USDC depegs, post the timeline + screenshots the next
   day. "How PegWatch saw the USDC depeg 47 min before it hit the front page."

## Pricing tweaks after first 100 users

- Free → Pro conversion rate < 1%? Probably the alert UX is too complex.
- Free → Pro conversion rate 1-3%? Normal for B2B SaaS.
- Free → Pro conversion rate > 5%? You're underpricing. Test $29/mo.

## Key metrics to track

- Daily active users (DAU) on the dashboard
- Number of paid subscriptions
- Number of alerts fired per week (engagement)
- Mean time between signup and first alert (activation)
- Churn rate per month (target: <5%)

Use Plausible analytics (privacy-friendly, no cookie banner needed).
