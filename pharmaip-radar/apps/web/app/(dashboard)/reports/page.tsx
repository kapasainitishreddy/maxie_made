"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, LandscapeSummary, Report, ReportType, ApiError } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Plus, FileText, Loader2, BarChart3 } from "lucide-react";

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState("FTO — New Drug");
  const [drug, setDrug] = useState("Keytruda");
  const [type, setType] = useState<ReportType>("fto");

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get<Report[]>("/reports");
      setReports(r);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const generate = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    setError(null);
    try {
      await api.post<Report>("/reports", {
        report_type: type,
        title,
        target_drug: drug,
        query: {},
      });
      setShowForm(false);
      await load();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to generate");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Reports</h1>
          <p className="text-text-muted">FTO, landscape, and infringement reports</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          New report
        </Button>
      </div>

      {showForm && (
        <Card className="p-6">
          <form onSubmit={generate} className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Type</label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value as ReportType)}
                className="w-full h-10 rounded-lg border border-border bg-bg-surface px-3 text-sm"
              >
                <option value="fto">FTO (Freedom to Operate)</option>
                <option value="landscape">IP Landscape</option>
                <option value="infringement">Infringement</option>
                <option value="patentability">Patentability</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Title</label>
              <Input value={title} onChange={(e) => setTitle(e.target.value)} required />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Target drug</label>
              <Input value={drug} onChange={(e) => setDrug(e.target.value)} placeholder="e.g. Keytruda" />
            </div>
            {error && <div className="text-red-300 text-sm">{error}</div>}
            <div className="flex gap-2">
              <Button type="submit" disabled={generating}>
                {generating && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                Generate
              </Button>
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {loading ? (
        <Skeleton className="h-64" />
      ) : reports.length === 0 ? (
        <Card className="p-12 text-center">
          <BarChart3 className="h-12 w-12 mx-auto mb-3 text-text-muted" />
          <p className="text-text-muted">No reports yet. Click "New report" to generate your first one.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {reports.map((r) => (
            <Card key={r.id} className="hover:border-accent/40 transition-all">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <Badge variant="secondary" className="uppercase text-xs">
                    {r.report_type}
                  </Badge>
                  <Badge variant={r.status === "ready" ? "success" : "warning"}>
                    {r.status}
                  </Badge>
                </div>
                <CardTitle className="text-lg mt-2">{r.title}</CardTitle>
                <CardDescription>{new Date(r.created_at).toLocaleString()}</CardDescription>
              </CardHeader>
              <CardContent>
                {r.status === "ready" && (
                  <Button asChild size="sm" variant="outline" className="w-full">
                    <a href={`/api/proxy/reports/${r.id}/pdf`} target="_blank" rel="noopener">
                      <FileText className="h-4 w-4 mr-2" />
                      Download PDF
                    </a>
                  </Button>
                )}
                {r.error && <div className="text-xs text-red-300 mt-2">{r.error}</div>}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
