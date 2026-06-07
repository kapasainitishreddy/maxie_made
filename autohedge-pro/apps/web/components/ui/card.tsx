import * as React from "react";
import { cn } from "@/lib/utils";
const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-xl border border-border bg-bg-surface/60 backdrop-blur-md text-text shadow-lg", className)} {...props} />
));
export const CardHeader = (p: React.HTMLAttributes<HTMLDivElement>) => <div className={cn("flex flex-col space-y-1.5 p-6", p.className)} {...p} />;
export const CardContent = (p: React.HTMLAttributes<HTMLDivElement>) => <div className={cn("p-6 pt-0", p.className)} {...p} />;
export const CardTitle = (p: React.HTMLAttributes<HTMLHeadingElement>) => <h3 className={cn("text-lg font-semibold", p.className)} {...p} />;
Card.displayName = "Card";
export { Card };
