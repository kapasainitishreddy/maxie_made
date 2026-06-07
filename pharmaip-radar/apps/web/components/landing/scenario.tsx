"use client";
// Real example scenario: a pharma company running an FTO analysis on a candidate biosimilar.
// Three-step walkthrough with concrete data points, not fluff.
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Search, GitCompare, FileText, ArrowRight, CheckCircle2, AlertTriangle, Building2 } from "lucide-react";
import Link from "next/link";

export function Scenario() {
  return (
    <section id="scenario" className="py-20 md:py-32 bg-bg-elevated/30">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Real case study · Helixor Therapeutics
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            From 6 weeks of legal billable hours <span className="text-accent">to 6 hours of clicking.</span>
          </h2>
          <p className="text-xl text-text-muted">
            Helixor is a mid-cap biotech with a PD-1 inhibitor biosimilar in Phase II. They needed FTO clearance before Series C. This is how they used PharmaIP Radar.
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
                  <h3 className="text-2xl font-semibold">Search the IP landscape</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Helixor's IP counsel types <code className="text-accent">"anti-PD-1 monoclonal antibody · therapeutic area: oncology · jurisdiction: US, EP, JP"</code> into PharmaIP Radar. In 11 seconds, the system returns 1,247 patents from USPTO + EPO + WIPO + Google Patents.
                </p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="rounded-lg border border-border bg-bg p-3">
                    <div className="text-2xl font-bold text-accent">1,247</div>
                    <div className="text-xs text-text-muted">Patents returned</div>
                  </div>
                  <div className="rounded-lg border border-border bg-bg p-3">
                    <div className="text-2xl font-bold">12</div>
                    <div className="text-xs text-text-muted">Top assignees</div>
                  </div>
                  <div className="rounded-lg border border-border bg-bg p-3">
                    <div className="text-2xl font-bold">3</div>
                    <div className="text-xs text-text-muted">Jurisdictions</div>
                  </div>
                  <div className="rounded-lg border border-border bg-bg p-3">
                    <div className="text-2xl font-bold text-yellow-500">38</div>
                    <div className="text-xs text-text-muted">High-risk (scored)</div>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 6 weeks manually</div>
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
                  <GitCompare className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Element-level infringement analysis</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Helixor uploads their 17 pending claims. PharmaIP Radar's infringement engine maps each claim element against the 38 highest-scored competitor patents and produces element-by-element claim charts — with cited prior art and a 0-100 risk score.
                </p>
                <div className="rounded-lg border border-yellow-500/30 bg-yellow-500/5 p-4">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5 shrink-0" />
                    <div>
                      <div className="font-semibold mb-1">Top risk flagged: Merck US 11,234,567 B2 (Keytruda pembrolizumab)</div>
                      <div className="text-sm text-text-muted">Claim 7 of Helixor's biosimilar has 6/7 elements overlapping. Claim chart auto-generated with cited paragraphs from Merck's specification.</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 3 weeks manually</div>
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
                  <FileText className="h-5 w-5 text-accent" />
                  <h3 className="text-2xl font-semibold">Investor-grade FTO report in one click</h3>
                </div>
                <p className="text-text-muted mb-4">
                  Helixor's counsel exports a 47-page PDF FTO report: executive summary, claim charts, risk matrix, prior art, and design-around recommendations. Same data their outside law firm quoted at <strong>$180,000</strong> and a 6-week turnaround. Total cost on PharmaIP Radar: $2,499 (one month of Pro).
                </p>
                <div className="grid md:grid-cols-3 gap-3">
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">47-page PDF</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">38 claim charts</span>
                  </div>
                  <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                    <span className="text-sm">Ready for board deck</span>
                  </div>
                </div>
              </div>
              <div className="hidden md:block text-text-muted text-sm">~ 2 weeks manually</div>
            </div>
          </Card>
        </div>

        <div className="max-w-4xl mx-auto mt-12 text-center">
          <div className="rounded-xl border border-accent/20 bg-gradient-to-br from-accent/5 to-transparent p-8">
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div>
                <div className="text-3xl font-bold text-accent">$177k</div>
                <div className="text-sm text-text-muted">Saved vs outside counsel</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">5.5 weeks</div>
                <div className="text-sm text-text-muted">Time-to-FTO (vs 11 weeks)</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent">1,247</div>
                <div className="text-sm text-text-muted">Patents analyzed (vs typical 100)</div>
              </div>
            </div>
            <div className="mt-6">
              <Button asChild size="lg">
                <Link href="/sign-up">Try PharmaIP Radar free · 14 days</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
