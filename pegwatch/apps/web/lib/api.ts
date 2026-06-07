/** Typed API client for the PegWatch backend. */
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8004";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function fetchJSON<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined),
  };
  // Dev auth header (backend accepts "Bearer dev:<user>:<plan>" when no Clerk key set)
  if (!headers["Authorization"] && typeof window !== "undefined") {
    const plan = window.localStorage?.getItem("pegwatch_plan") || "pro";
    const user = window.localStorage?.getItem("pegwatch_user") || "demo-user";
    headers["Authorization"] = `Bearer dev:${user}:${plan}`;
  }
  const r = await fetch(`${API_BASE}${path}`, { ...init, headers, cache: "no-store" });
  if (!r.ok) {
    let body: any = {};
    try { body = await r.json(); } catch {}
    throw new ApiError(r.status, body.detail || `HTTP ${r.status}`);
  }
  return r.json() as Promise<T>;
}

// ----- Types -----
export interface Stablecoin {
  id: string;
  symbol: string;
  name: string;
  issuer: string;
  category: string;
  peg_currency: string;
  chain: string;
  contract_address: string | null;
  market_cap_usd: number;
  circulating_supply: number;
  is_active: boolean;
  tier: number;
}

export interface PegStatus {
  symbol: string;
  name: string;
  issuer: string;
  price_usd: number;
  deviation_pct: number;
  z_score: number;
  liquidity_depth_usd: number;
  severity: "healthy" | "watch" | "warning" | "critical";
  last_updated: string;
  market_cap_usd: number;
  sources_count: number;
}

export interface PegHistoryPoint {
  observed_at: string;
  price_usd: number;
  deviation_pct: number;
  z_score: number;
}

export interface PegHistory {
  symbol: string;
  points: PegHistoryPoint[];
  mean_7d: number;
  stddev_7d: number;
}

export interface Alert {
  id: string;
  stablecoin_id: string;
  triggered_at: string;
  severity: string;
  price_at_trigger: number;
  deviation_pct: number;
  z_score: number;
  title: string;
  summary: string | null;
  ai_summary: string | null;
  resolved: boolean;
  notification_count: number;
}

export interface Plan {
  id: string;
  name: string;
  price_usd: number;
  max_stablecoins: number;
  alerts: boolean;
  api_access: boolean;
  features: string[];
}

// ----- Endpoints -----
export const api = {
  health: () => fetchJSON<{ status: string; version: string; environment: string; db: string }>("/health"),
  listStablecoins: (tier?: number) =>
    fetchJSON<Stablecoin[]>(`/api/v1/stablecoins${tier ? `?tier=${tier}` : ""}`),
  getStablecoin: (symbol: string) => fetchJSON<Stablecoin>(`/api/v1/stablecoins/${symbol}`),
  allStatus: () => fetchJSON<PegStatus[]>("/api/v1/peg/status"),
  status: (symbol: string) => fetchJSON<PegStatus>(`/api/v1/peg/${symbol}/status`),
  history: (symbol: string, hours = 168) =>
    fetchJSON<PegHistory>(`/api/v1/peg/${symbol}/history?hours=${hours}`),
  refresh: (symbol: string) =>
    fetchJSON<PegStatus>(`/api/v1/peg/${symbol}/refresh`, { method: "POST" }),
  listAlerts: () => fetchJSON<Alert[]>("/api/v1/alerts"),
  plans: () => fetchJSON<Plan[]>("/api/v1/billing/plans"),
  checkout: (plan: "pro" | "api") =>
    fetchJSON<{ url: string; session_id: string; dev_mode: boolean }>(
      "/api/v1/billing/checkout",
      { method: "POST", body: JSON.stringify({ plan }) }
    ),
  portal: () =>
    fetchJSON<{ url: string; dev_mode: boolean }>("/api/v1/billing/portal", {
      method: "POST",
    }),
};
