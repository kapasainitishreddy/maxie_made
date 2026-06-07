"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Hero3D } from "./hero3d";
import { ArrowRight, Check } from "lucide-react";

export function Hero() {
  return (
    <section className="relative pt-20 pb-12 overflow-hidden">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: copy */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass mb-6 text-sm">
              <span className="w-2 h-2 rounded-full bg-ok animate-pulse" />
              <span className="text-text-muted">Now monitoring 8 stables · $150B aggregate</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold leading-[1.1] tracking-tight mb-6">
              Hear about USDC at{" "}
              <span className="gradient-text">$0.9982</span>
              <br />
              <span className="text-text-muted">before it hits $0.99.</span>
            </h1>
            <p className="text-lg text-text-muted mb-8 max-w-xl">
              Statistical stablecoin depeg early-warning. Z-score based alerts from
              Curve, Uniswap, and 5+ CEXs. Built so your treasury, market making,
              or LP position isn't the bag-holder when the next stable breaks.
            </p>
            <div className="flex flex-wrap gap-3 mb-8">
              <Link href="/dashboard">
                <Button size="lg" className="gap-2">
                  Open live monitor <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
              <Link href="/pricing">
                <Button size="lg" variant="outline">See pricing</Button>
              </Link>
            </div>
            <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-text-muted">
              <span className="flex items-center gap-1.5"><Check className="w-4 h-4 text-ok" /> No credit card</span>
              <span className="flex items-center gap-1.5"><Check className="w-4 h-4 text-ok" /> Free for 3 stables</span>
              <span className="flex items-center gap-1.5"><Check className="w-4 h-4 text-ok" /> Open source</span>
            </div>
          </div>

          {/* Right: 3D hero */}
          <div className="hidden lg:block">
            <Hero3D />
          </div>
        </div>
      </div>
    </section>
  );
}
