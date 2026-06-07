"use client";
import { useEffect, useState } from "react";
import { api, Strategy, BacktestResult, PortfolioSnapshot, Trade } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Loader2, TrendingUp, Briefcase, Activity, BarChart3, Play, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { formatCurrency, formatPct } from "@/lib/utils";

export default function Dashboard() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [portfolio, setPortfolio] = useState<PortfolioSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [selectedStrategy, setSelectedStrategy] = useState("sma_crossover");
  const [startDate, setStartDate] = useState("2023-01-01");
  const [endDate, setEndDate] = useState("2024-01-01");
  const [initialCapital, setInitialCapital] = useState(100000);
  const [latestBacktest, setLatestBacktest] = useState<BacktestResult | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const [s, p, t] = await Promise.all([
        api.get<Strategy[]>("/strategies/catalog"),
        api.get<PortfolioSnapshot>("/portfolio/snapshot"),
        api.get<Trade[]>("/portfolio/trades").catch(() => [] as Trade[]),
      ]);
      setStrategies(s); setPortfolio(p); setTrades(t);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const runBacktest = async () => {
    setRunning(true);
    try {
      const r = await api.post<BacktestResult>("/backtest/run", {
        strategy_kind: selectedStrategy, asset: "SPY", start_date: startDate, end_date: endDate, initial_capital: initialCapital, params: {},
      });
      setLatestBacktest(r);
    } catch (e) { console.error(e); } finally { setRunning(false); }
  };

  const refreshPortfolio = async () => {
    try {
      const p = await api.get<PortfolioSnapshot>("/portfolio/snapshot");
      setPortfolio(p);
    } catch (e) { console.error(e); }
  };

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="h-8 w-8 animate-spin text-accent" /></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-1">Dashboard</h1>
          <p className="text-text-muted">Your trading command center · Paper + live · 12 strategies</p>
        </div>
        <Button variant="outline" size="sm" onClick={refreshPortfolio}>Refresh</Button>
      </div>

      {/* Top stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard icon={Briefcase} label="Portfolio value" value={formatCurrency(portfolio?.total_value ?? 100000)} trend={`Cash: ${formatCurrency(portfolio?.cash ?? 0)}`} />
        <StatCard icon={Activity} label="Open positions" value={(portfolio?.positions.length ?? 0).toString()} trend={`${portfolio?.num_trades ?? 0} total trades`} />
        <StatCard icon={BarChart3} label="Strategies" value={strategies.length.toString()} trend="Ready to deploy" />
        <StatCard icon={TrendingUp} label="Latest backtest" value={latestBacktest ? formatPct(latestBacktest.total_return) : "—"} trend={latestBacktest ? `Sharpe ${latestBacktest.sharpe.toFixed(2)}` : "Run one below"} />
      </div>

      {/* Equity curve */}
      {latestBacktest && latestBacktest.equity_curve && latestBacktest.equity_curve.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Equity curve — {selectedStrategy} · {startDate} → {endDate}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={latestBacktest.equity_curve.map(p => ({ ...p, t: new Date(p.timestamp).toLocaleDateString() }))}>
                  <CartesianGrid stroke="#333" strokeDasharray="3 3" />
                  <XAxis dataKey="t" stroke="#888" fontSize={11} />
                  <YAxis stroke="#888" fontSize={11} tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f0f17', border: '1px solid #333' }} formatter={(v: any) => formatCurrency(v)} />
                  <Line type="monotone" dataKey="equity" stroke="#f59e0b" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Backtest form + results */}
      <div id="backtest" className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle>Run a backtest</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div>
              <label className="text-sm font-medium mb-1 block">Strategy</label>
              <Select value={selectedStrategy} onChange={(e) => setSelectedStrategy(e.target.value)}>
                {strategies.map(s => <option key={s.kind} value={s.kind}>{s.name}</option>)}
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div><label className="text-sm font-medium mb-1 block">Start</label><Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} /></div>
              <div><label className="text-sm font-medium mb-1 block">End</label><Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} /></div>
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">Initial capital</label>
              <Input type="number" value={initialCapital} onChange={(e) => setInitialCapital(Number(e.target.value))} min={1000} step={1000} />
            </div>
            <Button onClick={runBacktest} disabled={running} className="w-full">
              {running ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
              {running ? "Running backtest..." : "Run backtest"}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Latest backtest result</CardTitle></CardHeader>
          <CardContent>
            {!latestBacktest ? (
              <div className="text-center py-12 text-text-muted">
                <TrendingUp className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>Run a backtest to see results here.</p>
              </div>
            ) : (
              <div className="space-y-2">
                <ResultRow label="Total return" value={formatPct(latestBacktest.total_return)} positive={latestBacktest.total_return >= 0} />
                <ResultRow label="Sharpe" value={latestBacktest.sharpe.toFixed(2)} />
                <ResultRow label="Sortino" value={latestBacktest.sortino.toFixed(2)} />
                <ResultRow label="Max drawdown" value={formatPct(latestBacktest.max_drawdown)} negative />
                <ResultRow label="Trades" value={latestBacktest.num_trades.toString()} />
                <ResultRow label="Final value" value={formatCurrency(latestBacktest.final_value)} positive />
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Open positions */}
      <Card>
        <CardHeader>
          <CardTitle>Open positions</CardTitle>
        </CardHeader>
        <CardContent>
          {!portfolio || portfolio.positions.length === 0 ? (
            <div className="text-center py-8 text-text-muted">
              <Briefcase className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No open positions yet. Execute a trade from the API or come back after the paper-trader runs.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-text-muted text-left">
                    <th className="py-2 px-2">Symbol</th>
                    <th className="py-2 px-2 text-right">Qty</th>
                    <th className="py-2 px-2 text-right">Avg entry</th>
                    <th className="py-2 px-2 text-right">Current</th>
                    <th className="py-2 px-2 text-right">Market value</th>
                    <th className="py-2 px-2 text-right">Unrealized P&L</th>
                  </tr>
                </thead>
                <tbody>
                  {portfolio.positions.map((pos, i) => (
                    <tr key={i} className="border-b border-border/50">
                      <td className="py-2 px-2 font-semibold">{pos.symbol}</td>
                      <td className="py-2 px-2 text-right font-mono">{pos.quantity.toFixed(2)}</td>
                      <td className="py-2 px-2 text-right font-mono">${pos.avg_entry.toFixed(2)}</td>
                      <td className="py-2 px-2 text-right font-mono">${pos.current_price.toFixed(2)}</td>
                      <td className="py-2 px-2 text-right font-mono">{formatCurrency(pos.market_value)}</td>
                      <td className={`py-2 px-2 text-right font-mono ${pos.unrealized_pnl >= 0 ? "text-emerald-400" : "text-red-400"}`}>
                        {pos.unrealized_pnl >= 0 ? "+" : ""}{formatCurrency(pos.unrealized_pnl)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Strategy library */}
      <div id="strategies">
        <h2 className="text-2xl font-bold mb-3">Strategy library</h2>
        <p className="text-text-muted mb-4 text-sm">12 production-tested strategies across 4 categories: trend, mean reversion, arbitrage, options.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {strategies.map((s) => (
            <button
              key={s.kind}
              onClick={() => setSelectedStrategy(s.kind)}
              className={`text-left p-4 rounded-lg border transition-all ${
                selectedStrategy === s.kind ? "border-accent bg-accent/10" : "border-border bg-bg-elevated hover:border-accent/50"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <Activity className="h-4 w-4 text-accent" />
                <div className="font-semibold text-sm">{s.name}</div>
              </div>
              <div className="text-xs text-text-muted line-clamp-2">{s.description}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, trend }: any) {
  return (
    <Card className="hover:border-accent/40 transition-all">
      <CardContent className="pt-6">
        <Icon className="h-5 w-5 text-accent mb-2" />
        <div className="text-3xl font-bold mb-1">{value}</div>
        <div className="text-sm text-text-muted">{label}</div>
        <div className="text-xs text-text-muted mt-2">{trend}</div>
      </CardContent>
    </Card>
  );
}

function ResultRow({ label, value, positive, negative }: { label: string; value: string; positive?: boolean; negative?: boolean }) {
  return (
    <div className="flex justify-between py-1">
      <span className="text-text-muted">{label}</span>
      <span className={`font-bold ${positive ? "text-emerald-400" : negative ? "text-red-400" : ""}`}>{value}</span>
    </div>
  );
}
