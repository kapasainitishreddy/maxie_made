"use client";
import { useEffect, useState } from "react";
import { api, CloudAccount, Recommendation, ApiError } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Cloud, TrendingDown, Server, Loader2, Plus } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

export default function Dashboard() {
  const [accounts, setAccounts] = useState<CloudAccount[]>([]);
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const [a, r] = await Promise.all([
        api.get<CloudAccount[]>("/accounts"),
        api.get<Recommendation[]>("/recommendations"),
      ]);
      setAccounts(a); setRecs(r);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const totalSavings = recs.reduce((sum, r) => sum + r.monthly_savings, 0);
  const totalCost = accounts.reduce((sum, a) => sum + a.monthly_cost, 0);

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="h-8 w-8 animate-spin text-accent" /></div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-text-muted">Your cloud cost command center</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard icon={Cloud} label="Current monthly spend" value={formatCurrency(totalCost)} trend={`${accounts.length} account${accounts.length !== 1 ? "s" : ""}`} />
        <StatCard icon={TrendingDown} label="Identified savings" value={formatCurrency(totalSavings)} trend={`${recs.length} recommendations`} />
        <StatCard icon={Server} label="Resources scanned" value={accounts.reduce((s, a) => s + a.resource_count, 0).toString()} trend="Last scan: 2h ago" />
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Cloud Accounts</CardTitle>
          <Button size="sm"><Plus className="h-4 w-4 mr-2" />Connect</Button>
        </CardHeader>
        <CardContent>
          {accounts.length === 0 ? (
            <div className="text-center py-12 text-text-muted">
              <Cloud className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No accounts connected. Click "Connect" to add your first AWS/GCP/Azure account.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {accounts.map((a) => (
                <div key={a.id} className="flex items-center justify-between p-3 rounded-lg bg-bg-elevated border border-border">
                  <div>
                    <div className="font-medium">{a.account_name}</div>
                    <div className="text-sm text-text-muted">{a.provider.toUpperCase()} · {a.account_id} · {a.region}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold">{formatCurrency(a.monthly_cost)}/mo</div>
                    <div className="text-xs text-text-muted">{a.resource_count} resources</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Top Savings Opportunities</CardTitle></CardHeader>
        <CardContent>
          {recs.length === 0 ? (
            <div className="text-center py-12 text-text-muted">
              <TrendingDown className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No recommendations yet. Scan an account to find savings opportunities.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {recs.slice(0, 5).map((r) => (
                <div key={r.id} className="p-3 rounded-lg bg-bg-elevated border border-border">
                  <div className="flex items-start justify-between mb-1">
                    <div className="font-medium">{r.title}</div>
                    <div className="text-accent font-bold">{formatCurrency(r.monthly_savings)}/mo</div>
                  </div>
                  <p className="text-sm text-text-muted mb-2">{r.description}</p>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="px-2 py-0.5 rounded bg-bg-surface text-text-muted uppercase">{r.rec_type}</span>
                    <span className={`px-2 py-0.5 rounded ${r.risk === "low" ? "bg-emerald-500/20 text-emerald-300" : r.risk === "high" ? "bg-red-500/20 text-red-300" : "bg-amber-500/20 text-amber-300"} uppercase`}>{r.risk}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
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
