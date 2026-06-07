"use client";

export function Logo({ size = 32, withWordmark = true }: { size?: number; withWordmark?: boolean }) {
  return (
    <div className="flex items-center gap-2.5">
      <div
        className="rounded-lg bg-gradient-accent flex items-center justify-center shadow-lg shadow-accent/20"
        style={{ width: size, height: size }}
      >
        <svg viewBox="0 0 32 32" width={size * 0.7} height={size * 0.7} fill="none">
          {/* Peg target */}
          <circle cx="16" cy="16" r="11" stroke="white" strokeWidth="1.5" />
          <circle cx="16" cy="16" r="7" stroke="white" strokeWidth="1.5" />
          <circle cx="16" cy="16" r="3" fill="white" />
          {/* Pulse indicator */}
          <circle cx="16" cy="16" r="13" stroke="white" strokeWidth="1" strokeOpacity="0.4" />
          {/* Center crosshair */}
          <line x1="16" y1="2" x2="16" y2="6" stroke="white" strokeWidth="1.5" />
          <line x1="16" y1="26" x2="16" y2="30" stroke="white" strokeWidth="1.5" />
        </svg>
      </div>
      {withWordmark && (
        <span className="font-bold text-lg tracking-tight">
          Peg<span className="text-accent">Watch</span>
        </span>
      )}
    </div>
  );
}
