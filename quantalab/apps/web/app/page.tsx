import { TopNav } from "@/components/layout/topnav";
import { Hero } from "@/components/landing/hero";
import { Features } from "@/components/landing/features";
import { HowItWorks } from "@/components/landing/how";
import { Scenario } from "@/components/landing/scenario";

export default function Home() {
  return (
    <>
      <TopNav />
      <main>
        <Hero />
        <div id="features"><Features /></div>
        <div id="how"><HowItWorks /></div>
        <Scenario />
      </main>
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-text-muted">
          © 2026 QuantaLab
        </div>
      </footer>
    </>
  );
}
