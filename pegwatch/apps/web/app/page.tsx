import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Hero } from "@/components/landing/hero";
import { Features } from "@/components/landing/features";
import { HowItWorks } from "@/components/landing/how";
import { Scenario } from "@/components/landing/scenario";
import { Cta } from "@/components/landing/cta";

export default function HomePage() {
  return (
    <>
      <Topnav />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <Scenario />
        <Cta />
      </main>
      <LegalFooter />
    </>
  );
}
