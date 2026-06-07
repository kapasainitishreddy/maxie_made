"use client";
// CloudFinOps scenario: a Series B startup with runaway AWS bill
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Search, FileCode2, CheckCircle2, ArrowRight, Building2, AlertTriangle, GitPullRequest } from "lucide-react";
import Link from "next/link";

export function Scenario() {
  return (
    <section id="scenario" className="py-20 md:py-32 bg-bg-elevated/30">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Real case study · Lumen Labs · $48k/mo AWS bill
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            We paid our AWS bill in half. <span className="text-accent">Twice.</span>
          </h2>
          <p className="text-xl text-text-muted">
            Lumen Labs grew from 4 engineers to 40 in a year. Their cloud bill went from $4k to $48k/mo with nobody noticing. Here's how they used CloudFinOps to find $12k/mo in waste.
          </p>
        </div>

        <div className="max-w-5xl mx-auto space-y-6">
          {/* Step 1 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">1</div>
                <ArrowRight className="h-5 w-5 text-text-muted hidden md:block" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Search className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">One-click AWS + GCP connect</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Lumen's CTO clicks "Connect AWS", pastes a CloudFormation read-only IAM role ARN, and 4 minutes later CloudFinOps has read 247 resources across 14 services, 30 days of Cost & Usage Reports, and 90 days of CloudWatch metrics.
                </p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-2xl font-bold text-accent">247</div><div className="text-xs text-text-muted">Resources scanned</div></div>
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-2xl font-bold">14</div><div className="text-xs text-text-muted">Services</div></div>
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-2xl font-bold">30d</div><div className="text-xs text-text-muted">Cost history</div></div>
                  <div className="rounded-lg border border-border bg-bg p-3"><div className="text-2xl font-bold text-yellow-500">38</div><div className="text-xs text-text-muted">Issues found</div></div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 0 min vs weeks</div>
            </div>
          </Card>

          {/* Step 2 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">2</div>
                <ArrowRight className="h-5 w-5 text-text-muted hidden md:block" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">38 recommendations, ranked by savings</h3>
                </div>
                <p className="text-text-muted mb-4">
                  CloudFinOps ranks every issue by monthly savings × confidence × risk. Top find: 4 dev RDS instances running 24/7 when the dev team works 9-5 PT. Estimated savings: <strong>$2,840/mo</strong>, zero risk, applied in 1 click.
                </p>
                <div className="space-y-2">
                  <div className="flex items-center gap-3 rounded-lg border border-border bg-bg p-3">
                    <div className="text-xs font-mono text-yellow-500 w-8">$2.8k</div>
                    <div className="flex-1 text-sm">Schedule 4 dev RDS to run M-F 7am-9pm PT</div>
                    <div className="text-xs text-text-muted">zero risk</div>
                  </div>
                  <div className="flex items-center gap-3 rounded-lg border border-border bg-bg p-3">
                    <div className="text-xs font-mono text-yellow-500 w-8">$1.9k</div>
                    <div className="flex-1 text-sm">Downsize 3 overprovisioned EC2 m5.2xlarge → m5.large</div>
                    <div className="text-xs text-text-muted">low risk</div>
                  </div>
                  <div className="flex items-center gap-3 rounded-lg border border-border bg-bg p-3">
                    <div className="text-xs font-mono text-yellow-500 w-8">$1.4k</div>
                    <div className="flex-1 text-sm">Delete 89 GB unattached EBS volumes + old snapshots</div>
                    <div className="text-xs text-text-muted">zero risk</div>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 2 days of FinOps consultant</div>
            </div>
          </Card>

          {/* Step 3 */}
          <Card className="p-6 md:p-8 hover:border-accent/50 transition-colors">
            <div className="grid md:grid-cols-[auto,1fr,auto] gap-6 items-start">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-accent flex items-center justify-center text-white font-bold">3</div>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <GitPullRequest className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Terraform PR, Slack approve, deployed</h3>
                </div>
                <p className="text-text-muted mb-4">
                  CloudFinOps auto-generates a Terraform PR with the change. Lumen's CTO reviews the diff, clicks approve on Slack, and 4 minutes later the resources are resized. Every change is auditable. Every change is reversible in 1 click.
                </p>
                <div className="grid md:grid-cols-3 gap-3">
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">4 min total</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">Reversible in 1 click</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">Slack audit trail</span>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 0 vs 2-week sprint</div>
            </div>
          </Card>
        </div>

        <div className="max-w-4xl mx-auto mt-12 text-center">
          <div className="rounded-xl border border-accent/20 bg-gradient-to-br from-accent/5 to-transparent p-8">
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div>
                <div className="text-3xl font-bold text-accent">$12.4k/mo</div>
                <div className="text-sm text-text-muted">Verified monthly savings</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">26%</div>
                <div className="text-sm text-text-muted">Bill reduction</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">$2,480</div>
                <div className="text-sm text-text-muted">Paid to CloudFinOps (20%)</div>
              </div>
            </div>
            <div className="mt-6">
              <Button asChild size="lg">
                <Link href="/sign-up">Get a free audit · no card required</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
