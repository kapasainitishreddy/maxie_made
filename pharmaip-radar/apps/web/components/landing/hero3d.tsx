"use client";

/**
 * 3D Hero with floating patent cards.
 * Uses CSS 3D transforms + framer-motion for parallax float.
 * No external 3D library required — pure CSS for max perf.
 */

import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect, useRef } from "react";
import { FileText, AlertTriangle, CheckCircle2 } from "lucide-react";

const samplePatents = [
  {
    title: "Anti-PD-1 antibodies",
    assignee: "Merck",
    drug: "Keytruda",
    risk: "low",
    color: "from-emerald-500/20 to-emerald-500/5",
    border: "border-emerald-500/30",
  },
  {
    title: "IL-23 antagonist",
    assignee: "AbbVie",
    drug: "Skyrizi",
    risk: "medium",
    color: "from-amber-500/20 to-amber-500/5",
    border: "border-amber-500/30",
  },
  {
    title: "Apixaban formulation",
    assignee: "BMS",
    drug: "Eliquis",
    risk: "low",
    color: "from-emerald-500/20 to-emerald-500/5",
    border: "border-emerald-500/30",
  },
  {
    title: "Aflibercept",
    assignee: "Regeneron",
    drug: "Eylea",
    risk: "high",
    color: "from-red-500/20 to-red-500/5",
    border: "border-red-500/30",
  },
  {
    title: "CAR-T CD19",
    assignee: "Novartis",
    drug: "Kymriah",
    risk: "medium",
    color: "from-amber-500/20 to-amber-500/5",
    border: "border-amber-500/30",
  },
  {
    title: "mRNA vaccine",
    assignee: "Moderna",
    drug: "Spikevax",
    risk: "low",
    color: "from-emerald-500/20 to-emerald-500/5",
    border: "border-emerald-500/30",
  },
];

export function Hero3D() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
  const sx = useSpring(mx, { stiffness: 60, damping: 20 });
  const sy = useSpring(my, { stiffness: 60, damping: 20 });

  useEffect(() => {
    const handle = (e: MouseEvent) => {
      const rect = containerRef.current?.getBoundingClientRect();
      if (!rect) return;
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      mx.set(x * 30);
      my.set(y * 30);
    };
    window.addEventListener("mousemove", handle);
    return () => window.removeEventListener("mousemove", handle);
  }, [mx, my]);

  const rotX = useTransform(sy, [-15, 15], [8, -8]);
  const rotY = useTransform(sx, [-15, 15], [-8, 8]);

  return (
    <div
      ref={containerRef}
      className="relative h-[600px] perspective-1000"
      style={{ perspective: "1200px" }}
    >
      <motion.div
        className="absolute inset-0"
        style={{ rotateX: rotX, rotateY: rotY, transformStyle: "preserve-3d" }}
      >
        {/* Floating cards */}
        {samplePatents.map((p, i) => (
          <PatentCard key={i} patent={p} index={i} />
        ))}

        {/* Central glow */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-gradient-accent opacity-20 blur-3xl"
          style={{ transform: "translate(-50%, -50%) translateZ(0)" }}
        />
      </motion.div>
    </div>
  );
}

function PatentCard({
  patent,
  index,
}: {
  patent: typeof samplePatents[0];
  index: number;
}) {
  const positions = [
    { top: "5%", left: "10%", z: 50, rot: -8 },
    { top: "15%", right: "8%", z: 80, rot: 6 },
    { top: "40%", left: "5%", z: 30, rot: 4 },
    { top: "55%", right: "15%", z: 70, rot: -4 },
    { top: "70%", left: "20%", z: 60, rot: 8 },
    { top: "75%", right: "5%", z: 40, rot: -6 },
  ];
  const pos = positions[index % positions.length];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{
        opacity: 1,
        scale: 1,
        y: [0, -10, 0],
      }}
      transition={{
        opacity: { duration: 0.6, delay: index * 0.1 },
        scale: { duration: 0.6, delay: index * 0.1 },
        y: { duration: 4 + index * 0.3, repeat: Infinity, ease: "easeInOut" },
      }}
      whileHover={{ scale: 1.05, zIndex: 100 }}
      className={`absolute w-56 rounded-xl bg-gradient-to-br ${patent.color} backdrop-blur-md border ${patent.border} p-4 shadow-2xl`}
      style={{
        top: pos.top,
        left: pos.left,
        right: pos.right,
        transform: `translateZ(${pos.z}px) rotate(${pos.rot}deg)`,
        transformStyle: "preserve-3d",
      }}
    >
      <div className="flex items-start gap-2 mb-2">
        <FileText className="h-4 w-4 text-accent mt-0.5 flex-shrink-0" />
        <div className="text-sm font-semibold leading-tight line-clamp-2">{patent.title}</div>
      </div>
      <div className="text-xs text-text-muted mb-2">{patent.assignee}</div>
      <div className="flex items-center justify-between text-xs">
        <span className="font-mono text-text-muted">{patent.drug}</span>
        <RiskBadge risk={patent.risk} />
      </div>
    </motion.div>
  );
}

function RiskBadge({ risk }: { risk: string }) {
  const map = {
    low: { color: "text-emerald-400", icon: CheckCircle2, label: "Low" },
    medium: { color: "text-amber-400", icon: AlertTriangle, label: "Med" },
    high: { color: "text-red-400", icon: AlertTriangle, label: "High" },
  };
  const cfg = map[risk as keyof typeof map] || map.low;
  const Icon = cfg.icon;
  return (
    <span className={`flex items-center gap-1 ${cfg.color}`}>
      <Icon className="h-3 w-3" />
      {cfg.label}
    </span>
  );
}
