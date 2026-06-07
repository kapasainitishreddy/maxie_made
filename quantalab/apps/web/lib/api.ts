const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/proxy";
export class ApiError extends Error { constructor(public status: number, public code: string, message: string) { super(message); } }
async function req<T>(p: string, o: RequestInit = {}): Promise<T> {
  const r = await fetch(`${API_BASE}${p}`, { ...o, headers: { "Content-Type": "application/json", ...(o.headers || {}) } });
  if (!r.ok) { const b = await r.json().catch(() => ({})); throw new ApiError(r.status, b.code || "error", b.message || r.statusText); }
  return r.json();
}
export const api = { get: <T,>(p: string) => req<T>(p), post: <T,>(p: string, b?: any) => req<T>(p, { method: "POST", body: b ? JSON.stringify(b) : undefined }) };
export interface MarketplaceStrategy { id: string; name: string; author: string; description: string; price_cents: number; downloads: number; rating: number; tags: string[]; }
export interface BacktestResult { final_value: number; total_return: number; sharpe: number; sortino: number; max_drawdown: number; num_trades: number; equity_curve: any[]; code?: string; error?: string; }
