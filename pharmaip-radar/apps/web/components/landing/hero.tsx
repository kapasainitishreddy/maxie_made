"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, FileSearch, AlertTriangle, BarChart3, Lock, Sparkles, Building2 } from "lucide-react";
import { Hero3D } from "./hero3d";

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10 bg-gradient-radial" />
      <div className="absolute inset-0 -z-10 bg-[linear-gradient(rgba(99,102,241,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.05)_1px,transparent_1px)] bg-[size:60px_60px]" />

      <div className="container mx-auto px-4 pt-20 pb-24 md:pt-32 md:pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: copy */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="text-left"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-accent/30 bg-accent/5 text-sm">
              <Sparkles className="h-3.5 w-3.5 text-accent" />
              <span className="text-text-muted">Trusted by 30+ pharma IP teams</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
              The <span className="text-gradient">pharma IP radar</span><br />
              your legal team needs.
            </h1>

            <p className="text-xl md:text-2xl text-text-muted mb-10 leading-relaxed">
              Scan 100M+ global patents, detect infringement in minutes, and generate investor-grade FTO reports — all from a single terminal.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button asChild size="lg" className="text-base">
                <Link href="/sign-up">
                  Start free trial
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/pricing">View pricing</Link>
              </Button>
            </div>

            <p className="mt-6 text-sm text-text-muted">
              No credit card. 14-day trial. $0 to launch.
            </p>
          </motion.div>

          {/* Right: 3D */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Hero3D />
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function StatCard({ label, value, trend }: { label: string; value: string; trend: string }) {
  return (
    <div className="rounded-lg bg-bg-elevated border border-border p-4">
      <div className="text-xs text-text-muted mb-1">{label}</div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs text-emerald-400 mt-1">{trend} this month</div>
    </div>
  );
}
