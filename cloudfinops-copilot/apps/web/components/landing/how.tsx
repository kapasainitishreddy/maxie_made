"use client";
import { Card } from "@/components/ui/card";
import { KeyRound, Search, FileCode2, CheckCircle2 } from "lucide-react";

const steps = [
  { n: 1, icon: KeyRound, title: "Connect with a read-only IAM role", body: "One-time, 4 minutes. We never write to your account. We never store your data plane." },
  { n: 2, icon: Search, title: "We scan 30 days of usage + 90 days of metrics", body: "Idle EC2, oversized RDS, unattached EBS, NAT gateway abuse, data transfer, Graviton candidates, Savings Plan gaps." },
  { n: 3, icon: FileCode2, title: "We auto-generate a Terraform PR per fix", body: "Reversible, auditable, with risk score. You review the diff and click approve on Slack." },
  { n: 4, icon: CheckCircle2, title: "We measure verified savings for 30 days", body: "Then we invoice 20% of what we actually saved. Zero base fee, zero risk to you." },
];

export function HowItWorks() {
  return (
    <section id="how" className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">How CloudFinOps works</h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">Four steps from connection to verified savings. We get paid only if we actually save you money.</p>
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
