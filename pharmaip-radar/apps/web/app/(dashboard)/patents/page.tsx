"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, Patent, PatentSearchResult, ApiError } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Search, Loader2 } from "lucide-react";

export default function PatentsPage() {
  const [q, setQ] = useState("");
  const [data, setData] = useState<PatentSearchResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const search = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get<PatentSearchResult>(
        `/patents?q=${encodeURIComponent(query)}&page_size=50`
      );
      setData(r);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to search");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    search("");
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Patents</h1>
        <p className="text-text-muted">Search 100M+ global patents</p>
      </div>

      <Card className="p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            search(q);
          }}
          className="flex gap-2"
        >
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
            <Input
              placeholder="Search by drug name, company, IPC class..."
              value={q}
              onChange={(e) => setQ(e.target.value)}
              className="pl-9"
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Search"}
          </Button>
        </form>
      </Card>

      {error && (
        <Card className="border-red-500/50 bg-red-500/5 p-4 text-red-300">{error}</Card>
      )}

      {data && (
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Patent #</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Assignee</TableHead>
                <TableHead>Drug</TableHead>
                <TableHead>Area</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Filed</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.patents.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} className="text-center py-12 text-text-muted">
                    No patents found. Try a different query.
                  </TableCell>
                </TableRow>
              ) : (
                data.patents.map((p) => <PatentRow key={p.id} patent={p} />)
              )}
            </TableBody>
          </Table>
        </Card>
      )}
    </div>
  );
}

function PatentRow({ patent }: { patent: Patent }) {
  return (
    <TableRow>
      <TableCell className="font-mono text-xs">{patent.patent_number}</TableCell>
      <TableCell className="max-w-md">
        <Link href={`/patents/${patent.id}`} className="hover:text-accent line-clamp-1">
          {patent.title}
        </Link>
      </TableCell>
      <TableCell className="text-sm">{patent.assignee || "—"}</TableCell>
      <TableCell className="text-sm">{patent.drug_name || "—"}</TableCell>
      <TableCell>
        {patent.therapeutic_area && (
          <Badge variant="secondary">{patent.therapeutic_area}</Badge>
        )}
      </TableCell>
      <TableCell>
        <Badge variant={patent.status === "granted" ? "success" : "warning"}>
          {patent.status}
        </Badge>
      </TableCell>
      <TableCell className="text-sm text-text-muted">
        {patent.filing_date || "—"}
      </TableCell>
    </TableRow>
  );
}
