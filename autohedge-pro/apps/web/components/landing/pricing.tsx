"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Check } from "lucide-react";
import Link from "next/link";

const PLANS = [
  {
    name: "Hobby",
    price: "$0",
    period: "/mo",
    description: "Paper trading, backtest, one strategy at a time.",
    features: [
      "Paper trading only",
      "5 backtests / month",
      "1 active strategy",
      "Standard market data",
      "Community support",
    ],
    cta: "Start free",
    href: "/sign-up",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "$99",
    period: "/mo + 0.5% AUM",
    description: "12 strategies, paper + live via Alpaca/IBKR, regime detection.",
    features: [
      "Everything in Hobby",
      "12 pre-built strategies",
      "Unlimited backtests + Monte Carlo",
      "Live trading via Alpaca or IBKR",
      "HMM regime detection",
      "Priority email support",
    ],
    cta: "Start 14-day trial",
    href: "/sign-up",
    highlighted: true,
  },
  {
    name: "Family Office",
    price: "$499",
    period: "/mo + 0.3% AUM",
    description: "For $1M+ AUM. Custom strategies, dedicated strategist.",
    features: [
      "Everything in Pro",
      "AUM capped at $2k/mo (0.3%)",
      "Custom strategy development",
      "Multi-account / multi-broker",
      "Dedicated quant strategist",
      "Monthly performance review",
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
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Simple, transparent pricing.</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            Pay for what you trade. Not for what you don't.
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
                <Button asChild size="lg" className="w-full" variant={p.highlighted ? "default" : "outline"}>
                  <Link href={p.href}>{p.cta}</Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
        <p className="text-center text-text-muted text-sm mt-8">
          14-day free trial. No card required. Cancel anytime.
        </p>
      </div>
    </section>
  );
}
