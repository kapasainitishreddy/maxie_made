"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, Patent as PatentType, ApiError } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

interface PatentDetail extends PatentType {
  abstract?: string;
  inventors?: string[];
  ipc_classes?: string[];
  expiration_date?: string;
}

export default function PatentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [patent, setPatent] = useState<PatentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    (async () => {
      try {
        const p = await api.get<PatentDetail>(`/patents/${id}`);
        setPatent(p);
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <Skeleton className="h-96" />;
  if (error) return <Card className="p-6 text-red-300">{error}</Card>;
  if (!patent) return null;

  return (
    <div className="space-y-6 animate-fade-in">
      <Button asChild variant="ghost" size="sm">
        <Link href="/patents">
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to patents
        </Link>
      </Button>

      <div>
        <div className="flex items-center gap-2 mb-3">
          <span className="font-mono text-sm text-text-muted">{patent.patent_number}</span>
          <span className="text-text-muted">·</span>
          <Badge variant="secondary">{patent.jurisdiction}</Badge>
          <Badge variant={patent.status === "granted" ? "success" : "warning"}>
            {patent.status}
          </Badge>
        </div>
        <h1 className="text-3xl font-bold mb-3">{patent.title}</h1>
        {patent.abstract && (
          <p className="text-text-muted leading-relaxed">{patent.abstract}</p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Assignee</CardTitle>
          </CardHeader>
          <CardContent>{patent.assignee || "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Drug</CardTitle>
          </CardHeader>
          <CardContent>{patent.drug_name || "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Therapeutic area</CardTitle>
          </CardHeader>
          <CardContent>{patent.therapeutic_area || "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Filed</CardTitle>
          </CardHeader>
          <CardContent>{patent.filing_date || "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Granted</CardTitle>
          </CardHeader>
          <CardContent>{patent.grant_date || "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Expires</CardTitle>
          </CardHeader>
          <CardContent>{patent.expiration_date || "—"}</CardContent>
        </Card>
      </div>

      {patent.inventors && patent.inventors.length > 0 && (
        <Card className="p-6">
          <h3 className="font-semibold mb-2">Inventors</h3>
          <div className="text-sm text-text-muted">{patent.inventors.join(", ")}</div>
        </Card>
      )}

      {patent.ipc_classes && patent.ipc_classes.length > 0 && (
        <Card className="p-6">
          <h3 className="font-semibold mb-2">IPC classes</h3>
          <div className="flex flex-wrap gap-2">
            {patent.ipc_classes.map((ipc) => (
              <Badge key={ipc} variant="outline">{ipc}</Badge>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
