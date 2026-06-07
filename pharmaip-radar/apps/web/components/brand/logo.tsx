// Custom SVG logos for all 4 apps — distinctive, no generic icons
// Each logo is a 32x32 inline SVG that scales to any size.

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
        {/* Radar sweep + molecule */}
        <svg
          viewBox="0 0 32 32"
          width={size * 0.65}
          height={size * 0.65}
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Outer radar rings */}
          <circle cx="16" cy="16" r="13" stroke="white" strokeOpacity="0.35" strokeWidth="1" />
          <circle cx="16" cy="16" r="8" stroke="white" strokeOpacity="0.55" strokeWidth="1" />
          <circle cx="16" cy="16" r="3" stroke="white" strokeWidth="1.2" />
          {/* Radar sweep wedge */}
          <path d="M16 16 L29 16 A13 13 0 0 0 22 4 Z" fill="white" fillOpacity="0.3" />
          {/* Patent blip */}
          <circle cx="24" cy="9" r="1.6" fill="white" />
          <circle cx="9" cy="22" r="1.2" fill="white" fillOpacity="0.7" />
        </svg>
      </div>
      {withWordmark && (
        <span className="font-bold text-lg tracking-tight">PharmaIP Radar</span>
      )}
    </div>
  );
}
