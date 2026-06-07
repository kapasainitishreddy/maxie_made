"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ManageSubscriptionButton } from "@/components/billing/manage-subscription-button";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface Plan {
  id: string;
  name: string;
  price?: number;
  price_usd?: number;
}

export default function SettingsPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [currentPlan, setCurrentPlan] = useState<string>("free");

  useEffect(() => {
    api.get<Plan[]>("/billing/plans")
      .then(setPlans)
      .catch(() => setPlans([]));
  }, []);

  const current = plans.find((p) => p.id === currentPlan);
  const price = current?.price ?? current?.price_usd ?? 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-text-muted">Manage your account and subscription</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Subscription</CardTitle>
          <p className="text-sm text-text-muted">Your current plan</p>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center rounded-full bg-gradient-accent px-3 py-1 text-xs font-semibold text-white">
              {current?.name ?? "Free"}
            </span>
            {price > 0 && (
              <span className="text-sm text-text-muted">${price}/mo</span>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Billing</CardTitle>
          <p className="text-sm text-text-muted">
            Update card, change plan, or cancel
          </p>
        </CardHeader>
        <CardContent>
          <ManageSubscriptionButton />
        </CardContent>
      </Card>
    </div>
  );
}
