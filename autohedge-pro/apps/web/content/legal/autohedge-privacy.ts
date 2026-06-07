export const PRIVACY_MARKDOWN = `# Privacy Policy — AutoHedge Pro

**Last updated:** 2026-06-06

AutoHedge Pro ("we", "us", or "our") operates the SaaS platform at autohedgepro.com. This page informs you of our policies regarding the collection, use, and disclosure of personal data.

## 1. Information We Collect

### Account data (you provide)
- Email address (via Clerk authentication)
- Name and profile picture
- Organization name and billing details
- Brokerage account credentials (Alpaca, Interactive Brokers) — stored encrypted

### Usage data (automatic)
- IP address, browser type, device type
- Pages visited, strategies used, backtests run
- API call patterns to brokers (place orders, read positions)

### Trading data (generated)
- Paper trading history
- Live trade history (we log every order)
- Portfolio snapshots (cash, positions, P&L)
- Backtest results

**You keep custody of all assets. We place orders via your broker's API but the shares/cash are held in YOUR brokerage account, not ours.**

## 2. How We Use Your Data

- To provide and maintain the Service
- To run your trading strategies (paper or live)
- To detect market regimes and rebalance positions
- To send transactional emails (account, billing, trade confirmations, alerts)
- To improve the Service (aggregated, anonymized analytics)
- **We never sell your data. We never share your trading history with third parties.**

## 3. AI/ML Disclosure

We use statistical models (Hidden Markov Models for regime detection) and may use LLMs to generate trading signals. Your trading data is **never** sent to LLM providers for training. Local Ollama models run entirely on your infrastructure.

## 4. Data Storage & Security

- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Brokerage credentials encrypted with broker-specific key rotation
- PostgreSQL database (Neon.tech / AWS RDS)
- Daily encrypted backups, 30-day retention
- SOC2 Type II controls in progress (Q3 2026)

## 5. Your Rights (GDPR / CCPA)

You have the right to access, rectify, erase, port, object, and restrict processing. Email privacy@autohedgepro.com. We respond within 30 days.

## 6. Cookies & Tracking

First-party analytics only (Plausible). No third-party trackers.

## 7. Subprocessors

| Provider | Purpose | Data shared |
|---|---|---|
| Clerk | Authentication | Email, name |
| Stripe | Payments | Email, billing address |
| Neon / AWS RDS | Database | All customer data (encrypted) |
| Resend | Email | Email address |
| Sentry | Error monitoring | Stack traces, user ID (no PII) |
| Alpaca | Brokerage API | Order placement (no PII unless you set it) |
| Interactive Brokers | Brokerage API | Order placement (no PII unless you set it) |

## 8. International Transfers

EU/UK data may be transferred to the US under Standard Contractual Clauses.

## 9. Financial Disclaimers

**We are NOT a broker-dealer, investment advisor, or financial institution.** We are a software tool that places orders via YOUR brokerage account based on YOUR strategies.

**Past performance does not guarantee future results.** Backtests, paper trading, and even live trading can result in losses. You are solely responsible for your investment decisions.

**No fiduciary relationship.** We do not provide investment advice. Strategy descriptions, backtest results, and AI-generated signals are for informational purposes only. Consult a licensed financial advisor before trading.

## 10. Changes to This Policy

We will notify you by email at least 30 days before any material change.

## 11. Contact

- Email: privacy@autohedgepro.com
- DPO: dpo@autohedgepro.com
- Address: [Your registered business address]`;
