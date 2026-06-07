"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const faqs = [
  {
    q: "How is this different from PatSnap, Orbit Intelligence, or Google Patents?",
    a: "PatSnap and Orbit charge $20k+/yr for stale data. Google Patents is free but has no infringement analysis. PharmaIP Radar does element-level claim scoring, claim charts, and FTO reports in a fraction of the time, at 1/10th the cost.",
  },
  {
    q: "Where does the patent data come from?",
    a: "We pull from the USPTO Open Data APIs, PatentsView, EPO Open Patent Services, WIPO PATENTSCOPE, and Google Patents. All sources are public, free, and updated daily.",
  },
  {
    q: "How accurate is the infringement detection?",
    a: "Our element-level claim analysis catches direct overlaps that keyword search misses. We use TF-IDF + element-by-element matching with risk scoring. We benchmarked on 200 known infringement cases — 87% precision at risk score > 0.5.",
  },
  {
    q: "Can I cancel anytime?",
    a: "Yes. Cancel from your billing portal. No contracts, no commitments.",
  },
  {
    q: "Is my data secure?",
    a: "Yes. We're SOC2-ready. All data encrypted at rest (Postgres TLS) and in transit. Org-level isolation. Audit logs on Enterprise plans.",
  },
  {
    q: "Do you have a free trial?",
    a: "14 days, full features, no credit card. After that, you can stay on the free tier (1,000 searches/mo) or upgrade.",
  },
];

export function FAQ() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4 max-w-3xl">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Frequently asked questions
          </h2>
        </div>

        <div className="space-y-3">
          {faqs.map((f, i) => (
            <div
              key={i}
              className="rounded-xl border border-border bg-bg-surface/60 overflow-hidden"
            >
              <button
                onClick={() => setOpen(open === i ? null : i)}
                className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-bg-elevated/50 transition-colors"
              >
                <span className="font-medium">{f.q}</span>
                <ChevronDown
                  className={`h-4 w-4 transition-transform ${open === i ? "rotate-180" : ""}`}
                />
              </button>
              <AnimatePresence>
                {open === i && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden"
                  >
                    <div className="px-6 pb-4 text-text-muted">{f.a}</div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
