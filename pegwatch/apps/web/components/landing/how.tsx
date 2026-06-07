"use client";

import { Card } from "@/components/ui/card";

const steps = [
  {
    n: 1,
    title: "Pick your stables",
    body: "Free tier covers USDC, USDT, DAI. Pro unlocks 25+ including FRAX, TUSD, USDP, PYUSD, GUSD. API tier adds custom registration.",
  },
  {
    n: 2,
    title: "We aggregate 8+ venues",
    body: "Curve, Uniswap V3, Binance, Coinbase, Kraken, OKX, Bybit, Bitstamp. Median price + liquidity depth = one number you can trust.",
  },
  {
    n: 3,
    title: "Z-score watches 7d baseline",
    body: "Every minute, we recompute the z-score of current price vs your rolling 7-day mean. Persistent z > 2 = something real is happening.",
  },
  {
    n: 4,
    title: "Alerts go where you work",
    body: "Telegram, Discord, email, or any webhook. AI summary in plain English, with a recommendation. No raw data dumps.",
  },
];

export function HowItWorks() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-3">How it works</h2>
          <p className="text-text-muted">From raw on-chain data to a phone notification in under 60 seconds.</p>
        </div>
        <div className="grid md:grid-cols-4 gap-4">
          {steps.map((s) => (
            <Card key={s.n} className="relative">
              <div className="absolute -top-3 -left-3 w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-accent/30">
                {s.n}
              </div>
              <h3 className="font-semibold mb-2 mt-2">{s.title}</h3>
              <p className="text-sm text-text-muted">{s.body}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
