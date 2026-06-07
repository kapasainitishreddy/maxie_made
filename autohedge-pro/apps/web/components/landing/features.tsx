"use client";
import { Card } from "@/components/ui/card";
import { LineChart, FlaskConical, Bot, Wallet } from "lucide-react";

const features = [
  { icon: LineChart, title: "12 strategies pre-built", description: "SMA, RSI, momentum, vol breakout, pairs trading, statarb, trend following, breakout, funding arb, options spreads, delta-neutral, buy & hold. All production-tested, all backtestable." },
  { icon: FlaskConical, title: "Walk-forward + Monte Carlo", description: "Real out-of-sample backtesting. 5,000 Monte Carlo paths. Equity curve fan, not a point estimate. See the worst case, not the best case." },
  { icon: Bot, title: "HMM regime detection", description: "Hidden Markov Model classifier. Bear, bull, sideways chop, crash. Auto-rebalances position sizes when regimes shift. Defensive in chaos, aggressive in trends." },
  { icon: Wallet, title: "Paper + Live via Alpaca/IBKR", description: "Free paper trading to validate. Go live with one click via Alpaca or Interactive Brokers. You keep custody of every share. Pay $99/mo + 0.5% AUM, capped at $2k/mo." },
];

export function Features() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Trading, automated.
          </h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            No PhD required. Built for retail traders and family offices.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {features.map((f, i) => (
            <Card key={i} className="p-6 hover:border-accent/50 transition-all group">
              <div className="h-12 w-12 rounded-lg bg-gradient-accent/10 border border-accent/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <f.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
              <p className="text-sm text-text-muted leading-relaxed">{f.description}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
