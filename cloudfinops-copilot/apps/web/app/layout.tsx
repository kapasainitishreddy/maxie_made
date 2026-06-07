import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";
import { Plausible } from "@/components/analytics/plausible";

const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = { title: "CloudFinOps Co-Pilot", description: "Auto-find and fix cloud cost waste." };
const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const body = <html lang="en" className={`${inter.className} dark`}><body className="min-h-screen bg-bg text-text antialiased">{children}        <Plausible />
      </body></html>;
  return clerkKey ? <ClerkProvider>{body}</ClerkProvider> : body;
}
