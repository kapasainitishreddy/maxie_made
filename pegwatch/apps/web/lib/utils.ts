import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatUSD(n: number, digits = 4): string {
  return `$${n.toFixed(digits)}`;
}

export function formatPct(n: number, digits = 3): string {
  const sign = n > 0 ? "+" : "";
  return `${sign}${n.toFixed(digits)}%`;
}

export function formatZ(z: number, digits = 2): string {
  const sign = z > 0 ? "+" : "";
  return `${sign}${z.toFixed(digits)}`;
}

export function formatUSDshort(n: number): string {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(1)}K`;
  return `$${n.toFixed(0)}`;
}

export function severityColor(sev: string): string {
  switch (sev) {
    case "critical": return "text-crit border-crit/30 bg-crit/10";
    case "warning": return "text-warn border-warn/30 bg-warn/10";
    case "watch": return "text-yellow-400 border-yellow-400/30 bg-yellow-400/10";
    default: return "text-ok border-ok/30 bg-ok/10";
  }
}

export function severityDot(sev: string): string {
  switch (sev) {
    case "critical": return "bg-crit animate-pulse";
    case "warning": return "bg-warn";
    case "watch": return "bg-yellow-400";
    default: return "bg-ok";
  }
}
