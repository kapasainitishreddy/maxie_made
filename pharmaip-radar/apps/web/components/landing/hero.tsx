"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Hero3D } from "./hero3d";
import { MagneticButton, FloatingBadge, Counter, Typewriter, ScrollReveal } from "@/components/fx/motion";
import { ArrowRight, Sparkles, Zap, Shield, FileSearch, Brain } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden aurora-bg noise">
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 -z-10 grid-bg mask-radial" />

      {/* Floating gradient orbs */}
      <div className="absolute top-1/4 left-1/4 -z-10 h-72 w-72 rounded-full bg-violet-500/20 blur-[120px] float" />
      <div className="absolute bottom-1/4 right-1/4 -z-10 h-96 w-96 rounded-full bg-blue-500/15 blur-[120px] float-delayed" />

      <div className="container mx-auto px-4 pt-24 pb-24 md:pt-32 md:pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left: copy */}
          <div className="relative z-10">
            <FloatingBadge>
              <div className="inline-flex items-center gap-2 rounded-full glass px-4 py-1.5 text-xs font-medium text-text-muted">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
                </span>
                Live · 100M+ patents indexed
              </div>
            </FloatingBadge>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="mt-8 text-5xl md:text-7xl font-bold tracking-tight text-balance"
            >
              The <span className="gradient-text">pharma IP radar</span> your legal team needs
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="mt-6 text-lg md:text-xl text-text-muted max-w-xl text-balance"
            >
              Ingest 100M+ patents. Detect infringement in seconds.
              Run FTO analyses with AI claim scoring. The fastest way to <Typewriter words={["protect", "license", "monetize", "defend"]} className="text-text" /> your pharma IP.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.3 }}
              className="mt-10 flex flex-wrap items-center gap-4"
            >
              <MagneticButton
                strength={0.25}
                className="group relative inline-flex h-12 items-center gap-2 rounded-full bg-gradient-to-r from-violet-500 via-fuchsia-500 to-blue-500 px-7 text-sm font-semibold text-white shadow-lg shadow-violet-500/25 transition-shadow hover:shadow-violet-500/40"
              >
                <Link href="/sign-up" className="flex items-center gap-2">
                  Start free trial
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
              </MagneticButton>

              <MagneticButton
                strength={0.25}
                className="inline-flex h-12 items-center gap-2 rounded-full glass-elevated px-6 text-sm font-medium text-text hover:bg-bg-surface-hover transition-colors"
              >
                <Link href="/pricing">View pricing</Link>
              </MagneticButton>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.5 }}
              className="mt-12 grid grid-cols-3 gap-6 max-w-md"
            >
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  <Counter to={100} suffix="M+" />
                </div>
                <div className="text-xs text-text-muted mt-1">patents indexed</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  <Counter to={6} duration={1.5} />h
                </div>
                <div className="text-xs text-text-muted mt-1">avg FTO time</div>
              </div>
              <div>
                <div className="text-3xl font-bold gradient-text-static">
                  $<Counter to={177} duration={2.5} suffix="k" />
                </div>
                <div className="text-xs text-text-muted mt-1">avg savings/case</div>
              </div>
            </motion.div>
          </div>

          {/* Right: 3D hero */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <Hero3D />
          </motion.div>
        </div>

        {/* Trust strip */}
        <ScrollReveal delay={0.6} className="mt-20">
          <div className="flex flex-wrap items-center justify-center gap-x-12 gap-y-6 text-sm text-text-muted">
            <span className="flex items-center gap-2">
              <Shield className="h-4 w-4 text-emerald-400" />
              SOC 2 Type II
            </span>
            <span className="flex items-center gap-2">
              <FileSearch className="h-4 w-4 text-blue-400" />
              USPTO + EPO + WIPO
            </span>
            <span className="flex items-center gap-2">
              <Brain className="h-4 w-4 text-violet-400" />
              GPT-4o + Claude 3.5
            </span>
            <span className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-amber-400" />
              Sub-200ms latency
            </span>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
