import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PegWatch — Stablecoin Depeg Early-Warning",
  description:
    "Real-time stablecoin depeg monitor. Statistical early-warning before USDC, USDT, or DAI breaks its peg. Free for 3 stables, $19/mo Pro.",
  keywords: [
    "stablecoin",
    "depeg",
    "USDC",
    "USDT",
    "DAI",
    "FRAX",
    "crypto risk",
    "treasury management",
    "stablecoin monitoring",
  ],
  authors: [{ name: "PegWatch" }],
  openGraph: {
    title: "PegWatch — Stablecoin Depeg Early-Warning",
    description: "Hear about USDC at $0.9982 BEFORE it hits $0.99.",
    type: "website",
    url: "https://pegwatch.dev",
  },
  twitter: {
    card: "summary_large_image",
    title: "PegWatch — Stablecoin Depeg Early-Warning",
    description: "Real-time statistical depeg detection. Free tier, no signup.",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg text-text antialiased min-h-screen">
        <div className="grid-bg fixed inset-0 pointer-events-none opacity-30" />
        <div className="relative">{children}</div>
      </body>
    </html>
  );
}
