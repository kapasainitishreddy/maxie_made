"use client";
import { useEffect, useState } from "react";
import { api, MarketplaceStrategy } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Star, Download, ShoppingBag, Loader2 } from "lucide-react";

export default function Marketplace() {
  const [items, setItems] = useState<MarketplaceStrategy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<MarketplaceStrategy[]>("/marketplace").then(setItems).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="h-8 w-8 animate-spin text-accent" /></div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Marketplace</h1>
        <p className="text-text-muted">Buy and sell proven quant strategies</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((s) => (
          <Card key={s.id} className="hover:border-accent/40 transition-all">
            <CardHeader>
              <CardTitle className="text-lg">{s.name}</CardTitle>
              <div className="text-sm text-text-muted">by {s.author}</div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-text-muted mb-3 line-clamp-3">{s.description}</p>
              <div className="flex flex-wrap gap-1 mb-3">
                {s.tags.map((t) => <Badge key={t} variant="outline" className="text-xs">{t}</Badge>)}
              </div>
              <div className="flex items-center justify-between mb-3 text-sm">
                <div className="flex items-center gap-1"><Star className="h-3.5 w-3.5 text-amber-400" />{s.rating}</div>
                <div className="flex items-center gap-1 text-text-muted"><Download className="h-3.5 w-3.5" />{s.downloads.toLocaleString()}</div>
              </div>
              <div className="flex items-center justify-between">
                <div className="text-xl font-bold">{s.price_cents === 0 ? "Free" : `$${(s.price_cents / 100).toFixed(0)}`}</div>
                <Button size="sm">{s.price_cents === 0 ? "Get" : <><ShoppingBag className="h-3.5 w-3.5 mr-1" /> Buy</>}</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
