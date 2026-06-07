"use client";
import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const faqs = [
  { q: "How do you verify savings?", a: "We track your baseline cost for 30 days, then measure actual post-execution cost. You pay 20% of the verified difference, never more." },
  { q: "What if you terminate something important?", a: "We never auto-apply. Every change posts a Terraform PR to Slack. You review the diff, see the cost impact, then click Approve." },
  { q: "What permissions do you need?", a: "Read-only IAM cross-account role. We list resources, read CloudWatch metrics, and read Cost Explorer. Zero write access." },
  { q: "Is there a setup fee?", a: "No setup fee, no minimum. The free audit shows what we can save in 24 hours. You only pay after the first $100 in verified savings." },
];

export function FAQ() {
  const [open, setOpen] = useState(0);
  return (
    <section className="py-20">
      <div className="container mx-auto px-4 max-w-3xl">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12">FAQ</h2>
        <div className="space-y-3">
          {faqs.map((f, i) => (
            <div key={i} className="rounded-xl border border-border bg-bg-surface/60 overflow-hidden">
              <button onClick={() => setOpen(open === i ? null : i)} className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-bg-elevated/50">
                <span className="font-medium">{f.q}</span>
                <ChevronDown className={`h-4 w-4 transition-transform ${open === i ? "rotate-180" : ""}`} />
              </button>
              <AnimatePresence>
                {open === i && (
                  <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} exit={{ height: 0 }} className="overflow-hidden">
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
