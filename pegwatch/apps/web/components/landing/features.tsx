"use client";

import { Card } from "@/components/ui/card";
import { Activity, Bell, Database, GitBranch, LineChart, Shield } from "lucide-react";

const features = [
  {
    icon: LineChart,
    title: "Real-time peg tracking",
    body: "Median price aggregated across Curve, Uniswap V3, and 5+ CEXs. Refresh every minute on Pro.",
  },
  {
    icon: GitBranch,
    title: "Z-score early-warning",
    body: "Statistical deviation vs your 7-day baseline. Alerts fire on |z| ≥ 2.0, not when the crowd is already panicking.",
  },
  {
    icon: Database,
    title: "Liquidity depth scan",
    body: "See how much stable liquidity is parked within ±0.5% of peg. Low depth + z = 2 = real danger.",
  },
  {
    icon: Bell,
    title: "Telegram, Discord, email, webhook",
    body: "Route alerts to wherever you already work. Per-symbol filters, severity thresholds, no spam.",
  },
  {
    icon: Activity,
    title: "Treasury attestation tracking",
    body: "Monitor Circle, Tether, and Paxos reserve publications. Velocity drop = canary in the coal mine.",
  },
  {
    icon: Shield,
    title: "AI incident summaries",
    body: "Local Ollama (no API cost) generates plain-English incident reports. No marketing fluff.",
  },
];

export function Features() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-3">Built for the people who lose money when stables break</h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Most depeg tools show you what already happened. PegWatch tells you it's about to.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map((f) => (
            <Card key={f.title} className="hover:border-accent/30 transition-colors">
              <f.icon className="w-8 h-8 text-accent mb-3" />
              <h3 className="font-semibold mb-2">{f.title}</h3>
              <p className="text-sm text-text-muted">{f.body}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
