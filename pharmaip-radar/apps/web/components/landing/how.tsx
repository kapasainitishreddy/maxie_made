"use client";
// "How PharmaIP Radar works" — 4-step process diagram
import { Card } from "@/components/ui/card";
import { Database, Cpu, GitBranch, FileText } from "lucide-react";

const steps = [
  {
    n: 1,
    icon: Database,
    title: "We ingest 100M+ patents nightly",
    body: "USPTO, EPO, WIPO, Google Patents. Plus drug databases (FDA Orange Book, EMA). We dedupe, normalize, and re-classify by therapeutic area.",
  },
  {
    n: 2,
    icon: Cpu,
    title: "AI scores every claim against your portfolio",
    body: "Our infringement engine (TF-IDF + LLM re-ranking) compares your claims element-by-element. Risk 0-100 with human-readable explanation.",
  },
  {
    n: 3,
    icon: GitBranch,
    title: "You collaborate with your team",
    body: "Org workspaces, role-based access, comments, watchlists. Email alerts when new patents in your therapeutic area are filed.",
  },
  {
    n: 4,
    icon: FileText,
    title: "Export investor-grade PDF reports",
    body: "FTO clearance, landscape, prior art, design-around. Cited, dated, board-ready. 47 pages in 90 seconds.",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">How PharmaIP Radar works</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">Four steps from query to board-ready report. No manual PDF reading, no claim-chart drafting in Word, no $400/hr associate time.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {steps.map((s) => (
            <Card key={s.n} className="p-6 relative">
              <div className="absolute -top-3 -left-3 h-8 w-8 rounded-full bg-gradient-accent text-white text-sm font-bold flex items-center justify-center">{s.n}</div>
              <s.icon className="h-8 w-8 text-accent mb-3" />
              <h3 className="text-lg font-semibold mb-2">{s.title}</h3>
              <p className="text-sm text-text-muted leading-relaxed">{s.body}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
