"use client";

import { useEffect, useState } from "react";
import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api, type Plan } from "@/lib/api";
import { Check } from "lucide-react";

export default function PricingPage() {
  const [plans, setPlans] = useState<Plan[]>([]);

  useEffect(() => {
    api.plans().then(setPlans).catch(() => {});
  }, []);

  return (
    <>
      <Topnav />
      <main className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-3">Pricing</h1>
          <p className="text-text-muted max-w-xl mx-auto">
            Free for 3 stables, forever. Pro for serious treasury teams. API for funds and platforms.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((p) => {
            const isPro = p.id === "pro";
            return (
              <Card
                key={p.id}
                className={`relative ${isPro ? "border-accent/50 shadow-lg shadow-accent/10" : ""}`}
              >
                {isPro && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <Badge variant="info">Most popular</Badge>
                  </div>
                )}
                <h3 className="font-semibold text-lg mb-1">{p.name}</h3>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-4xl font-bold">${p.price_usd}</span>
                  <span className="text-text-muted text-sm">/month</span>
                </div>
                <p className="text-xs text-text-muted mb-6">
                  {p.id === "free" ? "No credit card required" : p.id === "pro" ? "Cancel anytime" : "Volume pricing available"}
                </p>
                <ul className="space-y-2 mb-6 text-sm">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2">
                      <Check className="w-4 h-4 text-ok flex-shrink-0 mt-0.5" />
                      <span className="text-text-muted">{f}</span>
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full"
                  variant={isPro ? "primary" : "outline"}
                  onClick={() => {
                    if (p.id === "free") {
                      window.location.href = "/dashboard";
                    } else {
                      api.checkout(p.id as "pro" | "api").then((r) => {
                        if (r.dev_mode) {
                          window.location.href = r.url;
                        } else {
                          window.location.href = r.url;
                        }
                      });
                    }
                  }}
                >
                  {p.id === "free" ? "Get started" : `Subscribe to ${p.name}`}
                </Button>
              </Card>
            );
          })}
        </div>

        <div className="max-w-2xl mx-auto mt-16">
          <Card>
            <h3 className="font-semibold mb-2">Refund policy</h3>
            <p className="text-sm text-text-muted">
              All plans are month-to-month with no commitment. Cancel any time from your dashboard — you'll
              keep access until the end of your billing period. We don't do annual lock-ins because the
              stablecoin landscape changes too fast.
            </p>
          </Card>
        </div>
      </main>
      <LegalFooter />
    </>
  );
}
