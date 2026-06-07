import { cn } from "@/lib/utils";

type LogoProps = {
  size?: number;
  className?: string;
  withWordmark?: boolean;
};

export function Logo({ size = 32, className, withWordmark = true }: LogoProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <div
        className="relative shrink-0 rounded-lg bg-gradient-accent flex items-center justify-center"
        style={{ width: size, height: size }}
      >
        <svg
          viewBox="0 0 32 32"
          width={size * 0.7}
          height={size * 0.7}
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Candlesticks */}
          <line x1="7" y1="6" x2="7" y2="26" stroke="white" strokeOpacity="0.4" strokeWidth="1" />
          <rect x="5" y="14" width="4" height="8" fill="white" fillOpacity="0.6" />
          <line x1="16" y1="6" x2="16" y2="26" stroke="white" strokeOpacity="0.4" strokeWidth="1" />
          <rect x="14" y="10" width="4" height="14" fill="white" />
          <line x1="25" y1="6" x2="25" y2="26" stroke="white" strokeOpacity="0.4" strokeWidth="1" />
          <rect x="23" y="17" width="4" height="6" fill="white" fillOpacity="0.6" />
          {/* Up arrow overlay */}
          <path
            d="M3 28 L29 4 M22 4 L29 4 L29 11"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      {withWordmark && (
        <span className="font-bold text-lg tracking-tight">AutoHedge Pro</span>
      )}
    </div>
  );
}
