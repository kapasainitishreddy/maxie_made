"use client";
import { useEffect, useState } from "react";
import { api, CloudAccount, Recommendation, ApiError } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { TrendingDown, Check, X, Code } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

export default function Recommendations() {
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [accounts, setAccounts] = useState<CloudAccount[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const [r, a] = await Promise.all([
        api.get<Recommendation[]>("/recommendations"),
        api.get<CloudAccount[]>("/accounts"),
      ]);
      setRecs(r); setAccounts(a);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const approve = async (id: string) => {
    try { await api.post(`/recommendations/${id}/approve`); await load(); } catch (e) { console.error(e); }
  };
  const reject = async (id: string) => {
    try { await api.post(`/recommendations/${id}/reject`); await load(); } catch (e) { console.error(e); }
  };

  if (loading) return <div className="space-y-4">{[1,2,3].map(i => <Skeleton key={i} className="h-32" />)}</div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Recommendations</h1>
        <p className="text-text-muted">{recs.length} opportunities · {formatCurrency(recs.reduce((s, r) => s + r.monthly_savings, 0))} potential monthly savings</p>
      </div>

      {recs.length === 0 ? (
        <Card className="p-12 text-center">
          <TrendingDown className="h-12 w-12 mx-auto mb-3 text-text-muted" />
          <p className="text-text-muted">No recommendations yet. Connect a cloud account and run a scan.</p>
        </Card>
      ) : (
        <div className="space-y-3">
          {recs.map((r) => (
            <Card key={r.id} className="hover:border-accent/40 transition-all">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="font-semibold text-lg mb-1">{r.title}</div>
                    <p className="text-sm text-text-muted">{r.description}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-accent">{formatCurrency(r.monthly_savings)}</div>
                    <div className="text-xs text-text-muted">/month</div>
                  </div>
                </div>
                <div className="flex items-center gap-2 mb-3 text-xs">
                  <Badge variant="outline" className="uppercase">{r.rec_type}</Badge>
                  <Badge variant={r.risk === "low" ? "success" : r.risk === "high" ? "danger" : "warning"} className="uppercase">{r.risk} risk</Badge>
                  <Badge variant={r.status === "approved" ? "success" : r.status === "rejected" ? "destructive" : "secondary"} className="uppercase">{r.status}</Badge>
                </div>
                {r.terraform_hcl && (
                  <details className="mb-3">
                    <summary className="text-sm text-text-muted cursor-pointer hover:text-accent flex items-center gap-1">
                      <Code className="h-3 w-3" /> View Terraform
                    </summary>
                    <pre className="mt-2 p-3 rounded bg-bg p-3 overflow-x-auto text-xs font-mono">{r.terraform_hcl}</pre>
                  </details>
                )}
                {r.status === "pending" && (
                  <div className="flex gap-2">
                    <Button size="sm" onClick={() => approve(r.id)}><Check className="h-4 w-4 mr-1" />Approve</Button>
                    <Button size="sm" variant="outline" onClick={() => reject(r.id)}><X className="h-4 w-4 mr-1" />Reject</Button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
