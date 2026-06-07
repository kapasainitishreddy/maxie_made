export const PRIVACY_MARKDOWN = `# Privacy Policy — PharmaIP Radar

**Last updated:** 2026-06-06
**Effective date:** 2026-06-06

PharmaIP Radar ("we", "us", or "our") operates the SaaS platform at pharmaip-radar.com. This page informs you of our policies regarding the collection, use, and disclosure of personal data.

## 1. Information We Collect

### Account data (you provide)
- Email address (via Clerk authentication)
- Name and profile picture (from your OAuth provider or as entered)
- Organization name and billing details
- API keys you paste (for USPTO/EPO/Google Patents integrations)

### Usage data (automatic)
- IP address, browser type, device type
- Pages visited, features used, search queries
- Timestamps and session duration

### Customer data (you upload)
- Patent claim text for infringement analysis
- Landscape configurations and watchlist alerts
- Generated reports (FTO, landscape, prior art)

## 2. How We Use Your Data

- To provide and maintain the Service
- To process patent searches, infringement analysis, and report generation
- To send transactional emails (account, billing, alerts)
- To improve the Service (aggregated, anonymized analytics)
- To respond to support requests
- **We never sell your data. We never train AI models on your patent claims or client data.**

## 3. AI/ML Disclosure

We use third-party LLMs (Anthropic Claude, OpenAI GPT-4) for claim analysis. Your patent claim text is sent to these providers under their enterprise data processing agreements (zero data retention). LLM providers do not train on your inputs.

Local Ollama models (when configured) run entirely on your infrastructure — no data leaves your environment.

## 4. Data Storage & Security

- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Stored in EU/US PostgreSQL databases (Neon.tech, AWS RDS, or self-hosted)
- Daily encrypted backups, 30-day retention
- SOC2 Type II controls in progress (expected Q3 2026)
- Access logs retained for 90 days

## 5. Your Rights (GDPR / CCPA)

You have the right to:
- **Access** — request a copy of your data
- **Rectification** — correct inaccurate data
- **Erasure** — delete your account and all data (within 30 days)
- **Portability** — export all data as JSON
- **Object** — opt out of analytics/tracking
- **Restrict processing** — pause certain processing activities

Email privacy@pharmaip-radar.com to exercise any right. We respond within 30 days.

## 6. Cookies & Tracking

We use **only first-party, privacy-respecting analytics** (Plausible). No Google Analytics, no Facebook Pixel, no third-party ad cookies. Essential session cookies are required for authentication.

## 7. Subprocessors

| Provider | Purpose | Data shared |
|---|---|---|
| Clerk | Authentication | Email, name, OAuth profile |
| Stripe | Payments | Email, billing address, last 4 of card |
| Neon / AWS RDS | Database | All customer data (encrypted) |
| Resend | Transactional email | Email address |
| Sentry | Error monitoring | Stack traces, user ID (no PII) |
| Anthropic / OpenAI | AI inference | Patent claim text (zero retention) |

## 8. Children

The Service is not intended for users under 16. We do not knowingly collect data from children.

## 9. International Transfers

If you are in the EU/UK, your data may be transferred to the US under Standard Contractual Clauses (SCCs) or to a GDPR-compliant processor (Clerk, Neon, AWS, all of which provide SCCs).

## 10. Changes to This Policy

We will notify you by email and in-product at least 30 days before any material change. Continued use after the effective date constitutes acceptance.

## 11. Contact

- Email: privacy@pharmaip-radar.com
- DPO: dpo@pharmaip-radar.com
- Address: [Your registered business address]
- EU representative: [Per GDPR Article 27 if applicable]`;
