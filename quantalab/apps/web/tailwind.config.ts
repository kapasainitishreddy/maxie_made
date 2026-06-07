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
        accent: { DEFAULT: "#8b5cf6", 400: "#a78bfa", 500: "#8b5cf6", 600: "#7c3aed" },
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], mono: ["JetBrains Mono", "monospace"] },
      backgroundImage: {
        "gradient-accent": "linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%)",
        "gradient-radial": "radial-gradient(circle at 50% 0%, rgba(139,92,246,0.15) 0%, transparent 50%)",
      },
      animation: { "fade-in": "fadeIn 0.5s ease-in-out" },
      keyframes: { fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } } },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
