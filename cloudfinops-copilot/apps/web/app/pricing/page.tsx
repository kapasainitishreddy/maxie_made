import { TopNav } from "@/components/layout/topnav";
import { Pricing } from "@/components/landing/pricing";

export default function PricingPage() {
  return (
    <>
      <TopNav />
      <main>
        <Pricing />
      </main>
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-text-muted">
          © 2026 CloudFinOps Co-Pilot
        </div>
      </footer>
    </>
  );
}
