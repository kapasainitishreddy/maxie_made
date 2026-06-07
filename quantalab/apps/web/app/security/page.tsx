import { LegalPageLayout } from "@/components/legal/legal-layout";

export default function SecurityPage() {
  return (
    <LegalPageLayout title="Security" lastUpdated="January 1, 2026">
      <p>
        At Maxie Made, Inc., security is a top priority. This page describes the technical and
        organizational measures we take to protect your data.
      </p>

      <h2>Infrastructure Security</h2>
      <ul>
        <li><strong>Encryption in transit:</strong> All data is transmitted over TLS 1.3 with modern cipher suites.</li>
        <li><strong>Encryption at rest:</strong> All databases and backups are encrypted with AES-256.</li>
        <li><strong>Hosting:</strong> Vercel (frontend) and Fly.io (backend) — both SOC 2 Type II certified.</li>
        <li><strong>Database:</strong> Hosted on Neon (PostgreSQL) with automated daily backups and point-in-time recovery.</li>
        <li><strong>CDN:</strong> All static assets served via Cloudflare with DDoS protection.</li>
      </ul>

      <h2>Application Security</h2>
      <ul>
        <li><strong>Authentication:</strong> Industry-standard OAuth 2.0 / OpenID Connect via Clerk.</li>
        <li><strong>Authorization:</strong> Role-based access control (RBAC) with per-org isolation.</li>
        <li><strong>Rate limiting:</strong> 100 requests/minute per IP (30/min for write operations).</li>
        <li><strong>Input validation:</strong> All user input is validated server-side using Pydantic schemas.</li>
        <li><strong>SQL injection prevention:</strong> All database access uses SQLAlchemy ORM with parameterized queries.</li>
        <li><strong>XSS prevention:</strong> React's built-in escaping + strict Content Security Policy.</li>
        <li><strong>CSRF protection:</strong> SameSite cookies + token-based authentication.</li>
      </ul>

      <h2>Security Headers</h2>
      <p>Every response includes these security headers:</p>
      <ul>
        <li><code>Strict-Transport-Security</code> — force HTTPS for 1 year</li>
        <li><code>X-Content-Type-Options: nosniff</code> — prevent MIME sniffing</li>
        <li><code>X-Frame-Options: DENY</code> — prevent clickjacking</li>
        <li><code>Content-Security-Policy</code> — restrict script sources</li>
        <li><code>Referrer-Policy: strict-origin-when-cross-origin</code></li>
        <li><code>Permissions-Policy</code> — disable camera, mic, geolocation</li>
      </ul>

      <h2>Operational Security</h2>
      <ul>
        <li><strong>Dependency scanning:</strong> Automated daily scans via GitHub Dependabot + pip-audit.</li>
        <li><strong>Code scanning:</strong> GitHub CodeQL on every push.</li>
        <li><strong>Secret scanning:</strong> GitHub secret scanning enabled — no secrets in code.</li>
        <li><strong>Access control:</strong> Least-privilege access for all employees. MFA required on all production systems.</li>
        <li><strong>Audit logging:</strong> All authentication and authorization events are logged with timestamp and IP.</li>
        <li><strong>Incident response:</strong> 24-hour response time for critical security incidents.</li>
      </ul>

      <h2>Compliance</h2>
      <ul>
        <li><strong>GDPR:</strong> EU data subject rights fully supported. Data Processing Agreement (DPA) available on request.</li>
        <li><strong>CCPA:</strong> California consumer privacy rights supported.</li>
        <li><strong>SOC 2 Type II:</strong> Vercel and Fly.io are SOC 2 Type II certified. We are working toward our own SOC 2 certification.</li>
      </ul>

      <h2>Bug Bounty</h2>
      <p>
        We do not currently have a public bug bounty program, but we welcome responsible
        disclosure of security vulnerabilities. If you find a security issue, please email{" "}
        <a href="mailto:security@quantalab.io">security@quantalab.io</a> with:
      </p>
      <ul>
        <li>A description of the vulnerability</li>
        <li>Steps to reproduce</li>
        <li>Potential impact</li>
      </ul>
      <p>
        We will acknowledge your report within 48 hours and provide a timeline for a fix. We do
        not pursue legal action against good-faith security researchers.
      </p>

      <h2>Data Backup and Recovery</h2>
      <ul>
        <li>Daily automated backups of all production databases</li>
        <li>30-day backup retention</li>
        <li>Point-in-time recovery available</li>
        <li>Disaster recovery plan tested quarterly</li>
      </ul>

      <h2>Contact</h2>
      <p>
        For security questions or to report a vulnerability, contact{" "}
        <a href="mailto:security@quantalab.io">security@quantalab.io</a>.
        For GPG-encrypted communication, request our public key via email.
      </p>
    </LegalPageLayout>
  );
}
