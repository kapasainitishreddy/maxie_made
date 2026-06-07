export const PRIVACY_MARKDOWN = `# Privacy Policy — QuantaLab

**Last updated:** 2026-06-06

QuantaLab ("we", "us", or "our") operates the SaaS platform at quantalab.com. This page informs you of our policies regarding the collection, use, and disclosure of personal data.

## 1. Information We Collect

### Account data (you provide)
- Email address (via Clerk authentication)
- Name and profile picture
- Organization name and billing details
- Payment details (processed by Stripe, we never see card data)

### Usage data (automatic)
- IP address, browser type, device type
- Pages visited, notebooks created, backtests run
- API call patterns

### Customer data (you upload)
- Strategy code (Python, in sandboxed notebook kernel)
- Backtest configurations and results
- Marketplace listings (if you publish a strategy)
- Comments and shared notebooks (if you collaborate)

**Critical: Strategy code is NEVER used to train AI models. Your IP is yours.**

## 2. How We Use Your Data

- To provide and maintain the Service
- To execute your code in a sandboxed environment
- To run backtests, walk-forward validation, and Monte Carlo simulations
- To send transactional emails (account, billing, marketplace)
- To improve the Service (aggregated, anonymized analytics)
- **We never sell your data. We never train AI models on your strategy code.**

## 3. Sandbox Execution

Your code runs in a **sandboxed Python kernel**:
- No internet access (no \`requests\`, \`urllib\`, \`socket\`)
- No filesystem access outside the notebook working directory
- Memory and CPU limits enforced
- Process killed after 5 minutes
- All imports are allowlisted (pandas, numpy, scipy, scikit-learn, matplotlib, etc.)

This protects you from accidentally (or maliciously) damaging our infrastructure or other tenants.

## 4. NL→Code Disclosure

When you use the NL→Code feature, your plain-English description is sent to:
- **Local Ollama** (default, if you have it running) — no data leaves your machine
- **Cloud Ollama** (optional) — your description is sent to the Ollama Cloud under their zero-retention agreement
- **Anthropic Claude** (optional) — your description is sent to Anthropic under their enterprise zero-retention agreement

**Default is local.** Cloud is opt-in.

## 5. Data Storage & Security

- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- PostgreSQL database (Neon.tech / AWS RDS)
- Daily encrypted backups, 30-day retention
- SOC2 Type II controls in progress (Q3 2026)

## 6. Your Rights (GDPR / CCPA)

You have the right to access, rectify, erase, port, object, and restrict processing. Email privacy@quantalab.com. We respond within 30 days.

## 7. Cookies & Tracking

First-party analytics only (Plausible). No third-party trackers.

## 8. Subprocessors

| Provider | Purpose | Data shared |
|---|---|---|
| Clerk | Authentication | Email, name |
| Stripe | Payments | Email, billing address |
| Neon / AWS RDS | Database | All customer data (encrypted) |
| Resend | Email | Email address |
| Sentry | Error monitoring | Stack traces, user ID (no PII) |
| Ollama Cloud (opt-in) | NL→Code | Description text (zero retention) |
| Anthropic (opt-in) | NL→Code | Description text (zero retention) |

## 9. International Transfers

EU/UK data may be transferred to the US under Standard Contractual Clauses.

## 10. Changes to This Policy

We will notify you by email at least 30 days before any material change.

## 11. Contact

- Email: privacy@quantalab.com
- DPO: dpo@quantalab.com
- Address: [Your registered business address]`;
