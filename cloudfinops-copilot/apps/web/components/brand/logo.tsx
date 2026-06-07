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
          {/* Cloud outline */}
          <path
            d="M9 22 Q4 22 4 17 Q4 13 8 12 Q9 7 14 7 Q19 7 20 12 Q24 11 27 15 Q30 18 27 22 Z"
            stroke="white"
            strokeWidth="1.5"
            fill="white"
            fillOpacity="0.15"
          />
          {/* Down arrow (cost going down) */}
          <path
            d="M16 14 L16 21 M12.5 17.5 L16 21 L19.5 17.5"
            stroke="white"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          {/* Dollar sign dot */}
          <circle cx="16" cy="13" r="1.2" fill="white" />
        </svg>
      </div>
      {withWordmark && (
        <span className="font-bold text-lg tracking-tight">CloudFinOps</span>
      )}
    </div>
  );
}
