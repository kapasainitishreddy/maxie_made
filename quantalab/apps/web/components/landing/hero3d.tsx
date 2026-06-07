"use client";
/** 3D Hero — floating code cells in 3D space, with parallax mouse follow. */
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect, useRef } from "react";
import { Code2, Sparkles, Cpu } from "lucide-react";

const cells = [
  { kind: "code", label: "def signals(prices)", value: "fast = prices.rolling(20).mean()", color: "from-accent/20 to-accent/5", border: "border-accent/30" },
  { kind: "code", label: "# backtest", value: "sharpe: 1.87 | max_dd: -8.4%", color: "from-cyan-500/20 to-cyan-500/5", border: "border-cyan-500/30" },
  { kind: "code", label: "Output", value: "+34.2% YTD", color: "from-emerald-500/20 to-emerald-500/5", border: "border-emerald-500/30" },
  { kind: "code", label: "NL → Code", value: "translated via qwen3:8b", color: "from-amber-500/20 to-amber-500/5", border: "border-amber-500/30" },
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
        {/* Central notebook */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="absolute top-[20%] left-[15%] w-[70%] rounded-2xl glass-elevated p-5 shadow-2xl shadow-accent/30"
          style={{ transform: "translateZ(100px)" }}
        >
          <div className="flex items-center gap-2 mb-3 text-text-muted text-xs">
            <div className="h-2.5 w-2.5 rounded-full bg-red-500/80" />
            <div className="h-2.5 w-2.5 rounded-full bg-amber-500/80" />
            <div className="h-2.5 w-2.5 rounded-full bg-emerald-500/80" />
            <span className="ml-2 font-mono">quantalab/notebook.ipynb</span>
          </div>
          <pre className="font-mono text-xs leading-relaxed text-text">
{`# Strategy: SMA crossover with regime filter
import pandas as pd

def signals(prices):
    fast = prices.rolling(20).mean()
    slow = prices.rolling(50).mean()

    out = []
    for i in range(1, len(prices)):
        if pd.isna(fast.iloc[i]) or pd.isna(slow.iloc[i]):
            continue
        if fast.iloc[i-1] < slow.iloc[i-1] and fast.iloc[i] > slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "buy"})
        elif fast.iloc[i-1] > slow.iloc[i-1] and fast.iloc[i] < slow.iloc[i]:
            out.append({"timestamp": prices.index[i], "side": "sell"})
    return out

# Backtest result:
# Sharpe: 1.87 | Max DD: -8.4% | Return: +34.2%`}
          </pre>
        </motion.div>

        {/* Floating code badges */}
        {cells.map((c, i) => {
          const positions = [
            { top: "5%", right: "5%", z: 80, rot: -8 },
            { top: "8%", left: "5%", z: 60, rot: 6 },
            { top: "65%", right: "10%", z: 90, rot: 5 },
            { top: "70%", left: "8%", z: 50, rot: -6 },
          ];
          const p = positions[i];
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1, y: [0, -8, 0] }}
              transition={{ opacity: { duration: 0.6, delay: 0.3 + i * 0.1 }, scale: { duration: 0.6, delay: 0.3 + i * 0.1 }, y: { duration: 4 + i * 0.3, repeat: Infinity, ease: "easeInOut" } }}
              className={`absolute w-56 rounded-xl bg-gradient-to-br ${c.color} backdrop-blur-md border ${c.border} p-3 shadow-2xl`}
              style={{ top: p.top, left: p.left, right: p.right, transform: `translateZ(${p.z}px) rotate(${p.rot}deg)`, transformStyle: "preserve-3d" }}
            >
              <div className="flex items-center gap-2 mb-1">
                <Code2 className="h-3.5 w-3.5 text-accent" />
                <div className="text-xs font-semibold">{c.label}</div>
              </div>
              <pre className="font-mono text-xs text-text-muted truncate">{c.value}</pre>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
}
