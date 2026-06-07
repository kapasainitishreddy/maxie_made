import Link from "next/link";
import { Button } from "@/components/ui/button";
import { TopNav } from "@/components/layout/topnav";
import { Pricing } from "@/components/landing/pricing";
import { CTA } from "@/components/landing/cta";

export default function PricingPage() {
  return (
    <>
      <TopNav />
      <main>
        <Pricing />
        <CTA />
      </main>
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-text-muted">
          © 2026 PharmaIP Radar
        </div>
      </footer>
    </>
  );
}
