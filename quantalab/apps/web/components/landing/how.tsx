"use client";
import { Card } from "@/components/ui/card";
import { Code2, FlaskConical, BarChart3, ShoppingCart } from "lucide-react";

const steps = [
  { n: 1, icon: Code2, title: "Describe a strategy in plain English", body: "Local Ollama (qwen3:8b) translates your idea to executable Python. You iterate by editing the generated code, not by re-prompting." },
  { n: 2, icon: FlaskConical, title: "Run in a sandboxed Jupyter kernel", body: "Real Python, real pandas, real numpy. No server access, no internet. The kernel survives between cells." },
  { n: 3, icon: BarChart3, title: "Backtest + walk-forward + Monte Carlo", body: "Sharpe, Sortino, max DD, factor attribution, equity curve fan. Out-of-sample by default, no in-sample leakage." },
  { n: 4, icon: ShoppingCart, title: "List on the marketplace", body: "Publish once, sell to thousands. We take 15%. You earn passive revenue while keeping your prop trading edge private." },
];

export function HowItWorks() {
  return (
    <section id="how" className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">How QuantaLab works</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">Jupyter is for school. QuantaLab is for shipping strategies that make money.</p>
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
