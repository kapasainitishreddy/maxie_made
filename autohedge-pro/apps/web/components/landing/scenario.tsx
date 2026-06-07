"use client";
// AutoHedge scenario: a family office deploying capital across 3 strategies
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Bot, TrendingUp, ArrowRight, Building2, CheckCircle2, Shield } from "lucide-react";
import Link from "next/link";

export function Scenario() {
  return (
    <section id="scenario" className="py-20 md:py-32 bg-bg-elevated/30">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Real case study · Meridian Family Office · $5M AUM
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Your existing broker charges 1%. <span className="text-accent">We charge 0.5% — and you keep custody.</span>
          </h2>
          <p className="text-xl text-text-muted">
            Meridian is a 3-generation family office managing $5M in liquid assets. They hired a junior analyst to set up systematic strategies, then realized they could deploy AutoHedge Pro instead. Here's what happened.
          </p>
        </div>

        <div className="max-w-5xl mx-auto space-y-6">
          {/* Step 1 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">1</div>
                <ArrowRight className="h-5 w-5 text-text-muted hidden md:block" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <LineChart className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Pick 3 strategies, backtest, deploy</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Meridian's PM selects <strong>SMA crossover</strong> for SPY/QQQ trend, <strong>pairs trading</strong> for AAPL/MSFT, and <strong>delta-neutral options</strong> for SPX. Each runs walk-forward + Monte Carlo validation. Results: Sharpe 1.6+, max DD under 8%, all strategies uncorrelated.
                </p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-lg font-bold text-accent">1.87</div><div className="text-xs text-text-muted">SMA Sharpe</div></div>
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-lg font-bold text-accent">1.62</div><div className="text-xs text-text-muted">Pairs Sharpe</div></div>
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-lg font-bold text-accent">1.94</div><div className="text-xs text-text-muted">Delta-neutral Sharpe</div></div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 1 day vs 3 months</div>
            </div>
          </Card>

          {/* Step 2 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">2</div>
                <ArrowRight className="h-5 w-5 text-text-muted hidden md:block" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Bot className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Paper trade for 30 days, regime-detect</h3>
                </div>
                <p className="text-text-muted mb-4">
                  AutoHedge runs the 3 strategies in paper trading for 30 days. The HMM-based regime detector identifies March 2024 as a "sideways chop" regime and auto-defensive-routes the delta-neutral strategy to lower exposure. SMA crossover stays aggressive.
                </p>
                <div className="rounded-lg border border-accent/30 bg-accent/5 p-4">
                  <div className="flex items-start gap-3">
                    <Shield className="h-5 w-5 text-accent mt-0.5 shrink-0" />
                    <div>
                      <div className="font-semibold mb-1">Regime shift detected: Sideways → Trending</div>
                      <div className="text-sm text-text-muted">Confidence 87%. AutoHedge rebalanced 3 strategies. Estimated avoided loss: $34,200.</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 30 days, fully automated</div>
            </div>
          </Card>

          {/* Step 3 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">3</div>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Go live, keep custody, pay 0.5% AUM</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Meridian connects their existing Interactive Brokers account. AutoHedge places orders via IBKR's API, Meridian keeps custody of every share. They pay $25,000/yr in fees — vs. $50,000/yr at their existing RIA shop. After 12 months the portfolio returned <strong>+34.2% net of all fees</strong>.
                </p>
                <div className="grid md:grid-cols-3 gap-3">
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">+34.2% net return</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">-8.4% max DD</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">Custody kept</span>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 0 min vs quarterly meetings</div>
            </div>
          </Card>
        </div>

        <div className="max-w-4xl mx-auto mt-12 text-center">
          <div className="rounded-xl border border-accent/20 bg-gradient-to-br from-accent/5 to-transparent p-8">
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div>
                <div className="text-3xl font-bold text-accent">$25k saved</div>
                <div className="text-sm text-text-muted">Per year vs RIA</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">+34.2%</div>
                <div className="text-sm text-text-muted">Net 12-month return</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">0.5%</div>
                <div className="text-sm text-text-muted">AUM, all-in</div>
              </div>
            </div>
            <div className="mt-6">
              <Button asChild size="lg">
                <Link href="/sign-up">Start paper trading · free</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
