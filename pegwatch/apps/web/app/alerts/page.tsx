"use client";

import { useEffect, useState } from "react";
import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api, type Alert } from "@/lib/api";
import { formatPct, formatZ, formatUSD } from "@/lib/utils";
import { Bell, Plus, Trash2, AlertCircle, CheckCircle2, XCircle } from "lucide-react";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [addingChannel, setAddingChannel] = useState(false);
  const [channelType, setChannelType] = useState<"telegram" | "discord" | "webhook" | "email">("telegram");
  const [target, setTarget] = useState("");

  async function load() {
    try {
      const data = await api.listAlerts();
      setAlerts(data);
    } catch {
      // Free tier can't list alerts - that's fine
      setAlerts([]);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <>
      <Topnav />
      <main className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">Alerts</h1>
            <p className="text-text-muted text-sm mt-1">Global incident feed and notification channels</p>
          </div>
          <Button onClick={() => setAddingChannel(!addingChannel)}>
            <Plus className="w-4 h-4" />
            Add channel
          </Button>
        </div>

        {addingChannel && (
          <Card className="mb-6">
            <h3 className="font-semibold mb-3">New notification channel</h3>
            <div className="grid md:grid-cols-3 gap-3">
              <div>
                <label className="text-xs text-text-muted block mb-1">Channel</label>
                <select
                  value={channelType}
                  onChange={(e) => setChannelType(e.target.value as typeof channelType)}
                  className="w-full bg-bg-elevated border border-border rounded-lg px-3 py-2 text-sm"
                >
                  <option value="telegram">Telegram</option>
                  <option value="discord">Discord</option>
                  <option value="email">Email</option>
                  <option value="webhook">Webhook</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="text-xs text-text-muted block mb-1">
                  {channelType === "email" ? "Email address" : channelType === "webhook" ? "Webhook URL" : "Chat ID / webhook"}
                </label>
                <input
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  placeholder={
                    channelType === "email" ? "ops@treasury.com" :
                    channelType === "webhook" ? "https://hooks.slack.com/..." :
                    channelType === "telegram" ? "123456789" :
                    "https://discord.com/api/webhooks/..."
                  }
                  className="w-full bg-bg-elevated border border-border rounded-lg px-3 py-2 text-sm"
                />
              </div>
            </div>
            <p className="text-xs text-text-muted mt-3">
              Channels require a Pro subscription. Save flow goes through Stripe checkout.
            </p>
            <div className="flex gap-2 mt-4">
              <Button size="sm" onClick={() => alert("Upgrade to Pro to add channels (this is a demo)")}>
                Save channel
              </Button>
              <Button size="sm" variant="ghost" onClick={() => setAddingChannel(false)}>
                Cancel
              </Button>
            </div>
          </Card>
        )}

        <Card className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <h2 className="font-semibold flex items-center gap-2">
              <Bell className="w-4 h-4" />
              Recent incidents
            </h2>
            <Badge variant="info">{alerts.length} total</Badge>
          </div>
          <p className="text-sm text-text-muted">
            Incidents fire automatically when a stablecoin's z-score crosses the warning threshold.
            In dev mode, trigger one manually by clicking "Refresh" on a stablecoin with a synthetic depeg.
          </p>
        </Card>

        {alerts.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <CheckCircle2 className="w-12 h-12 text-ok mx-auto mb-3" />
              <h3 className="font-semibold mb-1">No active alerts</h3>
              <p className="text-sm text-text-muted">
                All monitored stablecoins are within their normal peg range. PegWatch will alert you the moment
                that changes.
              </p>
            </div>
          </Card>
        ) : (
          <div className="space-y-3">
            {alerts.map((a) => (
              <Card key={a.id} className={a.severity === "critical" ? "border-crit/30" : a.severity === "warning" ? "border-warn/30" : ""}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant={a.severity === "critical" ? "critical" : a.severity === "warning" ? "warning" : "info"}>
                        {a.severity}
                      </Badge>
                      <h3 className="font-semibold">{a.title}</h3>
                    </div>
                    <div className="grid grid-cols-3 gap-3 my-3 text-sm">
                      <div>
                        <div className="text-xs text-text-muted">Price</div>
                        <div className="font-mono font-bold">{formatUSD(a.price_at_trigger)}</div>
                      </div>
                      <div>
                        <div className="text-xs text-text-muted">Deviation</div>
                        <div className="font-mono font-bold">{formatPct(a.deviation_pct)}</div>
                      </div>
                      <div>
                        <div className="text-xs text-text-muted">Z-score</div>
                        <div className="font-mono font-bold">{formatZ(a.z_score)}</div>
                      </div>
                    </div>
                    {a.ai_summary && (
                      <div className="bg-bg/50 border border-border/40 rounded-lg p-3 mt-3 text-sm">
                        <div className="text-xs text-text-muted mb-1 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" /> AI summary
                        </div>
                        {a.ai_summary}
                      </div>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-text-muted">{new Date(a.triggered_at).toLocaleString()}</div>
                    {a.resolved && <Badge variant="success" className="mt-2">Resolved</Badge>}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>
      <LegalFooter />
    </>
  );
}
