export const TERMS_MARKDOWN = `# Terms of Service — QuantaLab

**Last updated:** 2026-06-06

By accessing or using QuantaLab ("the Service"), you agree to be bound by these Terms.

## 1. Eligibility

You must be at least 18 years old and have authority to enter into a contract.

## 2. Acceptable Use

You agree NOT to:
- Reverse-engineer, decompile, or attempt to extract source code
- Use the Service to build a competing product
- Use the Service for any illegal purpose
- Circumvent rate limits, authentication, or sandbox restrictions
- Use the sandbox to attack our infrastructure or other tenants
- Resell or sublicense access without written permission
- Publish marketplace strategies that contain malware, crypto miners, or resource abuse

## 3. Service Tiers & Payment

| Tier | Price | Includes |
|---|---|---|
| Free | $0/mo | 3 notebooks, 10 backtests/mo, local Ollama |
| Researcher | $199/mo | Unlimited notebooks, 1k backtests/mo, cloud Ollama |
| Quant Shop | $999/mo | 10 seats, shared notebooks, factor attribution, fine-tuning |

- All fees in USD, exclusive of taxes
- Monthly billing on the 1st; annual = 2 months free
- Failed payments retry automatically; service suspends after 14 days
- Refunds: pro-rata for annual plans with 30 days notice

## 4. Sandbox Use

The sandboxed Python kernel is provided "as is" with these constraints:
- No internet access
- No filesystem access outside notebook working directory
- 5-minute execution limit per cell
- Memory and CPU limits
- Allowlisted imports only

**Abuse of the sandbox** (crypto mining, attempting to break out, resource exhaustion) will result in immediate account termination without refund.

## 5. Intellectual Property

**Your code** — You retain all rights to your strategy code, notebooks, and backtests.

**The Service** — We retain all rights to the platform, algorithms, models, and documentation.

**Marketplace listings** — When you publish a strategy:
- You retain IP rights
- You grant buyers a non-exclusive, non-transferable license
- We take a 15% rev share
- You can delist at any time
- You warrant that the strategy does not infringe any third-party IP

## 6. Financial Disclaimers

**We are NOT a broker-dealer, investment advisor, or financial institution.**

**Backtests are illustrative only.** They do not represent actual trading and may not reflect real-world conditions (slippage, liquidity, market impact).

**Past performance does NOT guarantee future results.** Strategies that worked historically may lose money in the future.

**No investment advice.** Strategy descriptions, backtest results, and AI-generated signals are for informational purposes only.

## 7. Disclaimers

THE SERVICE IS PROVIDED "AS IS". WE DO NOT WARRANT THAT:
- Backtests are accurate (they are simulations)
- The Service will be uninterrupted or error-free
- The sandbox is bug-free (we patch CVEs but no system is 100% secure)
- Generated code is correct or profitable

## 8. Limitation of Liability

OUR AGGREGATE LIABILITY IS LIMITED TO THE FEES YOU PAID US IN THE 3 MONTHS PRECEDING THE CLAIM.

IN NO EVENT SHALL WE BE LIABLE FOR INDIRECT, INCIDENTAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS FROM USING A STRATEGY.

## 9. Termination

- **By you** — Cancel anytime. Access continues until end of billing period.
- **By us** — We may terminate for: (a) non-payment, (b) material breach, (c) sandbox abuse.
- **Effect** — Your data is retained for 30 days, then deleted.

## 10. Confidentiality

We will treat your strategy code, backtest results, and unpublished research as confidential. We will not disclose to third parties except: (a) with your consent, (b) to comply with law, (c) to subprocessors under equivalent confidentiality.

## 11. Governing Law & Disputes

These Terms are governed by the laws of [Your State/Country]. Disputes resolved by binding arbitration in [Your City].

## 12. Contact

- Email: legal@quantalab.com
- Support: support@quantalab.com
- Address: [Your registered business address]`;
