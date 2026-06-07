"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export function Cta() {
  return (
    <section className="py-20">
      <div className="max-w-4xl mx-auto px-6">
        <div className="rounded-2xl glass-elevated p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-accent/10 to-transparent" />
          <div className="relative">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              The next USDC depeg is coming.
            </h2>
            <p className="text-text-muted mb-8 max-w-xl mx-auto">
              Be the one who knew about it 47 minutes before Twitter did. Free
              for 3 stables, no credit card.
            </p>
            <div className="flex flex-wrap gap-3 justify-center">
              <Link href="/dashboard">
                <Button size="lg" className="gap-2">
                  Open live monitor <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
              <Link href="/pricing">
                <Button size="lg" variant="outline">View pricing</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
