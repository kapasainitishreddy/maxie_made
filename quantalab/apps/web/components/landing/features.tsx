"use client";
import { Card } from "@/components/ui/card";
import { Code2, FlaskConical, BarChart3, ShoppingCart } from "lucide-react";

const features = [
  { icon: Code2, title: "Plain English → Code", description: "Describe a strategy in natural language. Local Ollama (qwen3:8b) writes the Python. You iterate by editing code, not by re-prompting." },
  { icon: FlaskConical, title: "Real Python notebook", description: "Sandboxed Jupyter kernel with real pandas, numpy, scipy, scikit-learn. No server access, no internet. Cells survive between runs." },
  { icon: BarChart3, title: "Walk-forward + Monte Carlo", description: "Out-of-sample validation. 5,000 Monte Carlo paths. Sharpe, Sortino, max DD, factor attribution, equity curve fan. No in-sample leakage by default." },
  { icon: ShoppingCart, title: "Strategy marketplace", description: "Publish your strategy once, sell to thousands of subscribers. We take 15%. You earn passive income while keeping prop trading edge private." },
];

export function Features() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            For serious quants.
          </h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            Jupyter is for school. QuantaLab is for shipping strategies that make money.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {features.map((f, i) => (
            <Card key={i} className="p-6 hover:border-accent/50 transition-all group">
              <div className="h-12 w-12 rounded-lg bg-gradient-accent/10 border border-accent/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <f.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
              <p className="text-sm text-text-muted leading-relaxed">{f.description}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
