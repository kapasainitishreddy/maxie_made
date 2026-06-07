export const SECURITY_MARKDOWN = `# Security — PharmaIP Radar

We take security seriously. Here's how we protect your data.

## Infrastructure

- **Hosting**: Vercel (frontend) + Fly.io (backend) + Neon (database)
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Backups**: Daily encrypted snapshots, 30-day retention, tested quarterly
- **Regions**: US-East (primary), EU-West available for Enterprise tier
- **Uptime**: 99.9% target for Enterprise tier

## Authentication

- Clerk-managed authentication (OAuth 2.0, passwordless, MFA)
- Password requirements: 12+ chars, complexity rules, breached-password check
- Session timeout: 30 days for "Remember me", 24 hours otherwise
- MFA available via TOTP and WebAuthn
- API keys: scoped, rotatable, revocable

## Application Security

- **Input validation**: All API inputs validated with Pydantic schemas
- **SQL injection**: Parameterized queries via SQLAlchemy ORM (no string concatenation)
- **XSS prevention**: Content-Security-Policy header, React auto-escaping, no \`dangerouslySetInnerHTML\`
- **CSRF**: SameSite cookies, CSRF tokens on state-changing requests
- **CORS**: Restricted to whitelisted origins
- **Rate limiting**: 60 requests/min per IP per endpoint
- **Secrets**: All secrets via environment variables, never in code

## Data Handling

- **Your patent data**: Encrypted at rest, isolated per-organization
- **AI/LLM processing**: Zero data retention agreement with Anthropic and OpenAI
- **Backups**: Encrypted, isolated, tested monthly
- **Deletion**: Account deletion purges all data within 30 days
- **Audit logs**: All API access logged, 90-day retention

## Compliance

- **GDPR**: Compliant. DPA available on request. EU data residency option for Enterprise.
- **CCPA**: Compliant. California residents have all GDPR-equivalent rights.
- **SOC 2 Type II**: In progress (expected Q3 2026). Type I report available now.
- **HIPAA**: Not currently supported. We are not a Business Associate.
- **PCI DSS**: Not applicable (we use Stripe for payments, never see card data).

## Vulnerability Disclosure

We run a responsible disclosure program. If you find a security vulnerability:

- Email: **security@pharmaip-radar.com** (PGP key available on request)
- We will acknowledge within 24 hours
- We will provide a triage assessment within 72 hours
- We aim to fix critical vulnerabilities within 7 days, high within 30 days
- We credit researchers in our Hall of Fame (with permission)
- No legal action against good-faith researchers

## What You Can Do

- Enable MFA on your account (Settings → Security)
- Use a password manager; don't reuse passwords
- Rotate API keys quarterly
- Review active sessions and revoke unused ones
- Use SSO (Enterprise tier) for centralized access control
- Set up billing alerts for unusual activity

## Audits & Testing

- **Internal**: Daily SAST (Bandit), weekly dependency audit (pip-audit)
- **External**: Annual penetration test
- **Bug bounty**: Coming Q4 2026 (private program first, public after)

## Report a Security Issue

**Do not** report security issues via GitHub issues, public Slack, or social media.

Email: **security@pharmaip-radar.com** with:
- Description of the issue
- Steps to reproduce
- Potential impact
- Your name/handle (for credit)

We respond within 24 hours, fix per SLA above, and publicly disclose (with your permission) once remediated.

## Subprocessor Security

All subprocessors are required to maintain SOC 2 Type II or equivalent certification. We audit their security posture annually.

| Subprocessor | Certification | Data scope |
|---|---|---|
| Vercel | SOC 2 Type II | Frontend assets, logs |
| Fly.io | SOC 2 Type II | Backend compute |
| Neon | SOC 2 Type II | Database |
| Clerk | SOC 2 Type II | Auth data |
| Stripe | PCI DSS Level 1 | Payment metadata |
| Resend | SOC 2 Type II | Email delivery |
| Sentry | SOC 2 Type II | Error data |
| Anthropic | SOC 2 Type II | Claim analysis (zero retention) |

## Contact

- Security team: security@pharmaip-radar.com
- CISO: ciso@pharmaip-radar.com
- Status page: status.pharmaip-radar.com`;
