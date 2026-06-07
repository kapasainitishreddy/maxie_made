export const SECURITY_MARKDOWN = `# Security — CloudFinOps Co-Pilot

We take security seriously. Here's how we protect your data and infrastructure.

## Infrastructure

- **Hosting**: Vercel (frontend) + Fly.io (backend) + Neon (database)
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Backups**: Daily encrypted snapshots, 30-day retention
- **Uptime**: 99.9% target

## Authentication

- Clerk-managed authentication (OAuth 2.0, MFA)
- Session timeout: 30 days for "Remember me", 24 hours otherwise
- API keys: scoped, rotatable, revocable

## Cloud Account Access (Critical)

We require **read-only IAM access** to your cloud account. This is enforced by your cloud provider:

- **AWS**: IAM role with \`ReadOnlyAccess\` managed policy + Cost & Usage Reports (CUR) access
- **GCP**: \`roles/viewer\` + BigQuery access to billing export
- **Azure**: \`Reader\` role + Cost Management Reader

We **never** request, accept, or use write-level access. If you accidentally grant write access, we will:
1. Refuse to use it
2. Notify you immediately
3. Recommend you revoke the elevated role

## Application Security

- **Input validation**: All API inputs validated with Pydantic schemas
- **SQL injection**: Parameterized queries via SQLAlchemy ORM
- **XSS prevention**: CSP header, React auto-escaping
- **CSRF**: SameSite cookies, CSRF tokens
- **CORS**: Restricted to whitelisted origins
- **Rate limiting**: 60 requests/min per IP per endpoint
- **Secrets**: Environment variables, never in code

## Terraform Security

- Every Terraform change is **version-controlled** in our audit log
- Every change requires **your explicit approval** (Slack button, GitHub PR review, or dashboard click)
- Every change is **reversible** in 1 click
- We never run \`terraform apply\` without your prior approval
- All Terraform is **idempotent** — safe to re-run
- We never store Terraform state (you manage your own state)

## Audit Trail

- Every API call to your cloud account is logged
- Every recommendation is logged with rationale and evidence
- Every approval/rejection is logged with user ID and timestamp
- Audit logs retained for 7 years (SOX-compliant)
- Audit logs exportable as JSON/CSV

## Compliance

- **GDPR**: Compliant. DPA available on request.
- **SOC 2 Type II**: In progress (Q3 2026)
- **CCPA**: Compliant
- **HIPAA**: Not supported
- **PCI DSS**: Not applicable (Stripe handles payments)

## Vulnerability Disclosure

Email: **security@cloudfinops-copilot.com**

- We acknowledge within 24 hours
- Triage within 72 hours
- Critical fixes within 7 days
- No legal action against good-faith researchers

## What You Can Do

- Use a dedicated IAM role per environment (dev/staging/prod)
- Rotate the IAM role's external ID quarterly
- Review audit logs monthly
- Set up Slack alerts for approval requests
- Enable MFA on your CloudFinOps account

## Audits & Testing

- **Internal**: Daily SAST, weekly dependency audit
- **External**: Annual penetration test
- **Bug bounty**: Coming Q4 2026

## Contact

- Security team: security@cloudfinops-copilot.com
- CISO: ciso@cloudfinops-copilot.com
- Status page: status.cloudfinops-copilot.com`;
