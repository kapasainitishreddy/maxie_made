"use client";

import { useEffect, useState } from "react";
import { api, Watchlist, InfringementAlert, ApiError } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Plus, Eye, AlertTriangle, Loader2, Trash2 } from "lucide-react";

export default function WatchlistPage() {
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("Watch Keytruda competitors");
  const [drug, setDrug] = useState("Keytruda");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get<Watchlist[]>("/watchlist");
      setWatchlists(r);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.post<Watchlist>("/watchlist", {
        name,
        target_drug: drug,
        keywords: [drug],
        patent_ids: [],
      });
      setShowForm(false);
      await load();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to create");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Watchlists</h1>
          <p className="text-text-muted">Track competitor patents and detect infringement</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          New watchlist
        </Button>
      </div>

      {showForm && (
        <Card className="p-6">
          <form onSubmit={create} className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Name</label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Target drug</label>
              <Input value={drug} onChange={(e) => setDrug(e.target.value)} placeholder="e.g. Keytruda" />
            </div>
            {error && <div className="text-red-300 text-sm">{error}</div>}
            <div className="flex gap-2">
              <Button type="submit" disabled={creating}>
                {creating && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                Create
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
      ) : watchlists.length === 0 ? (
        <Card className="p-12 text-center">
          <Eye className="h-12 w-12 mx-auto mb-3 text-text-muted" />
          <p className="text-text-muted">No watchlists yet. Create one to start tracking competitor patents.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {watchlists.map((w) => <WatchlistCard key={w.id} watchlist={w} onChange={load} />)}
        </div>
      )}
    </div>
  );
}

function WatchlistCard({ watchlist, onChange }: { watchlist: Watchlist; onChange: () => void }) {
  const [scanning, setScanning] = useState(false);

  const scan = async () => {
    setScanning(true);
    try {
      await api.post(`/watchlist/${watchlist.id}/scan`, {});
      onChange();
    } finally {
      setScanning(false);
    }
  };

  return (
    <Card className="hover:border-accent/40 transition-all">
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">{watchlist.name}</CardTitle>
          <Badge variant={watchlist.active ? "success" : "secondary"}>
            {watchlist.active ? "Active" : "Paused"}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {watchlist.target_drug && (
          <div className="text-sm">
            <span className="text-text-muted">Drug:</span>{" "}
            <span className="font-medium">{watchlist.target_drug}</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-sm">
          <AlertTriangle className="h-4 w-4 text-amber-400" />
          <span>{watchlist.alert_count} alert{watchlist.alert_count !== 1 ? "s" : ""}</span>
        </div>
        <Button onClick={scan} disabled={scanning} size="sm" variant="outline" className="w-full">
          {scanning ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Eye className="h-4 w-4 mr-2" />}
          Scan now
        </Button>
      </CardContent>
    </Card>
  );
}
