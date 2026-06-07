"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Hero3D } from "./hero3d";
import { MagneticButton, FloatingBadge, Counter, Typewriter, ScrollReveal } from "@/components/fx/motion";
import { ArrowRight, Cloud, TrendingDown, Shield, Zap, Bot } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden aurora-bg noise">
      <div className="absolute inset-0 -z-10 grid-bg mask-radial" />

      <div className="absolute top-1/3 right-1/4 -z-10 h-72 w-72 rounded-full bg-emerald-500/20 blur-[120px] float" />
      <div className="absolute bottom-1/3 left-1/4 -z-10 h-96 w-96 rounded-full bg-cyan-500/15 blur-[120px] float-delayed" />

      <div className="container mx-auto px-4 pt-24 pb-24 md:pt-32 md:pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div className="relative z-10">
            <FloatingBadge>
              <div className="inline-flex items-center gap-2 rounded-full glass px-4 py-1.5 text-xs font-medium text-text-muted">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
                </span>
                Live · 38 verified savings opportunities today
              </div>
            </FloatingBadge>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="mt-8 text-5xl md:text-7xl font-bold tracking-tight text-balance"
            >
              Cut your cloud bill by <span className="gradient-text">20%</span>. We get paid after.
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="mt-6 text-lg md:text-xl text-text-muted max-w-xl text-balance"
            >
              We scan your AWS, GCP, and Azure usage 24/7. When we find verified savings, we send you a Terraform PR.
              <span className="block mt-1">You approve. We take 20%. <Typewriter words={["No savings, no fee.", "Zero risk.", "Pure upside."]} className="text-text" /></span>
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.3 }}
              className="mt-10 flex flex-wrap items-center gap-4"
            >
              <MagneticButton
                strength={0.25}
                className="group relative inline-flex h-12 items-center gap-2 rounded-full bg-gradient-to-r from-emerald-500 via-cyan-500 to-blue-500 px-7 text-sm font-semibold text-white shadow-lg shadow-emerald-500/25 transition-shadow hover:shadow-emerald-500/40"
              >
                <Link href="/sign-up" className="flex items-center gap-2">
                  Get free 30-day audit
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
              </MagneticButton>

              <MagneticButton
                strength={0.25}
                className="inline-flex h-12 items-center gap-2 rounded-full glass-elevated px-6 text-sm font-medium text-text hover:bg-bg-surface-hover transition-colors"
              >
                <Link href="/dashboard">View live demo</Link>
              </MagneticButton>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.5 }}
              className="mt-12 grid grid-cols-3 gap-6 max-w-md"
            >
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  <Counter to={20} suffix="%" />
                </div>
                <div className="text-xs text-text-muted mt-1">avg bill reduction</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  $<Counter to={12} duration={1.5} />k+
                </div>
                <div className="text-xs text-text-muted mt-1">saved / customer</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  <Counter to={30} duration={2.5} />s
                </div>
                <div className="text-xs text-text-muted mt-1">avg scan time</div>
              </div>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <Hero3D />
          </motion.div>
        </div>

        <ScrollReveal delay={0.6} className="mt-20">
          <div className="flex flex-wrap items-center justify-center gap-x-12 gap-y-6 text-sm text-text-muted">
            <span className="flex items-center gap-2">
              <Cloud className="h-4 w-4 text-emerald-400" />
              AWS · GCP · Azure
            </span>
            <span className="flex items-center gap-2">
              <Shield className="h-4 w-4 text-blue-400" />
              Read-only IAM
            </span>
            <span className="flex items-center gap-2">
              <Bot className="h-4 w-4 text-violet-400" />
              GPT-4o + FinOps-tuned
            </span>
            <span className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-amber-400" />
              Terraform PR in 60s
            </span>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
