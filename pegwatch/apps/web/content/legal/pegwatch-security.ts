export const SECURITY_MARKDOWN = `# Security Disclosure

We take the security of PegWatch seriously. This page explains our security practices and how to report vulnerabilities.

## Responsible disclosure

We welcome reports from security researchers. If you believe you have found a vulnerability:

- **Email:** security@pegwatch.dev (PGP key on request)
- **Response time:** We aim to acknowledge within 48 hours
- **Triage:** Initial assessment within 5 business days
- **Fixes:** Critical issues within 7 days; high within 30 days

We commit to not pursuing legal action against researchers who:
- Make a good-faith effort to avoid privacy violations
- Only interact with accounts they own or have explicit permission to test
- Stop testing immediately if they encounter user data
- Report the issue to us before disclosing publicly

## Scope

In scope:
- pegwatch.dev and all subdomains
- The PegWatch API at api.pegwatch.dev
- The PegWatch GitHub repository

Out of scope:
- Third-party services (Clerk, Stripe, Vercel, Fly.io) — report to them directly
- Denial-of-service attacks
- Social engineering of staff or users
- Physical attacks

## Security practices

**Application security:**
- OWASP security headers (CSP, X-Frame-Options, X-Content-Type-Options, HSTS, Permissions-Policy)
- Per-IP rate limiting (60 req/min)
- Parameterized SQL queries (SQLAlchemy ORM)
- Input validation via Pydantic schemas
- CSRF protection on state-changing endpoints
- HMAC signature verification on all Stripe webhooks

**Infrastructure:**
- TLS 1.3 enforced for all data in transit
- Database encryption at rest
- Secrets stored in environment variables (never in source)
- No hardcoded credentials in code
- Principle of least privilege on database access
- Backups encrypted and tested for restoration

**Operational:**
- Dependency auditing (bandit, pip-audit, pnpm audit) on every commit
- GitHub Actions CI/CD with required status checks
- Audit logging on all admin actions
- Incident response runbook (private)

## Bug bounty

We do not currently run a paid bug bounty program. Researchers who submit valid, in-scope vulnerabilities will be:
- Credited in our Hall of Fame (with their permission)
- Sent swag (PegWatch t-shirt, sticker pack)
- Given a free Pro or API subscription

## Hall of Fame

_No researchers have reported vulnerabilities yet. Be the first!_

## Security advisories

We publish security advisories on our GitHub Security tab. Subscribe to be notified of new advisories.

## Compliance

PegWatch is not SOC 2 certified. We follow security best practices but do not yet have third-party attestation. This is on our roadmap for 2026.
`;
