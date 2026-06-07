import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Cloud, TrendingDown, Shield, Zap } from "lucide-react";
import { Card } from "@/components/ui/card";

export function Features() {
  const features = [
    { icon: Cloud, title: "AWS, GCP, Azure", desc: "One read-only IAM role. We never touch your data plane." },
    { icon: TrendingDown, title: "20% verified savings", desc: "Rightsizing, idle termination, scheduling, Graviton migration, RIs." },
    { icon: Shield, title: "Slack approval flow", desc: "Every change posts a Block Kit card. Click to approve. We never auto-apply." },
    { icon: Zap, title: "Performance-based", desc: "0% base fee. You only pay 20% of verified monthly savings." },
  ];
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Cloud cost, finally fixed.</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">Stop the 4am bill shock. Let AI quietly trim the fat.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {features.map((f, i) => (
            <Card key={i} className="p-6 hover:border-accent/50 transition-all">
              <div className="h-12 w-12 rounded-lg bg-gradient-accent/10 border border-accent/20 flex items-center justify-center mb-4">
                <f.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-text-muted text-sm">{f.desc}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
