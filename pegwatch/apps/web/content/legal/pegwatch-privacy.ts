export const PRIVACY_MARKDOWN = `# Privacy Policy

Last updated: January 2026

PegWatch ("we", "us", "our") operates the website pegwatch.dev and the PegWatch API. This page informs you of our policies regarding the collection, use, and disclosure of personal data.

## 1. Information we collect

**Account data:** When you sign in via Clerk, we receive your email address and a unique user ID. We do not see your password.

**Usage data:** We log every API request (timestamp, endpoint, status code) for rate limiting, abuse prevention, and analytics. Logs are retained for 30 days.

**Stablecoin data:** We collect public blockchain data (Curve pool prices, Uniswap TWAPs, CEX orderbook snapshots). This data is public and not personal.

**Alert delivery:** If you configure Telegram, Discord, email, or webhook alerts, we store the target address (chat ID, webhook URL, or email) needed to deliver alerts to you.

## 2. How we use your information

- To provide the PegWatch service (price monitoring, alerts, dashboard)
- To process subscription payments (via Stripe; we never see your card number)
- To detect and prevent abuse (rate limiting, fraud)
- To improve the product (aggregate, anonymized analytics)

## 3. What we do NOT do

- We do not sell your personal data to third parties. Ever.
- We do not run third-party advertising on PegWatch.
- We do not track you across other websites.

## 4. Third-party services

We use the following sub-processors:

- **Clerk** — authentication (see clerk.com/privacy)
- **Stripe** — payment processing (see stripe.com/privacy)
- **Vercel** — frontend hosting (see vercel.com/legal/privacy-policy)
- **Fly.io** — backend hosting (see fly.io/privacy)
- **Ollama** — local LLM (runs on our infrastructure, no data sent to third parties)

## 5. Data retention

- Account data: until you delete your account
- Usage logs: 30 days
- Stablecoin snapshots: 30 days on Free, 1 year on Pro, indefinitely on API
- Alert channels: until you delete them

## 6. Your rights

You can request export or deletion of your data at any time by emailing privacy@pegwatch.dev. We respond within 30 days.

If you are in the EU/UK, you have the right to lodge a complaint with your local data protection authority.

## 7. Cookies

PegWatch uses first-party cookies only for authentication (Clerk session). No third-party tracking cookies. No advertising cookies.

## 8. Security

We use industry-standard security practices:
- TLS 1.3 for all data in transit
- Encrypted at rest (database-level encryption)
- HMAC-verified webhooks for Stripe
- OWASP security headers on all responses
- Rate limiting (60 req/min/IP)

See our [Security Disclosure](/security) page for how to report vulnerabilities.

## 9. Children's privacy

PegWatch is not intended for children under 16. We do not knowingly collect data from children.

## 10. Changes to this policy

We will notify you of material changes via email and a banner on the dashboard. Continued use after notification constitutes acceptance.

## 11. Contact

privacy@pegwatch.dev
`;
