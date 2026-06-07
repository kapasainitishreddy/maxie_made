import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: { DEFAULT: "#0a0a0f", surface: "#13131a", elevated: "#1a1a24" },
        border: { DEFAULT: "#2a2a3a" },
        text: { DEFAULT: "#f5f5f7", muted: "#9ca3af" },
        accent: {
          DEFAULT: "#10b981",  // emerald - "stable" / "money" / "trust"
          dark: "#059669",
        },
        warn: { DEFAULT: "#f59e0b" },
        crit: { DEFAULT: "#ef4444" },
        ok: { DEFAULT: "#10b981" },
      },
      backgroundImage: {
        "gradient-accent": "linear-gradient(135deg, #10b981 0%, #34d399 100%)",
        "gradient-warn": "linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)",
        "gradient-crit": "linear-gradient(135deg, #ef4444 0%, #f87171 100%)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "breathe": "breathe 4s ease-in-out infinite",
      },
      keyframes: {
        breathe: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-8px)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
