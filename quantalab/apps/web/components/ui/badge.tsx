"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

type BadgeVariant = "default" | "outline" | "success" | "danger" | "warning" | "secondary";

const VARIANT_CLASS: Record<BadgeVariant, string> = {
  default: "bg-accent/20 text-accent border-accent/30",
  outline: "bg-transparent text-text-muted border-border",
  success: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  danger: "bg-red-500/20 text-red-300 border-red-500/30",
  warning: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  secondary: "bg-bg-elevated text-text-muted border-border",
};

export function Badge({
  variant = "default",
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & { variant?: BadgeVariant }) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded border text-xs font-medium",
        VARIANT_CLASS[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
