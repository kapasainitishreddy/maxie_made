"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { api, BacktestResult, MarketplaceStrategy } from "@/lib/api";
import { formatPct } from "@/lib/utils";
import {
  Loader2,
  Sparkles,
  Play,
  FlaskConical,
  TrendingUp,
  Activity,
  ShoppingBag,
  ArrowUpRight,
  ArrowDownRight,
  BookOpen,
  Zap,
} from "lucide-react";

interface BacktestRow {
  id: string;
  strategy_name: string;
  asset: string;
  sharpe: number;
  total_return: number;
  max_drawdown: number;
}

const NL_PRESETS = [
  "Buy when 20-day SMA crosses above 50-day SMA; sell on reverse",
  "Buy when RSI drops below 30, sell when RSI rises above 70",
  "Hold SPY overnight only, flat intraday (overnight edge)",
  "Buy when price breaks above 20-day high (momentum breakout)",
];

export default function DashboardPage() {
  const [backtests, setBacktests] = useState<BacktestRow[]>([]);
  const [topStrategies, setTopStrategies] = useState<MarketplaceStrategy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Quick backtest form state
  const [description, setDescription] = useState(NL_PRESETS[0]);
  const [running, setRunning] = useState(false);
  const [latest, setLatest] = useState<BacktestResult | null>(null);
  const [latestCode, setLatestCode] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [bt, ms] = await Promise.all([
        api.get<BacktestRow[]>("/backtest").catch(() => [] as BacktestRow[]),
        api.get<MarketplaceStrategy[]>("/marketplace").catch(() => [] as MarketplaceStrategy[]),
      ]);
      setBacktests(bt || []);
      setTopStrategies((ms || []).slice(0, 4));
    } catch (e: any) {
      setError(e?.message || "Failed to load dashboard");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const runQuick = async () => {
    setRunning(true);
    setError(null);
    try {
      const r = await api.post<{ code: string; result: BacktestResult }>("/backtest/nl2code", {
        description,
      });
      setLatestCode(r.code);
      setLatest(r.result);
      // Refresh list
      api.get<BacktestRow[]>("/backtest").then((b) => setBacktests(b || [])).catch(() => {});
    } catch (e: any) {
      setError(e?.message || "Backtest failed");
    } finally {
      setRunning(false);
    }
  };

  // Aggregate stats
  const totalBacktests = backtests.length;
  const avgSharpe =
    totalBacktests > 0
      ? backtests.reduce((s, b) => s + (b.sharpe || 0), 0) / totalBacktests
      : 0;
  const bestReturn =
    totalBacktests > 0
      ? Math.max(...backtests.map((b) => b.total_return || 0))
      : 0;
  const avgDrawdown =
    totalBacktests > 0
      ? backtests.reduce((s, b) => s + (b.max_drawdown || 0), 0) / totalBacktests
      : 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-text-muted">
            Run a backtest, browse the strategy marketplace, and track your research.
          </p>
        </div>
        <div className="flex gap-2">
          <Link href="/notebook">
            <Button variant="outline" size="sm">
              <BookOpen className="h-4 w-4 mr-2" />
              Open notebook
            </Button>
          </Link>
          <Link href="/marketplace">
            <Button size="sm">
              <ShoppingBag className="h-4 w-4 mr-2" />
              Marketplace
            </Button>
          </Link>
        </div>
      </div>

      {error && (
        <div className="rounded-md border border-danger/40 bg-danger/10 p-3 text-sm text-danger">
          {error}
        </div>
      )}

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={<FlaskConical className="h-4 w-4 text-accent" />}
          label="Backtests run"
          value={loading ? "…" : String(totalBacktests)}
          accent
        />
        <StatCard
          icon={<Activity className="h-4 w-4" />}
          label="Avg Sharpe"
          value={loading ? "…" : avgSharpe.toFixed(2)}
        />
        <StatCard
          icon={<TrendingUp className="h-4 w-4 text-success" />}
          label="Best return"
          value={loading ? "…" : formatPct(bestReturn)}
          trend={bestReturn >= 0 ? "up" : "down"}
        />
        <StatCard
          icon={<ArrowDownRight className="h-4 w-4 text-danger" />}
          label="Avg max drawdown"
          value={loading ? "…" : formatPct(avgDrawdown)}
        />
      </div>

      {/* Quick backtest */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-accent" />
            Quick backtest
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-2">
            <Input
              placeholder="Describe a strategy in plain English…"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="flex-1"
            />
            <Button onClick={runQuick} disabled={running || !description.trim()}>
              {running ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Play className="h-4 w-4 mr-2" />
              )}
              Run on SPY
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {NL_PRESETS.map((p) => (
              <button
                key={p}
                onClick={() => setDescription(p)}
                className="text-xs px-2 py-1 rounded border border-border bg-bg-surface text-text-muted hover:text-text hover:border-accent transition-colors"
              >
                {p.length > 50 ? p.slice(0, 50) + "…" : p}
              </button>
            ))}
          </div>

          {latest && (
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
              <ResultStat
                label="Final value"
                value={`$${(latest.final_value || 0).toFixed(0)}`}
              />
              <ResultStat
                label="Total return"
                value={formatPct(latest.total_return || 0)}
                trend={(latest.total_return || 0) >= 0 ? "up" : "down"}
              />
              <ResultStat label="Sharpe" value={(latest.sharpe || 0).toFixed(2)} />
              <ResultStat label="Sortino" value={(latest.sortino || 0).toFixed(2)} />
              <ResultStat
                label="Trades"
                value={String(latest.num_trades || 0)}
              />
            </div>
          )}

          {latestCode && (
            <details className="text-xs">
              <summary className="cursor-pointer text-text-muted hover:text-text">
                View generated Python
              </summary>
              <pre className="mt-2 p-3 rounded bg-bg-surface border border-border overflow-x-auto text-text-muted">
                {latestCode}
              </pre>
            </details>
          )}
        </CardContent>
      </Card>

      {/* Recent backtests + Top strategies */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Recent backtests</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-12" />
                ))}
              </div>
            ) : backtests.length === 0 ? (
              <p className="text-sm text-text-muted">
                No backtests yet. Run one above to populate this list.
              </p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-text-muted border-b border-border">
                      <th className="py-2 pr-4 font-medium">Strategy</th>
                      <th className="py-2 pr-4 font-medium">Asset</th>
                      <th className="py-2 pr-4 font-medium">Sharpe</th>
                      <th className="py-2 pr-4 font-medium">Return</th>
                      <th className="py-2 font-medium">Drawdown</th>
                    </tr>
                  </thead>
                  <tbody>
                    {backtests.slice(0, 8).map((b) => (
                      <tr key={b.id} className="border-b border-border/50 last:border-0">
                        <td className="py-2 pr-4 font-medium">{b.strategy_name}</td>
                        <td className="py-2 pr-4 text-text-muted">{b.asset}</td>
                        <td className="py-2 pr-4">{(b.sharpe || 0).toFixed(2)}</td>
                        <td className="py-2 pr-4">
                          <span
                            className={
                              (b.total_return || 0) >= 0 ? "text-success" : "text-danger"
                            }
                          >
                            {formatPct(b.total_return || 0)}
                          </span>
                        </td>
                        <td className="py-2 text-danger">
                          {formatPct(b.max_drawdown || 0)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingBag className="h-4 w-4" />
              Top marketplace strategies
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-16" />
                ))}
              </div>
            ) : topStrategies.length === 0 ? (
              <p className="text-sm text-text-muted">No strategies loaded.</p>
            ) : (
              <ul className="space-y-3">
                {topStrategies.map((s) => (
                  <li
                    key={s.id}
                    className="border border-border/60 rounded p-3 hover:border-accent/50 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0 flex-1">
                        <div className="font-medium text-sm truncate">{s.name}</div>
                        <div className="text-xs text-text-muted truncate">
                          by {s.author}
                        </div>
                      </div>
                      <Badge variant="secondary" className="shrink-0">
                        ⭐ {s.rating?.toFixed(1) || "—"}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 mt-2 text-xs text-text-muted">
                      <span>{s.downloads?.toLocaleString() || 0} downloads</span>
                      <span>·</span>
                      <span>
                        {s.price_cents === 0 ? "Free" : `$${(s.price_cents / 100).toFixed(0)}`}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
            <Link
              href="/marketplace"
              className="inline-flex items-center text-sm text-accent hover:underline mt-3"
            >
              Browse all strategies
              <ArrowUpRight className="h-3 w-3 ml-1" />
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  accent,
  trend,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  accent?: boolean;
  trend?: "up" | "down";
}) {
  const valueClass =
    trend === "up" ? "text-success" : trend === "down" ? "text-danger" : accent ? "text-accent" : "";
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-2 text-text-muted text-xs mb-1">
          {icon}
          <span>{label}</span>
        </div>
        <div className={`text-2xl font-bold ${valueClass}`}>{value}</div>
      </CardContent>
    </Card>
  );
}

function ResultStat({
  label,
  value,
  trend,
}: {
  label: string;
  value: string;
  trend?: "up" | "down";
}) {
  const valueClass =
    trend === "up" ? "text-success" : trend === "down" ? "text-danger" : "";
  return (
    <div className="rounded border border-border bg-bg-surface p-2">
      <div className="text-xs text-text-muted">{label}</div>
      <div className={`text-lg font-semibold ${valueClass}`}>{value}</div>
    </div>
  );
}
