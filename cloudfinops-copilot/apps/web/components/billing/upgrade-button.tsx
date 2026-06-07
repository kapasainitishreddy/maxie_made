"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

interface UpgradeButtonProps {
  plan: string;
  className?: string;
  variant?: "default" | "outline" | "secondary" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  children?: React.ReactNode;
}

/**
 * Generic upgrade button: calls /billing/checkout, redirects to Stripe session URL.
 * In dev-bypass mode (no STRIPE_SECRET_KEY on backend), the API returns a demo URL
 * that the backend's app code handles (or we just navigate to /pricing?demo=1).
 */
export function UpgradeButton({
  plan,
  className,
  variant = "default",
  size = "default",
  children = "Start free trial",
}: UpgradeButtonProps) {
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
      const r = await fetch(`${API_BASE}/billing/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan }),
      });
      if (!r.ok) {
        const body = await r.json().catch(() => ({}));
        throw new Error(body.detail || body.error || `HTTP ${r.status}`);
      }
      const data = await r.json();
      // data.url is either a real Stripe checkout URL or a dev-bypass URL
      window.location.href = data.url;
    } catch (e: any) {
      setError(e?.message || "Checkout failed");
      setLoading(false);
    }
  };

  return (
    <div className={className}>
      <Button
        onClick={handleClick}
        disabled={loading}
        variant={variant}
        size={size}
        className="w-full"
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Redirecting...
          </>
        ) : (
          children
        )}
      </Button>
      {error && (
        <p className="mt-2 text-xs text-red-400 text-center">{error}</p>
      )}
    </div>
  );
}
