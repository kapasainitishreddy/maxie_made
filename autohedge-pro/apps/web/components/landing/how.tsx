"use client";
import { Card } from "@/components/ui/card";
import { LineChart, FlaskConical, Bot, Wallet } from "lucide-react";

const steps = [
  { n: 1, icon: LineChart, title: "Pick from 12 pre-built strategies", body: "SMA, RSI, momentum, vol breakout, pairs trading, statarb, trend following, breakout, funding arb, options spreads, delta-neutral, buy & hold." },
  { n: 2, icon: FlaskConical, title: "Walk-forward + Monte Carlo validation", body: "Out-of-sample backtesting. 5,000 Monte Carlo paths. Equity curve fan. We show you the worst case, not just the best case." },
  { n: 3, icon: Bot, title: "HMM regime detector runs 24/7", body: "Bear, bull, sideways chop, crash. Auto-rebalances position sizes when regimes shift. Defensive in chaos, aggressive in trends." },
  { n: 4, icon: Wallet, title: "Paper or live, you keep custody", body: "Connect IBKR or Alpaca. We place orders via their API. You own every share. Pay $99/mo + 0.5% AUM, capped at $2k/mo." },
];

export function HowItWorks() {
  return (
    <section id="how" className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">How AutoHedge Pro works</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">Four steps. No PhD required. Your broker keeps custody, you keep control.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {steps.map((s) => (
            <Card key={s.n} className="p-6 relative">
              <div className="absolute -top-3 -left-3 h-8 w-8 rounded-full bg-gradient-accent text-white text-sm font-bold flex items-center justify-center">{s.n}</div>
              <s.icon className="h-8 w-8 text-accent mb-3" />
              <h3 className="text-lg font-semibold mb-2">{s.title}</h3>
              <p className="text-sm text-text-muted leading-relaxed">{s.body}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
