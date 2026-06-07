"use client";
/**
 * 3D Hero with floating AWS bill cards + animated money saving visualization.
 */
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect, useRef } from "react";
import { Server, Database, HardDrive, TrendingDown } from "lucide-react";

const resources = [
  { icon: Server, label: "EC2 m5.xlarge", cost: 140, color: "from-amber-500/20 to-amber-500/5", border: "border-amber-500/30" },
  { icon: Database, label: "RDS db.r5.large", cost: 220, color: "from-red-500/20 to-red-500/5", border: "border-red-500/30" },
  { icon: HardDrive, label: "EBS gp3 500GB", cost: 48, color: "from-amber-500/20 to-amber-500/5", border: "border-amber-500/30" },
  { icon: Server, label: "EC2 c5.2xlarge (idle)", cost: 168, color: "from-red-500/20 to-red-500/5", border: "border-red-500/30" },
];

export function Hero3D() {
  const ref = useRef<HTMLDivElement>(null);
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
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
        {/* Total bill card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="absolute top-[10%] left-[15%] w-72 rounded-2xl glass-elevated p-5 shadow-2xl shadow-accent/30"
          style={{ transform: "translateZ(100px)" }}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-text-muted">This month so far</span>
            <TrendingDown className="h-4 w-4 text-accent" />
          </div>
          <div className="text-4xl font-bold mb-1">$12,450</div>
          <div className="text-sm text-accent">↓ 20% potential savings = $2,490/mo</div>
          <div className="mt-3 h-2 bg-bg-elevated rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "80%" }}
              transition={{ duration: 1.5, delay: 0.5 }}
              className="h-full bg-gradient-accent"
            />
          </div>
        </motion.div>

        {/* Floating resource cards */}
        {resources.map((r, i) => {
          const positions = [
            { top: "5%", right: "10%", z: 60, rot: -8 },
            { top: "50%", right: "5%", z: 80, rot: 5 },
            { top: "65%", left: "10%", z: 50, rot: 7 },
            { top: "30%", left: "5%", z: 30, rot: -5 },
          ];
          const p = positions[i];
          const Icon = r.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1, y: [0, -8, 0] }}
              transition={{
                opacity: { duration: 0.6, delay: 0.2 + i * 0.1 },
                scale: { duration: 0.6, delay: 0.2 + i * 0.1 },
                y: { duration: 4 + i * 0.3, repeat: Infinity, ease: "easeInOut" },
              }}
              className={`absolute w-48 rounded-xl bg-gradient-to-br ${r.color} backdrop-blur-md border ${r.border} p-3 shadow-2xl`}
              style={{ top: p.top, left: p.left, right: p.right, transform: `translateZ(${p.z}px) rotate(${p.rot}deg)`, transformStyle: "preserve-3d" }}
            >
              <div className="flex items-center gap-2 mb-1">
                <Icon className="h-4 w-4 text-accent" />
                <div className="text-xs font-semibold line-clamp-1">{r.label}</div>
              </div>
              <div className="text-lg font-bold">${r.cost}<span className="text-xs text-text-muted">/mo</span></div>
            </motion.div>
          );
        })}

        {/* Savings badge */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
          className="absolute bottom-[8%] right-[20%] w-40 h-40 rounded-full bg-gradient-accent flex items-center justify-center text-center shadow-2xl shadow-accent/40"
          style={{ transform: "translateZ(120px)" }}
        >
          <div>
            <div className="text-3xl font-bold text-white">20%</div>
            <div className="text-xs text-white/90">savings</div>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
