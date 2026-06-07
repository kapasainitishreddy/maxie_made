"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles } from "lucide-react";
import { Hero3D } from "@/components/landing/hero3d";
export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-gradient-radial" />
      <div className="absolute inset-0 -z-10 bg-[linear-gradient(rgba(139,92,246,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(139,92,246,0.05)_1px,transparent_1px)] bg-[size:60px_60px]" />
      <div className="container mx-auto px-4 pt-20 pb-24 md:pt-32 md:pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }}>
            <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-accent/30 bg-accent/5 text-sm">
              <Sparkles className="h-3.5 w-3.5 text-accent" /><span className="text-text-muted">NL→Code · Sandbox · Marketplace</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
              The <span className="text-gradient">quant research</span> IDE,<br />in your browser.
            </h1>
            <p className="text-xl md:text-2xl text-text-muted mb-10 leading-relaxed">
              Notebooks with real Python. Describe a strategy in plain English, get backtest code. Walk-forward, Monte Carlo, factor attribution, marketplace.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button asChild size="lg"><Link href="/sign-up">Start free <ArrowRight className="h-4 w-4" /></Link></Button>
              <Button asChild size="lg" variant="outline"><Link href="/pricing">Pricing</Link></Button>
            </div>
            <p className="mt-6 text-sm text-text-muted">No card · $0 free tier · 3-day Researcher trial</p>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8, delay: 0.2 }}><Hero3D /></motion.div>
        </div>
      </div>
    </section>
  );
}
