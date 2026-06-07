import { LegalPageLayout } from "@/components/legal/legal-layout";

export default function TermsPage() {
  return (
    <LegalPageLayout title="Terms of Service" lastUpdated="January 1, 2026">
      <p>
        These Terms of Service ("Terms") govern your access to and use of CloudFinOps Co-Pilot (the
        "Service"), operated by Maxie Made, Inc. ("we", "us", "our"). By accessing or using the
        Service, you agree to be bound by these Terms.
      </p>

      <h2>1. Account Terms</h2>
      <ul>
        <li>You must be 18 years or older to use this Service.</li>
        <li>You are responsible for maintaining the security of your account and password.</li>
        <li>You are responsible for all activity that occurs under your account.</li>
        <li>You must not share your account credentials with third parties.</li>
      </ul>

      <h2>2. Acceptable Use</h2>
      <p>You agree not to:</p>
      <ul>
        <li>Use the Service for any illegal purpose or in violation of any laws.</li>
        <li>Reverse-engineer, decompile, or attempt to extract the source code of the Service.</li>
        <li>Upload malicious code, viruses, or any content designed to harm the Service.</li>
        <li>Scrape, crawl, or use automated tools to access the Service without our written permission.</li>
        <li>Interfere with or disrupt the Service or its servers.</li>
        <li>Use the Service to infringe on any third party's intellectual property rights.</li>
      </ul>

      <h2>3. Subscription and Payment</h2>
      <p>
        Paid plans are billed monthly or annually via Stripe. By subscribing, you authorize us to
        charge your payment method on a recurring basis until you cancel.
      </p>
      <ul>
        <li>You may cancel at any time from your account settings.</li>
        <li>Cancellation takes effect at the end of your current billing period.</li>
        <li>We do not provide refunds for partial months or unused portions of your subscription.</li>
        <li>We reserve the right to change pricing with 30 days notice.</li>
      </ul>

      <h2>4. Intellectual Property</h2>
      <p>
        The Service, including all underlying technology, software, designs, and content (excluding
        user-uploaded content), is the property of Maxie Made, Inc. and protected by US and
        international copyright, trademark, and patent laws.
      </p>
      <p>
        You retain all rights to the data you upload to the Service. You grant us a limited
        license to use this data solely to provide the Service to you.
      </p>


      <h2>6. Termination</h2>
      <p>
        We may terminate or suspend your account at any time, with or without cause, with or
        without notice, including but not limited to breach of these Terms. Upon termination, your
        right to use the Service ceases immediately.
      </p>

      <h2>7. Limitation of Liability</h2>
      <p>
        To the maximum extent permitted by law, in no event shall Maxie Made, Inc., its directors,
        employees, partners, or affiliates be liable for any indirect, incidental, special,
        consequential, or punitive damages, including loss of profits, data, or goodwill, resulting
        from your access to or use of the Service.
      </p>

      <h2>8. Disclaimer of Warranties</h2>
      <p>
        The Service is provided "AS IS" and "AS AVAILABLE" without warranties of any kind, either
        express or implied. We do not warrant that the Service will be uninterrupted, error-free,
        or free of viruses or other harmful components.
      </p>

      <h2>9. Governing Law</h2>
      <p>
        These Terms shall be governed by and construed in accordance with the laws of the State of
        Delaware, without regard to its conflict of law provisions.
      </p>

      <h2>10. Changes to Terms</h2>
      <p>
        We reserve the right to modify these Terms at any time. We will notify users of any
        material changes via email or in-app notification. Your continued use of the Service
        after such changes constitutes acceptance of the new Terms.
      </p>

      <h2>11. Contact</h2>
      <p>
        For questions about these Terms, contact us at{" "}
        <a href="mailto:legal@cloudfinops.io">legal@cloudfinops.io</a>.
      </p>
    </LegalPageLayout>
  );
}
