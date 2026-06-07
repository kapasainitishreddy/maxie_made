import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";
import { Plausible } from "@/components/analytics/plausible";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "PharmaIP Radar — Pharmaceutical IP & Patent Intelligence",
  description:
    "Scan 100M+ global patents, detect infringement, and generate FTO reports in minutes. Built for pharma IP attorneys.",
  metadataBase: new URL("https://pharmaip-radar.com"),
  openGraph: {
    title: "PharmaIP Radar",
    description: "Pharmaceutical IP & patent intelligence platform",
    type: "website",
  },
};

const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const body = (
    <html lang="en" className={`${inter.variable} dark`}>
      <body className="min-h-screen bg-bg text-text antialiased">
        {children}
              <Plausible />
      </body>
    </html>
  );
  // Only wrap with ClerkProvider if Clerk key is set. Otherwise render raw.
  return clerkKey ? <ClerkProvider>{body}</ClerkProvider> : body;
}
