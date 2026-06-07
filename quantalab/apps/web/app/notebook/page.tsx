"use client";
import { useState } from "react";
import { api, BacktestResult } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Sparkles, Play, Code2 } from "lucide-react";
import { formatPct } from "@/lib/utils";

const DEFAULT_CODE = `# Buy when 20-day SMA crosses above 50-day SMA; sell on reverse.
def signals(prices):
    fast = prices.rolling(20).mean()
    slow = prices.rolling(50).mean()
    out = []
    for i in range(1, len(prices)):
        if fast.iloc[i-1] < slow.iloc[i-1] and fast.iloc[i] > slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "buy"})
        elif fast.iloc[i-1] > slow.iloc[i-1] and fast.iloc[i] < slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "sell"})
    return out
`;

export default function Notebook() {
  const [description, setDescription] = useState("Buy when RSI drops below 30, sell when RSI rises above 70");
  const [code, setCode] = useState(DEFAULT_CODE);
  const [translating, setTranslating] = useState(false);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const translate = async () => {
    setTranslating(true); setError(null);
    try {
      const r = await api.post<{ code: string; result: BacktestResult }>("/backtest/nl2code", { description });
      setCode(r.code);
      setResult(r.result);
    } catch (e: any) { setError(e.message); } finally { setTranslating(false); }
  };

  const run = async () => {
    setRunning(true); setError(null);
    try {
      const r = await api.post<BacktestResult>("/backtest/run", { code, asset: "SPY", start_date: "2023-01-01", end_date: "2024-01-01" });
      if (r.error) { setError(r.error); } else { setResult(r); }
    } catch (e: any) { setError(e.message); } finally { setRunning(false); }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Notebook</h1>
        <p className="text-text-muted">Describe a strategy in plain English. We'll write the Python.</p>
      </div>

      <Card className="p-6">
        <div className="flex gap-2 mb-3">
          <Input
            placeholder="Describe your strategy..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="flex-1"
          />
          <Button onClick={translate} disabled={translating || !description.trim()}>
            {translating ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Sparkles className="h-4 w-4 mr-2" />}
            Translate to Python
          </Button>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2"><Code2 className="h-4 w-4" /> Strategy code</CardTitle>
            <Button size="sm" onClick={run} disabled={running}>
              {running ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
              Run backtest
            </Button>
          </CardHeader>
          <CardContent>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-96 p-4 rounded-lg bg-bg-elevated border border-border font-mono text-xs focus:outline-none focus:border-accent"
              spellCheck={false}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Backtest results</CardTitle></CardHeader>
          <CardContent>
            {error && <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-sm mb-3">{error}</div>}
            {!result && !error && (
              <div className="text-center py-12 text-text-muted">
                <Sparkles className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>Translate or run a backtest to see results.</p>
              </div>
            )}
            {result && (
              <div className="space-y-3">
                <Metric label="Total return" value={formatPct(result.total_return)} positive={result.total_return >= 0} />
                <Metric label="Sharpe ratio" value={result.sharpe.toFixed(2)} />
                <Metric label="Sortino ratio" value={result.sortino.toFixed(2)} />
                <Metric label="Max drawdown" value={formatPct(result.max_drawdown)} positive={result.max_drawdown >= 0} />
                <Metric label="Num trades" value={result.num_trades.toString()} />
                <Metric label="Final value" value={`$${result.final_value.toFixed(2)}`} />
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function Metric({ label, value, positive }: { label: string; value: string; positive?: boolean }) {
  return (
    <div className="flex justify-between p-3 rounded-lg bg-bg-elevated">
      <span className="text-text-muted text-sm">{label}</span>
      <span className={`font-bold ${positive === true ? "text-emerald-400" : positive === false ? "text-red-400" : "text-text"}`}>{value}</span>
    </div>
  );
}
