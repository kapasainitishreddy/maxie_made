import { FileSearch, AlertTriangle, BarChart3, Shield, Building2, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";

const features = [
  {
    icon: FileSearch,
    title: "100M+ patents searchable",
    description: "Search USPTO, EPO, WIPO, and Google Patents in one query. Drug name, therapeutic area, IPC class — all filterable.",
  },
  {
    icon: AlertTriangle,
    title: "Infringement detection in minutes",
    description: "Element-level claim analysis with claim charts. Get a risk score and human-readable explanation for every potential conflict.",
  },
  {
    icon: BarChart3,
    title: "IP landscape visualization",
    description: "Density heatmaps, top assignees, tech clusters, white space detection. See the field before you make a move.",
  },
  {
    icon: Shield,
    title: "FTO + landscape reports",
    description: "Generate investor-grade PDF reports in one click. Cited, dated, and ready for the board.",
  },
  {
    icon: Building2,
    title: "Built for legal teams",
    description: "Org workspaces, role-based access, audit logs, Stripe billing. SOC2-ready architecture.",
  },
  {
    icon: Sparkles,
    title: "MCP server for AI agents",
    description: "Plug into Claude, Cursor, or any MCP client. Your legal AI can search patents and analyze infringement directly.",
  },
];

export function Features() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Everything your IP team needs.
          </h2>
          <p className="text-xl text-text-muted max-w-2xl mx-auto">
            Stop juggling 6 different patent tools. One platform, one workflow, one source of truth.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {features.map((f, i) => (
            <Card key={i} className="p-6 hover:border-accent/50 transition-all group">
              <div className="h-12 w-12 rounded-lg bg-gradient-accent/10 border border-accent/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <f.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-text-muted leading-relaxed">{f.description}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
