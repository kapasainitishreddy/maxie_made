const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/proxy";

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) { super(message); }
}

async function request<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
  });
  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    throw new ApiError(r.status, body.code || "error", body.message || r.statusText);
  }
  return r.json();
}

export const api = {
  get: <T,>(path: string) => request<T>(path),
  post: <T,>(path: string, body?: any) => request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
  patch: <T,>(path: string, body?: any) => request<T>(path, { method: "PATCH", body: body ? JSON.stringify(body) : undefined }),
  del: <T,>(path: string) => request<T>(path, { method: "DELETE" }),
};

export interface CloudAccount {
  id: string; provider: string; account_id: string; account_name: string;
  region: string; monthly_cost: number; resource_count: number; active: boolean;
}
export interface Recommendation {
  id: string; account_id: string; resource_id: string; resource_type: string;
  rec_type: string; title: string; description: string; current_cost: number;
  projected_cost: number; monthly_savings: number; risk: string; status: string;
  terraform_hcl: string; evidence: Record<string, any>;
}
