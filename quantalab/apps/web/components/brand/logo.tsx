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
          {/* Atom nucleus */}
          <circle cx="16" cy="16" r="2.5" fill="white" />
          {/* Three orbital ellipses */}
          <ellipse cx="16" cy="16" rx="13" ry="5" stroke="white" strokeWidth="1.2" />
          <ellipse cx="16" cy="16" rx="13" ry="5" stroke="white" strokeWidth="1.2" transform="rotate(60 16 16)" />
          <ellipse cx="16" cy="16" rx="13" ry="5" stroke="white" strokeWidth="1.2" transform="rotate(-60 16 16)" />
          {/* Electrons */}
          <circle cx="29" cy="16" r="1.5" fill="white" />
          <circle cx="9.5" cy="22" r="1.5" fill="white" />
          <circle cx="9.5" cy="10" r="1.5" fill="white" />
        </svg>
      </div>
      {withWordmark && (
        <span className="font-bold text-lg tracking-tight">QuantaLab</span>
      )}
    </div>
  );
}
