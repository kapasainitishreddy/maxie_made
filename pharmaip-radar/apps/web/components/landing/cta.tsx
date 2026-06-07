import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export function CTA() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto glass-elevated rounded-2xl p-12 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Ready to ship a better IP workflow?
          </h2>
          <p className="text-xl text-text-muted mb-8 max-w-2xl mx-auto">
            Join 30+ pharma IP teams already using PharmaIP Radar. Free 14-day trial. No card required.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg">
              <Link href="/sign-up">
                Get started free
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/pricing">Compare plans</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
