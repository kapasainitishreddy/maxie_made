import { LegalPageLayout } from "@/components/legal/legal-layout";

export default function PrivacyPage() {
  return (
    <LegalPageLayout title="Privacy Policy" lastUpdated="January 1, 2026">
      <p>
        Maxie Made, Inc. ("we", "us", "our") operates PharmaIP Radar (the "Service"). This page
        informs you of our policies regarding the collection, use, and disclosure of personal data
        when you use our Service and the choices you have associated with that data.
      </p>

      <h2>1. Information We Collect</h2>
      <h3>Account Data</h3>
      <p>
        When you sign up via Clerk, we collect your email address, name, and profile picture. We do
        not have access to your password.
      </p>
      <h3>Usage Data</h3>
      <p>
        We automatically collect information about how you interact with the Service, including
        pages visited, features used, and timestamps. This is collected via Plausible Analytics
        (privacy-friendly, no cookies, no personal data).
      </p>
      <h3>Customer Data</h3>
      <p>
        When you upload patent data, search queries, or saved landscapes, this data is stored in
        our database and associated with your account. We do not use your data to train AI models.
      </p>

      <h2>2. How We Use Your Information</h2>
      <ul>
        <li>To provide and maintain the Service</li>
        <li>To notify you about changes to the Service</li>
        <li>To provide customer support</li>
        <li>To detect and prevent fraud or abuse</li>
        <li>To comply with legal obligations</li>
      </ul>

      <h2>3. Data Sharing</h2>
      <p>
        We do not sell your personal data. We share data only with:
      </p>
      <ul>
        <li><strong>Clerk</strong> — authentication (privacy policy: <a href="https://clerk.com/privacy">clerk.com/privacy</a>)</li>
        <li><strong>Stripe</strong> — payment processing (privacy policy: <a href="https://stripe.com/privacy">stripe.com/privacy</a>)</li>
        <li><strong>Plausible Analytics</strong> — privacy-friendly analytics (privacy policy: <a href="https://plausible.io/data-policy">plausible.io/data-policy</a>)</li>
        <li><strong>Hosting providers</strong> (Vercel, Fly.io) — infrastructure</li>
      </ul>

      <h2>4. Data Retention</h2>
      <p>
        We retain your account data for as long as your account is active. You can request deletion
        of your account and all associated data at any time by emailing{" "}
        <a href="mailto:privacy@pharmaip-radar.com">privacy@pharmaip-radar.com</a>.
      </p>

      <h2>5. Your Rights (GDPR / CCPA)</h2>
      <p>You have the right to:</p>
      <ul>
        <li>Access the personal data we hold about you</li>
        <li>Correct inaccurate data</li>
        <li>Request deletion of your data</li>
        <li>Object to processing of your data</li>
        <li>Data portability (export your data)</li>
      </ul>

      <h2>6. Security</h2>
      <p>
        We use industry-standard security measures including encryption in transit (TLS 1.3),
        encryption at rest (AES-256), regular security audits, and rate limiting. See our{" "}
        <a href="/security">Security page</a> for details.
      </p>

      <h2>7. Children's Privacy</h2>
      <p>
        Our Service is not intended for children under 13. We do not knowingly collect personal
        data from children under 13.
      </p>

      <h2>8. Changes to This Policy</h2>
      <p>
        We may update this privacy policy from time to time. We will notify you of any changes by
        posting the new policy on this page and updating the "Last updated" date.
      </p>

      <h2>9. Contact</h2>
      <p>
        For privacy questions or to exercise your rights, contact us at{" "}
        <a href="mailto:privacy@pharmaip-radar.com">privacy@pharmaip-radar.com</a>.
      </p>
    </LegalPageLayout>
  );
}
