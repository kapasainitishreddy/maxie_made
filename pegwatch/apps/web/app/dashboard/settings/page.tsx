"use client";

import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ManageSubscriptionButton } from "@/components/billing/manage-subscription-button";
import { useEffect, useState } from "react";
import { api, type Plan } from "@/lib/api";

export default function SettingsPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [currentPlan, setCurrentPlan] = useState<string>("free");

  useEffect(() => {
    api.plans().then(setPlans).catch(() => setPlans([]));
  }, []);

  const current = plans.find((p) => p.id === currentPlan);
  const price = current?.price_usd ?? 0;

  return (
    <div className="space-y-6 max-w-3xl mx-auto p-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-text-muted">Manage your account and subscription</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Subscription</CardTitle>
          <CardDescription>Your current plan</CardDescription>
        </CardHeader>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <Badge variant="info">{current?.name ?? "Free"}</Badge>
            {price > 0 && (
              <span className="text-sm text-text-muted">${price}/mo</span>
            )}
          </div>
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Billing</CardTitle>
          <CardDescription>Update card, change plan, or cancel</CardDescription>
        </CardHeader>
        <ManageSubscriptionButton />
      </Card>
    </div>
  );
}
