import { Check, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const tiers = [
  {
    name: "Starter",
    price: 999,
    description: "For solo IP attorneys getting started",
    features: [
      "5,000 patent searches / month",
      "3 saved landscapes",
      "1 watchlist with email alerts",
      "PDF reports",
      "Email support",
    ],
  },
  {
    name: "Pro",
    price: 2499,
    description: "For boutique IP teams",
    features: [
      "50,000 patent searches / month",
      "Unlimited landscapes",
      "10 watchlists",
      "Infringement alerts + claim charts",
      "FTO + landscape reports",
      "Priority support",
      "MCP server access",
    ],
    popular: true,
  },
  {
    name: "Enterprise",
    price: 4999,
    description: "For pharma IP departments",
    features: [
      "Unlimited searches",
      "Unlimited everything",
      "API access + webhooks",
      "SSO + audit logs",
      "Custom integrations",
      "Dedicated CSM",
      "SOC2 + custom DPA",
    ],
  },
];

export function Pricing() {
  return (
    <section className="py-20 md:py-32 bg-bg-surface/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Simple, transparent pricing.
          </h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            Start free. Pay when you scale. Cancel anytime.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {tiers.map((tier, i) => (
            <Card
              key={i}
              className={`p-8 relative ${tier.popular ? "border-accent/60 shadow-2xl shadow-accent/20" : ""}`}
            >
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <Badge variant="default" className="bg-gradient-accent text-white px-3 py-1">
                    <Star className="h-3 w-3 mr-1" /> Most popular
                  </Badge>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-2xl font-bold mb-2">{tier.name}</h3>
                <p className="text-text-muted text-sm">{tier.description}</p>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-1">
                  <span className="text-5xl font-bold">${tier.price}</span>
                  <span className="text-text-muted">/mo</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {tier.features.map((feat, j) => (
                  <li key={j} className="flex items-start gap-2 text-sm">
                    <Check className="h-4 w-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>

              <Button
                asChild
                className="w-full"
                variant={tier.popular ? "default" : "outline"}
              >
                <Link href="/sign-up">Start free trial</Link>
              </Button>
            </Card>
          ))}
        </div>

        <p className="text-center mt-12 text-text-muted text-sm">
          All plans include 14-day free trial. No credit card required.
        </p>
      </div>
    </section>
  );
}
