export const SECURITY_MARKDOWN = `# Security — QuantaLab

We take security seriously. Here is how we protect your code, data, and IP.

## Infrastructure

- **Hosting**: Vercel (frontend) + Fly.io (backend) + Neon (database)
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Backups**: Daily encrypted snapshots, 30-day retention
- **Uptime**: 99.9% target

## Authentication

- Clerk-managed authentication (OAuth 2.0, MFA)
- Session timeout: 30 days for "Remember me", 24 hours otherwise

## Sandbox Security (Critical)

Your code runs in a **hardened Python sandbox**:
- **Process isolation**: Each notebook runs in a separate process with restricted syscalls (seccomp on Linux)
- **No network**: \`socket\` and network libraries are disabled at the Python level
- **No filesystem escape**: Working directory is chrooted
- **Resource limits**: 512MB RAM, 1 CPU, 5-minute execution per cell
- **Allowlisted imports**: Only \`pandas\`, \`numpy\`, \`scipy\`, \`scikit-learn\`, \`matplotlib\`, \`statsmodels\`, \`talib\`, \`arch\`, and ~50 other quantitative finance libraries
- **Wiped on exit**: Kernel state and variables are destroyed when you close the notebook

**Why this matters**: Even if your code is buggy or malicious (intentionally or not), it cannot:
- Phone home to a malicious server
- Read other users notebooks
- Exhaust server resources
- Persist between notebook sessions (unless you explicitly save)

## Code Confidentiality

- **Your strategy code is yours.** We never use it to train AI models.
- **NL→Code (default)**: Runs locally via Ollama. No data leaves your machine.
- **NL→Code (opt-in cloud)**: Sent to Ollama Cloud or Anthropic under their zero-retention agreements.
- **Backtests**: Run in the same sandbox; results stored encrypted in your account.

## Application Security

- **Input validation**: All API inputs validated with Pydantic schemas
- **SQL injection**: Parameterized queries via SQLAlchemy ORM
- **XSS prevention**: CSP header, React auto-escaping
- **CSRF**: SameSite cookies, CSRF tokens
- **CORS**: Restricted to whitelisted origins
- **Rate limiting**: 60 requests/min per IP per endpoint
- **Secrets**: Environment variables, never in code

## Data Handling

- **Notebooks**: Encrypted, isolated per-account
- **Backtest results**: Encrypted, isolated per-account
- **Marketplace listings**: Public (by your choice)
- **Deletion**: Account deletion purges all data within 30 days

## Compliance

- **GDPR**: Compliant. DPA available on request.
- **SOC 2 Type II**: In progress (Q3 2026)
- **CCPA**: Compliant
- **HIPAA**: Not supported
- **PCI DSS**: Not applicable (Stripe handles payments)

## Vulnerability Disclosure

Email: **security@quantalab.com**

- Acknowledge within 24 hours
- Triage within 72 hours
- Critical fixes within 7 days
- No legal action against good-faith researchers

## What You Can Do

- Enable MFA on your account
- Use local Ollama (not cloud) for sensitive strategies
- Do not paste API keys or credentials into notebook code
- Set notebook sharing to "private" by default
- Review your shared notebooks monthly
- Report suspicious marketplace strategies

## Audits & Testing

- **Internal**: Daily SAST, weekly dependency audit
- **External**: Annual penetration test
- **Sandbox fuzzing**: Continuous, automated
- **Bug bounty**: Coming Q4 2026

## Report a Security Issue

**Do not** report security issues via GitHub issues, public Slack, or social media.

Email: **security@quantalab.com** with:
- Description of the issue
- Steps to reproduce
- Potential impact
- Your name/handle (for credit)

## Contact

- Security team: security@quantalab.com
- CISO: ciso@quantalab.com
- Status page: status.quantalab.com`;
