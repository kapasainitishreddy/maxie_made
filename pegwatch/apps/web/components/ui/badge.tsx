import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

type Variant = "default" | "success" | "warning" | "critical" | "info";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: Variant;
}

const variantClasses: Record<Variant, string> = {
  default: "bg-bg-elevated text-text-muted border-border",
  success: "bg-ok/10 text-ok border-ok/30",
  warning: "bg-warn/10 text-warn border-warn/30",
  critical: "bg-crit/10 text-crit border-crit/30",
  info: "bg-accent/10 text-accent border-accent/30",
};

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border",
        variantClasses[variant],
        className
      )}
      {...props}
    />
  );
}
