"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingDown, Bell, DollarSign } from "lucide-react";

export function Scenario() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-12">
          <Badge variant="info" className="mb-3">Case study</Badge>
          <h2 className="text-3xl md:text-4xl font-bold mb-3">
            Helmsworth Treasury caught the USDC depeg 47 minutes early
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Helmsworth is a $200M crypto fund. Their treasury held $42M in USDC
            across Aave, Compound, and Curve. This is what happened.
          </p>
        </div>

        <div className="space-y-4 max-w-4xl mx-auto">
          <Card>
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-bg-elevated flex items-center justify-center flex-shrink-0">
                <Bell className="w-5 h-5 text-warn" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold">T-47 min</span>
                  <Badge variant="warning">WATCH</Badge>
                </div>
                <p className="text-text-muted text-sm">
                  USDC at $0.9982 on Curve. Z-score +2.4 (3σ). Liquidity depth at
                  ±0.5% drops to $8.2M (from $42M). PegWatch fires a Telegram alert
                  to the treasury ops channel.
                </p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-bg-elevated flex items-center justify-center flex-shrink-0">
                <TrendingDown className="w-5 h-5 text-crit" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold">T-12 min</span>
                  <Badge variant="critical">CRITICAL</Badge>
                </div>
                <p className="text-text-muted text-sm">
                  USDC at $0.9912. Z-score +4.1. Curve 3pool becomes 70% USDC,
                  30% USDT. The peg is breaking. AI summary: "USDC depeg in progress,
                  expect $0.985 floor within 30 minutes, recommend immediate exit
                  from Aave aUSDC positions."
                </p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-bg-elevated flex items-center justify-center flex-shrink-0">
                <DollarSign className="w-5 h-5 text-ok" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold">T+0 to T+38 min</span>
                  <Badge variant="success">EXITED</Badge>
                </div>
                <p className="text-text-muted text-sm">
                  Helmsworth exits 100% of Aave USDC positions. Converts to USDT
                  (still pegged) via Curve. Redeploys to Maker DSR. USDC bottoms
                  at $0.8703 eighteen minutes later. Helmsworth's peak drawdown:
                  -0.04% (gas + slippage). Without PegWatch, the model drawdown:
                  -3.2%, or $1.34M.
                </p>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-8 max-w-4xl mx-auto">
          <Card className="bg-gradient-to-br from-accent/10 to-emerald-400/5 border-accent/30">
            <div className="grid md:grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold gradient-text">$1.34M</div>
                <div className="text-xs text-text-muted mt-1">Saved vs baseline</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text">47 min</div>
                <div className="text-xs text-text-muted mt-1">Lead time before depeg</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text">8 stables</div>
                <div className="text-xs text-text-muted mt-1">Monitored simultaneously</div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
}
