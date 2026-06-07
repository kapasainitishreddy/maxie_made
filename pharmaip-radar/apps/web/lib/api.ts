/**
 * API client for the FastAPI backend.
 * Goes through the Next.js rewrite proxy in dev (configured in next.config.mjs).
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/proxy";

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

async function request<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      ...(opts.headers || {}),
    },
  });
  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    throw new ApiError(r.status, body.code || "error", body.message || r.statusText);
  }
  return r.json();
}

export const api = {
  get: <T,>(path: string) => request<T>(path),
  post: <T,>(path: string, body?: any) =>
    request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
  patch: <T,>(path: string, body?: any) =>
    request<T>(path, { method: "PATCH", body: body ? JSON.stringify(body) : undefined }),
  del: <T,>(path: string) => request<T>(path, { method: "DELETE" }),
};

// Typed API
export interface Patent {
  id: string;
  patent_number: string;
  jurisdiction: string;
  title: string;
  abstract?: string;
  assignee?: string;
  drug_name?: string;
  therapeutic_area?: string;
  status: string;
  filing_date?: string;
  grant_date?: string;
  expiration_date?: string;
  inventors?: string[];
  ipc_classes?: string[];
}

export interface PatentSearchResult {
  patents: Patent[];
  total: number;
  page: number;
  page_size: number;
}

export interface LandscapeSummary {
  id: string;
  name: string;
  description?: string;
  status: string;
  patent_count: number;
  created_at: string;
}

export interface Watchlist {
  id: string;
  name: string;
  description?: string;
  target_company?: string;
  target_drug?: string;
  keywords: string[];
  patent_ids: string[];
  active: boolean;
  alert_count: number;
  created_at: string;
}

export interface InfringementAlert {
  id: string;
  watchlist_id: string;
  patent_id: string;
  matched_patent_id: string;
  severity: "low" | "medium" | "high" | "critical";
  status: string;
  risk_score: number;
  summary?: string;
  claim_chart: any[];
  evidence: Record<string, any>;
  created_at: string;
}

export type ReportType = "fto" | "landscape" | "infringement" | "patentability";

export interface Report {
  id: string;
  report_type: ReportType;
  title: string;
  status: "queued" | "generating" | "ready" | "failed";
  query: Record<string, any>;
  content: Record<string, any>;
  pdf_path?: string;
  error?: string;
  created_at: string;
}
