"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ExternalLink, Loader2 } from "lucide-react";

interface ManageSubscriptionButtonProps {
  className?: string;
  variant?: "default" | "outline" | "secondary" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  children?: React.ReactNode;
}

/**
 * Opens Stripe customer portal (or demo URL in dev-bypass mode).
 * Customer can update card, change plan, cancel, download invoices.
 */
export function ManageSubscriptionButton({
  className,
  variant = "outline",
  size = "default",
  children = "Manage subscription",
}: ManageSubscriptionButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);
    try {
      // In dev, go through Next.js proxy at /api/proxy/* (rewrites to backend).
      // In prod, NEXT_PUBLIC_API_URL points directly at Fly.io and we bypass the proxy.
      const API_BASE = process.env.NEXT_PUBLIC_API_URL
        ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
        : "/api/proxy";
      const r = await fetch(`${API_BASE}/billing/portal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (!r.ok) {
        const body = await r.json().catch(() => ({}));
        throw new Error(body.detail || body.error || `HTTP ${r.status}`);
      }
      const data = await r.json();
      window.location.href = data.url;
    } catch (e: any) {
      setError(e?.message || "Failed to open billing portal");
      setLoading(false);
    }
  };

  return (
    <div className={className}>
      <Button onClick={handleClick} disabled={loading} variant={variant} size={size}>
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Opening...
          </>
        ) : (
          <>
            <ExternalLink className="mr-2 h-4 w-4" />
            {children}
          </>
        )}
      </Button>
      {error && <p className="mt-2 text-xs text-red-400">{error}</p>}
    </div>
  );
}
