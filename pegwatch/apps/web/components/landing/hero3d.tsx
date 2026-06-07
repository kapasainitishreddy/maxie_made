"use client";

import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Bell, Activity, Shield } from "lucide-react";
import Link from "next/link";
import { formatPct, formatZ, formatUSDshort, severityDot } from "@/lib/utils";

export function Hero3D() {
  const ref = useRef<HTMLDivElement>(null);
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
  const sx = useSpring(mx, { stiffness: 60, damping: 20 });
  const sy = useSpring(my, { stiffness: 60, damping: 20 });
  const rotX = useTransform(sy, [-15, 15], [6, -6]);
  const rotY = useTransform(sx, [-15, 15], [-6, 6]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      const r = ref.current?.getBoundingClientRect();
      if (!r) return;
      mx.set(((e.clientX - r.left) / r.width - 0.5) * 30);
      my.set(((e.clientY - r.top) / r.height - 0.5) * 30);
    };
    window.addEventListener("mousemove", handler);
    return () => window.removeEventListener("mousemove", handler);
  }, [mx, my]);

  return (
    <div
      ref={ref}
      className="relative h-[600px] w-full"
      style={{ perspective: "1200px" }}
    >
      <motion.div
        className="absolute inset-0"
        style={{ rotateX: rotX, rotateY: rotY, transformStyle: "preserve-3d" }}
      >
        {/* Main peg monitor card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className="absolute top-[15%] left-[8%] w-[84%] md:w-[55%] rounded-2xl glass-elevated p-5 shadow-2xl shadow-accent/20"
          style={{ transform: "translateZ(80px)" }}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-accent flex items-center justify-center text-white font-bold">
                $
              </div>
              <div>
                <div className="font-semibold">USDC — USD Coin</div>
                <div className="text-xs text-text-muted">Circle · Ethereum</div>
              </div>
            </div>
            <Badge variant="success">
              <span className={`w-1.5 h-1.5 rounded-full ${severityDot("healthy")}`} />
              Healthy
            </Badge>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div>
              <div className="text-xs text-text-muted">Price</div>
              <div className="text-2xl font-bold">$1.0001</div>
            </div>
            <div>
              <div className="text-xs text-text-muted">Deviation</div>
              <div className="text-2xl font-bold text-ok">{formatPct(0.01)}</div>
            </div>
            <div>
              <div className="text-xs text-text-muted">Z-score</div>
              <div className="text-2xl font-bold">{formatZ(0.42)}</div>
            </div>
          </div>
          {/* Sparkline */}
          <svg className="mt-4 w-full h-16" viewBox="0 0 300 50" preserveAspectRatio="none">
            <defs>
              <linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.5" />
                <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path
              d="M 0 25 L 20 22 L 40 28 L 60 24 L 80 26 L 100 22 L 120 27 L 140 23 L 160 25 L 180 21 L 200 24 L 220 26 L 240 23 L 260 25 L 280 22 L 300 24"
              fill="none"
              stroke="#10b981"
              strokeWidth="2"
            />
            <path
              d="M 0 25 L 20 22 L 40 28 L 60 24 L 80 26 L 100 22 L 120 27 L 140 23 L 160 25 L 180 21 L 200 24 L 220 26 L 240 23 L 260 25 L 280 22 L 300 24 L 300 50 L 0 50 Z"
              fill="url(#spark)"
            />
            <line x1="0" y1="25" x2="300" y2="25" stroke="#f59e0b" strokeWidth="0.5" strokeDasharray="4 4" opacity="0.5" />
          </svg>
        </motion.div>

        {/* Floating alert card (top right) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1, y: [0, -8, 0] }}
          transition={{
            y: { duration: 4, repeat: Infinity, ease: "easeInOut" },
            delay: 0.3,
          }}
          className="absolute top-[2%] right-[5%] w-44 rounded-xl bg-gradient-to-br from-warn/20 to-crit/20 backdrop-blur-md border border-warn/30 p-3 shadow-2xl"
          style={{ transform: "translateZ(100px) rotate(-6deg)" }}
        >
          <div className="flex items-center gap-2 mb-2">
            <Bell className="w-3 h-3 text-warn" />
            <span className="text-xs font-semibold text-warn">FRAX Warning</span>
          </div>
          <div className="text-xs">+0.32% off peg</div>
          <div className="text-xs text-text-muted">z = +2.14</div>
          <div className="text-xs text-text-muted mt-1">2m ago</div>
        </motion.div>

        {/* Floating liquidity card (right) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1, y: [0, -10, 0] }}
          transition={{
            y: { duration: 4.5, repeat: Infinity, ease: "easeInOut" },
            delay: 0.5,
          }}
          className="absolute top-[55%] right-[8%] w-44 rounded-xl bg-gradient-to-br from-accent/20 to-blue-500/20 backdrop-blur-md border border-accent/30 p-3 shadow-2xl"
          style={{ transform: "translateZ(70px) rotate(5deg)" }}
        >
          <div className="flex items-center gap-2 mb-2">
            <Activity className="w-3 h-3 text-accent" />
            <span className="text-xs font-semibold">Liquidity</span>
          </div>
          <div className="text-xl font-bold">$42.8M</div>
          <div className="text-xs text-text-muted">Curve · ±0.5%</div>
        </motion.div>

        {/* Floating coverage card (bottom left) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1, y: [0, -6, 0] }}
          transition={{
            y: { duration: 5, repeat: Infinity, ease: "easeInOut" },
            delay: 0.7,
          }}
          className="absolute bottom-[5%] left-[5%] w-48 rounded-xl bg-gradient-to-br from-accent/15 to-emerald-400/15 backdrop-blur-md border border-accent/30 p-3 shadow-2xl"
          style={{ transform: "translateZ(60px) rotate(4deg)" }}
        >
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-3 h-3 text-accent" />
            <span className="text-xs font-semibold">Monitoring</span>
          </div>
          <div className="text-xl font-bold">8 stables</div>
          <div className="text-xs text-text-muted">$150B aggregate</div>
        </motion.div>
      </motion.div>
    </div>
  );
}
