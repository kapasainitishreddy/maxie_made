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
        accent: { DEFAULT: "#10b981", 400: "#34d399", 500: "#10b981", 600: "#059669" },
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], mono: ["JetBrains Mono", "monospace"] },
      backgroundImage: {
        "gradient-accent": "linear-gradient(135deg, #10b981 0%, #06b6d4 100%)",
        "gradient-radial": "radial-gradient(circle at 50% 0%, rgba(16,185,129,0.15) 0%, transparent 50%)",
      },
      animation: { "fade-in": "fadeIn 0.5s ease-in-out", "slide-up": "slideUp 0.5s ease-out" },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: { "0%": { opacity: "0", transform: "translateY(20px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
