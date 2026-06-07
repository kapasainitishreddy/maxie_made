"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Check } from "lucide-react";
import Link from "next/link";
import { UpgradeButton } from "@/components/billing/upgrade-button";

const PLANS = [
  {
    name: "Pay-as-you-save",
    planId: "performance",
    price: "20%",
    period: "of verified savings",
    description: "We only get paid when we actually save you money.",
    features: [
      "AWS, GCP, Azure cost analysis",
      "30 days of usage + 90 days of metrics",
      "Unlimited recommendations",
      "Terraform PR per fix",
      "Slack approval workflow",
      "1 auditor seat",
    ],
    cta: "Get a free audit",
    href: "/sign-up",
    highlighted: true,
  },
  {
    name: "Enterprise",
    planId: null,
    price: "Custom",
    period: "talk to sales",
    description: "For companies with 10+ engineers and 5+ accounts.",
    features: [
      "Everything in Pay-as-you-save",
      "Multi-org, SSO, SAML",
      "Custom Terraform modules",
      "Dedicated FinOps engineer",
      "Quarterly business review",
      "SLA + 99.9% uptime",
    ],
    cta: "Talk to sales",
    href: "/sign-up",
    highlighted: false,
  },
];

export function Pricing() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Performance-based pricing.</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            No base fee. We take 20% of what we actually save you. Verified for 30 days before you pay.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {PLANS.map((p) => (
            <Card key={p.name} className={`p-8 ${p.highlighted ? "border-accent shadow-lg shadow-accent/20" : ""}`}>
              <CardContent className="pt-0 space-y-6">
                <div>
                  <h3 className="text-2xl font-bold mb-2">{p.name}</h3>
                  <p className="text-sm text-text-muted">{p.description}</p>
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-5xl font-bold">{p.price}</span>
                  <span className="text-text-muted">{p.period}</span>
                </div>
                <ul className="space-y-2">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm">
                      <Check className="h-4 w-4 text-accent mt-0.5 shrink-0" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                {p.planId ? (
                  <UpgradeButton plan={p.planId} variant={p.highlighted ? "default" : "outline"} size="lg">
                    {p.cta}
                  </UpgradeButton>
                ) : (
                  <Button asChild size="lg" className="w-full" variant={p.highlighted ? "default" : "outline"}>
                    <Link href={p.href}>{p.cta}</Link>
                  </Button>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
        <p className="text-center text-text-muted text-sm mt-8">
          Free 30-day audit. No card required. No commitment.
        </p>
      </div>
    </section>
  );
}
