export const TERMS_MARKDOWN = `# Terms of Service — CloudFinOps Co-Pilot

**Last updated:** 2026-06-06

By accessing or using CloudFinOps Co-Pilot ("the Service"), you agree to be bound by these Terms.

## 1. Eligibility

You must be at least 18 years old and have authority to enter into a contract on behalf of yourself or your organization.

## 2. Acceptable Use

You agree NOT to:
- Reverse-engineer, decompile, or attempt to extract source code
- Use the Service to build a competing product
- Provide write-level IAM access (we require read-only)
- Use the Service for any illegal purpose
- Circumvent rate limits, authentication, or access controls
- Resell or sublicense access without written permission

## 3. Service Tiers & Payment

| Tier | Pricing | Model |
|---|---|---|
| Pay-as-you-save | 20% of verified savings | Performance-based, no base fee |
| Enterprise | Custom | Monthly retainer + savings share |

- We charge **only** on verified savings (measured for 30 days)
- If we save $0, you pay $0
- No refunds on already-paid invoices. Disputed savings trigger a 14-day investigation.

## 4. Authorization Model

You grant us a **read-only IAM role** in your cloud account. This role permits:
- Listing resources (EC2, RDS, S3, etc.)
- Reading cost & usage reports
- Reading CloudWatch metrics
- Reading tags and metadata

The role **does NOT permit**: creating, modifying, or deleting resources, accessing data plane, or reading secrets. We never request write access.

**We deploy changes only via Terraform PR that you review and approve in Slack/GitHub.** Every change is auditable and reversible in 1 click.

## 5. Intellectual Property

**Your data** — You retain all rights to your cloud infrastructure data, cost reports, and Terraform configurations.

**The Service** — We retain all rights to the platform, algorithms, and documentation.

**Generated Terraform** — You own the Terraform we generate. Use it freely, modify it, or fork it.

## 6. Disclaimers

THE SERVICE IS PROVIDED "AS IS". WE DO NOT WARRANT THAT:
- Savings estimates will be realized (we verify for 30 days before billing)
- The Service will be uninterrupted or error-free
- Generated Terraform will work in all environments without modification

**We are not responsible for**: changes to cloud provider APIs, IAM misconfigurations on your side, third-party outages (AWS, GCP, Azure, Vercel, Fly.io), or force majeure events.

## 7. Limitation of Liability

OUR AGGREGATE LIABILITY IS LIMITED TO THE FEES YOU PAID US IN THE 12 MONTHS PRECEDING THE CLAIM.

IN NO EVENT SHALL WE BE LIABLE FOR INDIRECT, INCIDENTAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES.

## 8. Service Level Agreement

- 99.9% uptime for the dashboard, API, and Terraform generation
- Service credits: 5% of monthly fee per hour of downtime, capped at 100%
- Excludes: scheduled maintenance, force majeure, third-party outages

## 9. Termination

- **By you** — Cancel anytime. You pay only for verified savings to date.
- **By us** — We may terminate for: (a) non-payment after 14-day grace, (b) material breach, (c) abuse. 30 days' notice for non-breach.
- **Effect** — We revoke our IAM access within 24 hours. Your data is retained for 30 days, then deleted.

## 10. Confidentiality

We will treat your cloud infrastructure data, Terraform configurations, and business information as confidential. We will not disclose to third parties except: (a) with your consent, (b) to comply with law, (c) to subprocessors under equivalent confidentiality.

## 11. Governing Law & Disputes

These Terms are governed by the laws of [Your State/Country]. Disputes resolved by binding arbitration in [Your City].

## 12. Contact

- Email: legal@cloudfinops-copilot.com
- Support: support@cloudfinops-copilot.com
- Address: [Your registered business address]`;
