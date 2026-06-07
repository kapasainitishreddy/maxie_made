import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Card } from "@/components/ui/card";

export default function DocsPage() {
  return (
    <>
      <Topnav />
      <main className="max-w-4xl mx-auto px-6 py-16 space-y-6">
        <div>
          <h1 className="text-4xl font-bold mb-3">API Documentation</h1>
          <p className="text-text-muted">
            REST API for programmatic access to PegWatch data. Available on the API plan ($99/mo).
          </p>
        </div>

        <Card>
          <h2 className="text-xl font-semibold mb-3">Authentication</h2>
          <p className="text-sm text-text-muted mb-3">All requests require a Bearer token:</p>
          <pre className="bg-bg-elevated rounded-lg p-3 text-sm overflow-x-auto">
{`curl -H "Authorization: Bearer YOUR_API_KEY" \\
     https://api.pegwatch.dev/api/v1/peg/status`}
          </pre>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold mb-3">Endpoints</h2>
          <div className="space-y-3 text-sm">
            <div>
              <code className="text-accent">GET /api/v1/stablecoins</code>
              <p className="text-text-muted mt-1">List all stablecoins visible to your tier.</p>
            </div>
            <div>
              <code className="text-accent">GET /api/v1/peg/status</code>
              <p className="text-text-muted mt-1">Current peg status for every active stablecoin.</p>
            </div>
            <div>
              <code className="text-accent">GET /api/v1/peg/&#123;symbol&#125;/status</code>
              <p className="text-text-muted mt-1">Current peg status for one symbol.</p>
            </div>
            <div>
              <code className="text-accent">GET /api/v1/peg/&#123;symbol&#125;/history?hours=168</code>
              <p className="text-text-muted mt-1">Historical price + z-score data (up to 720 hours = 30 days).</p>
            </div>
            <div>
              <code className="text-accent">GET /api/v1/alerts</code>
              <p className="text-text-muted mt-1">Recent depeg incidents across all monitored stables.</p>
            </div>
          </div>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold mb-3">Rate limits</h2>
          <p className="text-sm text-text-muted">
            Free: 60 req/min/IP. Pro: 300 req/min/key. API: 3000 req/min/key.
            Exceeded limits return HTTP 429 with a <code className="text-accent">Retry-After</code> header.
          </p>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold mb-3">Webhooks</h2>
          <p className="text-sm text-text-muted">
            API tier customers can register webhook URLs to receive depeg alerts in real time.
            Payload includes severity, price, z-score, deviation, and an AI-generated summary.
            See the integration guide on our docs portal.
          </p>
        </Card>
      </main>
      <LegalFooter />
    </>
  );
}
