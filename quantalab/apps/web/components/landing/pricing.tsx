"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Check } from "lucide-react";
import Link from "next/link";
import { UpgradeButton } from "@/components/billing/upgrade-button";

const PLANS = [
  {
    name: "Free",
    planId: null,
    price: "$0",
    period: "/mo",
    description: "For learning and exploring. Up to 3 notebooks.",
    features: [
      "3 notebooks",
      "10 backtests / month",
      "Local Ollama NL→Code",
      "Community marketplace",
      "Community support",
    ],
    cta: "Start free",
    href: "/sign-up",
    highlighted: false,
  },
  {
    name: "Researcher",
    planId: "researcher",
    price: "$199",
    period: "/mo",
    description: "For solo quants. Unlimited notebooks, 1k backtests/month.",
    features: [
      "Unlimited notebooks",
      "1,000 backtests / month",
      "Cloud Ollama (qwen3:8b)",
      "Marketplace publishing (15% rev share)",
      "Walk-forward + Monte Carlo",
      "Priority email support",
    ],
    cta: "Start 3-day trial",
    href: "/sign-up",
    highlighted: true,
  },
  {
    name: "Quant Shop",
    planId: "quant",
    price: "$999",
    period: "/mo",
    description: "For 2-10 person quant teams. Shared notebooks, multi-user.",
    features: [
      "Everything in Researcher",
      "10 seats included",
      "Shared notebooks + comments",
      "Factor attribution + regime detection",
      "Custom model fine-tuning",
      "Dedicated Slack channel",
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
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Priced for quants, not enterprises.</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            Free for learning. $199/mo for solo. $999/mo for teams. No data fees.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {PLANS.map((p) => (
            <Card key={p.name} className={`p-6 ${p.highlighted ? "border-accent shadow-lg shadow-accent/20" : ""}`}>
              <CardContent className="pt-0 space-y-6">
                <div>
                  <h3 className="text-2xl font-bold mb-2">{p.name}</h3>
                  <p className="text-sm text-text-muted">{p.description}</p>
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold">{p.price}</span>
                  <span className="text-text-muted text-sm">{p.period}</span>
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
          All plans include sandboxed execution, walk-forward validation, and marketplace access.
        </p>
      </div>
    </section>
  );
}
