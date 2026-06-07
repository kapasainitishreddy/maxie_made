import type { Config } from "tailwindcss";
const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: { DEFAULT: "#0a0a0f", surface: "#13131a", elevated: "#1a1a24" },
        border: { DEFAULT: "#2a2a3a" },
        text: { DEFAULT: "#f5f5f7", muted: "#9ca3af" },
        accent: { DEFAULT: "#f59e0b", 400: "#fbbf24", 500: "#f59e0b", 600: "#d97706" },
        gain: "#10b981", loss: "#ef4444",
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], mono: ["JetBrains Mono", "monospace"] },
      backgroundImage: {
        "gradient-accent": "linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)",
        "gradient-radial": "radial-gradient(circle at 50% 0%, rgba(245,158,11,0.15) 0%, transparent 50%)",
      },
      animation: { "fade-in": "fadeIn 0.5s ease-in-out" },
      keyframes: { fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } } },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
