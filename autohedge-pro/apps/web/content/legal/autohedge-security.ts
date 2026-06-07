export const SECURITY_MARKDOWN = `# Security — AutoHedge Pro

We take security seriously. Here's how we protect your data, credentials, and trading account.

## Infrastructure

- **Hosting**: Vercel (frontend) + Fly.io (backend) + Neon (database)
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Backups**: Daily encrypted snapshots, 30-day retention
- **Uptime**: 99.9% target

## Authentication

- Clerk-managed authentication (OAuth 2.0, MFA)
- Session timeout: 30 days for "Remember me", 24 hours otherwise
- API keys: scoped, rotatable, revocable

## Brokerage Credentials (Critical)

Brokerage API keys are **encrypted with broker-specific key rotation**:
- **Alpaca**: API key + secret encrypted at rest. We never store the secret in plaintext.
- **Interactive Brokers**: OAuth tokens, encrypted with 24-hour rotation
- **Paper trading keys** (Alpaca) are isolated from your real account

**We never have withdrawal access.** Even if our system is compromised, an attacker cannot withdraw funds from your brokerage account.

You can revoke our access at any time from your broker's dashboard. Revocation is immediate.

## Trading Controls

- **Max position size** per strategy (configurable)
- **Max daily loss** (auto-pause if exceeded)
- **Allowed symbols** (whitelist/blacklist)
- **Pre-trade approval** (optional, for live trading)
- **Kill switch** (one-click pause of all strategies)
- **Anomaly detection** (auto-pause on unusual activity)

## Application Security

- **Input validation**: All API inputs validated with Pydantic schemas
- **SQL injection**: Parameterized queries via SQLAlchemy ORM
- **XSS prevention**: CSP header, React auto-escaping
- **CSRF**: SameSite cookies, CSRF tokens
- **CORS**: Restricted to whitelisted origins
- **Rate limiting**: 60 requests/min per IP per endpoint (trading endpoints: 600/min)
- **Secrets**: Environment variables, never in code

## Data Handling

- **Trade history**: Encrypted, isolated per-account
- **Backtest results**: Encrypted, isolated per-account
- **Strategy code**: Encrypted if using cloud Ollama; never leaves your machine if using local Ollama
- **Deletion**: Account deletion purges all data within 30 days

## Compliance

- **GDPR**: Compliant. DPA available on request.
- **SOC 2 Type II**: In progress (Q3 2026)
- **CCPA**: Compliant
- **SEC**: We are NOT a registered broker-dealer. Users are responsible for their own regulatory compliance.
- **PCI DSS**: Not applicable (Stripe handles payments)

## Vulnerability Disclosure

Email: **security@autohedgepro.com**

- Acknowledge within 24 hours
- Triage within 72 hours
- Critical fixes within 7 days
- No legal action against good-faith researchers

## What You Can Do

- Enable MFA (TOTP or WebAuthn) on your account
- Use a dedicated broker API key with limited permissions
- Set up kill switch and max loss limits
- Review trade history weekly
- Rotate brokerage API keys quarterly
- Use paper trading before going live
- Use local Ollama for sensitive strategies

## Audits & Testing

- **Internal**: Daily SAST, weekly dependency audit
- **External**: Annual penetration test
- **Bug bounty**: Coming Q4 2026

## Report a Security Issue

**Do not** report security issues via GitHub issues, public Slack, or social media.

Email: **security@autohedgepro.com** with:
- Description of the issue
- Steps to reproduce
- Potential impact
- Your name/handle (for credit)

## Contact

- Security team: security@autohedgepro.com
- CISO: ciso@autohedgepro.com
- Status page: status.autohedgepro.com`;
