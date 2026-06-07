export const PRIVACY_MARKDOWN = `# Privacy Policy — CloudFinOps Co-Pilot

**Last updated:** 2026-06-06
**Effective date:** 2026-06-06

CloudFinOps Co-Pilot ("we", "us", or "our") operates the SaaS platform at cloudfinops-copilot.com. This page informs you of our policies regarding the collection, use, and disclosure of personal data.

## 1. Information We Collect

### Account data (you provide)
- Email address (via Clerk authentication)
- Name and profile picture
- Organization name and billing details
- Cloud provider account identifiers (AWS account ID, GCP project ID, Azure subscription ID)

### Usage data (automatic)
- IP address, browser type, device type
- Pages visited, features used, recommendations reviewed
- API call patterns to cloud providers (we never see your data plane, only metadata)

### Customer data (you upload)
- Cloud cost & usage reports (read-only IAM)
- Terraform plans we generate
- Approval decisions and audit logs

**We only access your cloud account with read-only IAM roles. We never modify your infrastructure without explicit approval via Terraform PR.**

## 2. How We Use Your Data

- To provide and maintain the Service
- To analyze cloud cost patterns and generate savings recommendations
- To send transactional emails (account, billing, recommendations, alerts)
- To improve the Service (aggregated, anonymized analytics)
- To respond to support requests
- **We never sell your data. We never train AI models on your cloud infrastructure data.**

## 3. AI/ML Disclosure

We use Anthropic Claude and OpenAI GPT-4 to analyze cost data and generate recommendations. Your cost & usage data is sent to these providers under enterprise data processing agreements (zero data retention). Providers do not train on your inputs.

Local Ollama models (when configured) run entirely on your infrastructure.

## 4. Data Storage & Security

- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Stored in PostgreSQL (Neon.tech / AWS RDS)
- Daily encrypted backups, 30-day retention
- SOC2 Type II controls in progress (expected Q3 2026)

## 5. Your Rights (GDPR / CCPA)

You have the right to access, rectify, erase, port, object, and restrict processing of your data. Email privacy@cloudfinops-copilot.com to exercise any right. We respond within 30 days.

## 6. Cookies & Tracking

We use only first-party, privacy-respecting analytics (Plausible). No third-party ad cookies.

## 7. Subprocessors

| Provider | Purpose | Data shared |
|---|---|---|
| Clerk | Authentication | Email, name, OAuth profile |
| Stripe | Payments | Email, billing address |
| Neon / AWS RDS | Database | All customer data (encrypted) |
| Resend | Transactional email | Email address |
| Sentry | Error monitoring | Stack traces, user ID (no PII) |
| Anthropic / OpenAI | AI inference | Anonymized cost data (zero retention) |
| AWS / GCP / Azure | Read-only IAM | Metadata only (no data plane access) |

## 8. International Transfers

If you are in the EU/UK, your data may be transferred to the US under Standard Contractual Clauses (SCCs).

## 9. Changes to This Policy

We will notify you by email at least 30 days before any material change.

## 10. Contact

- Email: privacy@cloudfinops-copilot.com
- DPO: dpo@cloudfinops-copilot.com
- Address: [Your registered business address]`;
