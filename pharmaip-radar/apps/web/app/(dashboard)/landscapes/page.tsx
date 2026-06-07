"use client";

import { useEffect, useState } from "react";
import { api, LandscapeSummary, ApiError } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Map as MapIcon, Plus, Loader2 } from "lucide-react";

export default function LandscapesPage() {
  const [landscapes, setLandscapes] = useState<LandscapeSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("PD-1 inhibitor landscape");
  const [area, setArea] = useState("Oncology");
  const [drug, setDrug] = useState("pembrolizumab");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get<LandscapeSummary[]>("/landscapes");
      setLandscapes(r);
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
      await api.post<LandscapeSummary>("/landscapes", {
        name,
        therapeutic_area: area,
        drug_name: drug,
        keywords: [drug],
        query: {},
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
          <h1 className="text-3xl font-bold mb-2">IP Landscapes</h1>
          <p className="text-text-muted">Visualize patent density and competitive positioning</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          New landscape
        </Button>
      </div>

      {showForm && (
        <Card className="p-6">
          <form onSubmit={create} className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Name</label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-1.5 block">Therapeutic area</label>
                <Input value={area} onChange={(e) => setArea(e.target.value)} />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Drug</label>
                <Input value={drug} onChange={(e) => setDrug(e.target.value)} />
              </div>
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
      ) : landscapes.length === 0 ? (
        <Card className="p-12 text-center">
          <MapIcon className="h-12 w-12 mx-auto mb-3 text-text-muted" />
          <p className="text-text-muted">No landscapes yet. Create your first to visualize the field.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {landscapes.map((l) => (
            <Card key={l.id} className="hover:border-accent/40 transition-all cursor-pointer">
              <CardHeader>
                <CardTitle className="text-lg">{l.name}</CardTitle>
                <CardDescription>{l.description || "—"}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-text-muted">
                  {l.patent_count} patents · {l.status}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
