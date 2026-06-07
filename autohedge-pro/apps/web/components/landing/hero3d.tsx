"use client";
/** 3D Hero — animated equity curve over a tilted plane with floating P&L cards. */
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect, useRef } from "react";
import { TrendingUp, TrendingDown, Activity, Zap } from "lucide-react";

const stats = [
  { label: "YTD Return", value: "+34.2%", up: true, icon: TrendingUp, color: "from-emerald-500/20 to-emerald-500/5", border: "border-emerald-500/30" },
  { label: "Sharpe", value: "1.87", up: true, icon: Activity, color: "from-cyan-500/20 to-cyan-500/5", border: "border-cyan-500/30" },
  { label: "Max DD", value: "-8.4%", up: false, icon: TrendingDown, color: "from-red-500/20 to-red-500/5", border: "border-red-500/30" },
  { label: "Win Rate", value: "62%", up: true, icon: Zap, color: "from-accent/20 to-accent/5", border: "border-accent/30" },
];

export function Hero3D() {
  const ref = useRef<HTMLDivElement>(null);
  const mx = useMotionValue(0); const my = useMotionValue(0);
  const sx = useSpring(mx, { stiffness: 60, damping: 20 });
  const sy = useSpring(my, { stiffness: 60, damping: 20 });
  const rotX = useTransform(sy, [-15, 15], [6, -6]);
  const rotY = useTransform(sx, [-15, 15], [-6, 6]);

  useEffect(() => {
    const h = (e: MouseEvent) => {
      const r = ref.current?.getBoundingClientRect();
      if (!r) return;
      mx.set(((e.clientX - r.left) / r.width - 0.5) * 30);
      my.set(((e.clientY - r.top) / r.height - 0.5) * 30);
    };
    window.addEventListener("mousemove", h);
    return () => window.removeEventListener("mousemove", h);
  }, [mx, my]);

  return (
    <div ref={ref} className="relative h-[600px]" style={{ perspective: "1200px" }}>
      <motion.div className="absolute inset-0" style={{ rotateX: rotX, rotateY: rotY, transformStyle: "preserve-3d" }}>
        {/* Equity curve plane */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="absolute top-[15%] left-[8%] w-[80%] h-64 rounded-2xl glass-elevated p-6 shadow-2xl shadow-accent/30"
          style={{ transform: "translateZ(80px)" }}
        >
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="text-sm text-text-muted">Portfolio Value</div>
              <div className="text-3xl font-bold">$134,210</div>
            </div>
            <div className="text-emerald-400 font-semibold">+34.2% YTD</div>
          </div>
          <svg viewBox="0 0 400 120" className="w-full h-40">
            <defs>
              <linearGradient id="eqgrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.5" />
                <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
              </linearGradient>
            </defs>
            <motion.path
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2, ease: "easeInOut" }}
              d="M0,100 Q50,80 100,70 T200,40 T300,30 T400,10 L400,120 L0,120 Z"
              fill="url(#eqgrad)"
            />
            <motion.path
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2, ease: "easeInOut" }}
              d="M0,100 Q50,80 100,70 T200,40 T300,30 T400,10"
              fill="none"
              stroke="#10b981"
              strokeWidth="2"
            />
          </svg>
        </motion.div>

        {/* Floating stats */}
        {stats.map((s, i) => {
          const positions = [
            { top: "5%", right: "5%", z: 100, rot: -8 },
            { top: "55%", right: "8%", z: 70, rot: 5 },
            { top: "65%", left: "5%", z: 60, rot: 7 },
            { top: "8%", left: "20%", z: 50, rot: -5 },
          ];
          const p = positions[i];
          const Icon = s.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1, y: [0, -8, 0] }}
              transition={{ opacity: { duration: 0.6, delay: 0.3 + i * 0.1 }, scale: { duration: 0.6, delay: 0.3 + i * 0.1 }, y: { duration: 4 + i * 0.3, repeat: Infinity, ease: "easeInOut" } }}
              className={`absolute w-40 rounded-xl bg-gradient-to-br ${s.color} backdrop-blur-md border ${s.border} p-3 shadow-2xl`}
              style={{ top: p.top, left: p.left, right: p.right, transform: `translateZ(${p.z}px) rotate(${p.rot}deg)`, transformStyle: "preserve-3d" }}
            >
              <div className="flex items-center gap-2 mb-1">
                <Icon className="h-3.5 w-3.5 text-accent" />
                <div className="text-xs text-text-muted">{s.label}</div>
              </div>
              <div className={`text-xl font-bold ${s.up ? "text-emerald-400" : "text-red-400"}`}>{s.value}</div>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
}
