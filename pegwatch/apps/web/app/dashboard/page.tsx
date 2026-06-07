"use client";

import { useEffect, useState } from "react";
import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api, type PegStatus } from "@/lib/api";
import { formatPct, formatUSD, formatZ, formatUSDshort, severityColor, severityDot } from "@/lib/utils";
import { RefreshCw, TrendingUp, AlertCircle, Activity, DollarSign } from "lucide-react";

export default function DashboardPage() {
  const [statuses, setStatuses] = useState<PegStatus[] | null>(null);
  const [refreshing, setRefreshing] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());

  async function load() {
    try {
      const data = await api.allStatus();
      setStatuses(data);
      setError(null);
      setLastRefresh(new Date());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 30_000); // auto-refresh every 30s
    return () => clearInterval(t);
  }, []);

  async function refreshOne(symbol: string) {
    setRefreshing(symbol);
    try {
      await api.refresh(symbol);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Refresh failed");
    } finally {
      setRefreshing(null);
    }
  }

  const total = statuses?.length || 0;
  const critical = statuses?.filter((s) => s.severity === "critical").length || 0;
  const warning = statuses?.filter((s) => s.severity === "warning").length || 0;
  const watch = statuses?.filter((s) => s.severity === "watch").length || 0;
  const totalMcap = statuses?.reduce((a, s) => a + s.market_cap_usd, 0) || 0;

  return (
    <>
      <Topnav />
      <main className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">Live peg monitor</h1>
            <p className="text-text-muted text-sm mt-1">
              Auto-refreshes every 30s · last refresh {lastRefresh.toLocaleTimeString()}
            </p>
          </div>
        </div>

        {error && (
          <Card className="mb-6 border-crit/30 bg-crit/5">
            <div className="flex items-center gap-2 text-crit">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
          </Card>
        )}

        {/* Summary stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <Card className="!p-4">
            <div className="flex items-center gap-2 text-xs text-text-muted mb-1">
              <Activity className="w-3 h-3" /> Stables
            </div>
            <div className="text-2xl font-bold">{total}</div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-2 text-xs text-text-muted mb-1">
              <DollarSign className="w-3 h-3" /> Aggregate mcap
            </div>
            <div className="text-2xl font-bold">{formatUSDshort(totalMcap)}</div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-2 text-xs text-text-muted mb-1">
              <TrendingUp className="w-3 h-3 text-warn" /> Active alerts
            </div>
            <div className="text-2xl font-bold">
              {critical > 0 ? <span className="text-crit">{critical}</span> : null}
              {critical > 0 && (warning > 0 || watch > 0) ? " + " : null}
              {warning > 0 ? <span className="text-warn">{warning}</span> : null}
              {warning > 0 && watch > 0 ? " + " : null}
              {watch > 0 ? <span className="text-yellow-400">{watch}</span> : null}
              {critical === 0 && warning === 0 && watch === 0 ? <span className="text-ok">0</span> : null}
            </div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-2 text-xs text-text-muted mb-1">
              <RefreshCw className="w-3 h-3" /> Sources
            </div>
            <div className="text-2xl font-bold">8</div>
            <div className="text-xs text-text-muted">Curve · Uni · 5 CEX</div>
          </Card>
        </div>

        {/* Stablecoin cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {statuses === null && (
            <div className="col-span-full text-center py-12 text-text-muted">Loading...</div>
          )}
          {statuses?.map((s) => (
            <Card key={s.symbol} className="hover:border-accent/30 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-accent flex items-center justify-center text-white font-bold">
                    {s.symbol.slice(0, 1)}
                  </div>
                  <div>
                    <div className="font-semibold">{s.symbol}</div>
                    <div className="text-xs text-text-muted">{s.issuer}</div>
                  </div>
                </div>
                <Badge variant={s.severity === "healthy" ? "success" : s.severity === "watch" ? "info" : s.severity === "warning" ? "warning" : "critical"}>
                  <span className={`w-1.5 h-1.5 rounded-full ${severityDot(s.severity)}`} />
                  {s.severity}
                </Badge>
              </div>

              <div className="grid grid-cols-3 gap-3 my-4">
                <div>
                  <div className="text-xs text-text-muted">Price</div>
                  <div className="text-lg font-bold font-mono">{formatUSD(s.price_usd)}</div>
                </div>
                <div>
                  <div className="text-xs text-text-muted">Deviation</div>
                  <div className={`text-lg font-bold font-mono ${Math.abs(s.deviation_pct) > 0.1 ? "text-warn" : ""}`}>
                    {formatPct(s.deviation_pct)}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-text-muted">Z-score</div>
                  <div className="text-lg font-bold font-mono">{formatZ(s.z_score)}</div>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs text-text-muted mb-3">
                <span>Liquidity: {formatUSDshort(s.liquidity_depth_usd)}</span>
                <span>{s.sources_count} sources</span>
              </div>

              <div className="flex items-center justify-between">
                <a href={`https://www.coingecko.com/en/coins/${s.name.toLowerCase().replace(/ /g, "-")}`} target="_blank" rel="noreferrer" className="text-xs text-text-muted hover:text-text">
                  View on CoinGecko →
                </a>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => refreshOne(s.symbol)}
                  disabled={refreshing === s.symbol}
                >
                  <RefreshCw className={`w-3 h-3 ${refreshing === s.symbol ? "animate-spin" : ""}`} />
                  Refresh
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </main>
      <LegalFooter />
    </>
  );
}
