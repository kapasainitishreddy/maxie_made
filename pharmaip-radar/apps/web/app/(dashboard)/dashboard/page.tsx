"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileText, AlertTriangle, BarChart3, Eye, Loader2 } from "lucide-react";
import { api, PatentSearchResult, InfringementAlert, Report, ApiError } from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardPage() {
  const [patents, setPatents] = useState<PatentSearchResult | null>(null);
  const [alerts, setAlerts] = useState<InfringementAlert[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const [p, r] = await Promise.all([
          api.get<PatentSearchResult>("/patents?page_size=1"),
          api.get<Report[]>("/reports"),
        ]);
        setPatents(p);
        setReports(r);
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Skeleton key={i} className="h-32" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-text-muted">Overview of your pharma IP intelligence</p>
      </div>

      {error && (
        <Card className="border-red-500/50 bg-red-500/5">
          <CardContent className="pt-6 text-red-300">
            {error}. Make sure the backend is running on port 8000.
          </CardContent>
        </Card>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={FileText}
          label="Patents tracked"
          value={patents?.total.toLocaleString() ?? "—"}
          trend="Real-time from USPTO + EPO"
        />
        <StatCard
          icon={AlertTriangle}
          label="Infringement alerts"
          value={alerts.length.toString()}
          trend="Active watchlist alerts"
        />
        <StatCard
          icon={BarChart3}
          label="Reports generated"
          value={reports.length.toString()}
          trend="FTO + landscape + infringement"
        />
        <StatCard
          icon={Eye}
          label="Watchlists"
          value="1"
          trend="1 active"
        />
      </div>

      {/* Recent reports */}
      <Card>
        <CardHeader>
          <CardTitle>Recent reports</CardTitle>
          <CardDescription>Generated FTO and landscape reports</CardDescription>
        </CardHeader>
        <CardContent>
          {reports.length === 0 ? (
            <div className="text-center py-12 text-text-muted">
              <BarChart3 className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No reports yet. Generate your first FTO report to see it here.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {reports.slice(0, 5).map((r) => (
                <div
                  key={r.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-bg-elevated border border-border"
                >
                  <div>
                    <div className="font-medium">{r.title}</div>
                    <div className="text-sm text-text-muted">
                      {new Date(r.created_at).toLocaleString()}
                    </div>
                  </div>
                  <Badge variant={r.status === "ready" ? "success" : "warning"}>
                    {r.status}
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  trend,
}: {
  icon: any;
  label: string;
  value: string;
  trend: string;
}) {
  return (
    <Card className="hover:border-accent/40 transition-all">
      <CardContent className="pt-6">
        <div className="flex items-center justify-between mb-2">
          <Icon className="h-5 w-5 text-accent" />
        </div>
        <div className="text-3xl font-bold mb-1">{value}</div>
        <div className="text-sm text-text-muted">{label}</div>
        <div className="text-xs text-text-muted mt-2">{trend}</div>
      </CardContent>
    </Card>
  );
}
