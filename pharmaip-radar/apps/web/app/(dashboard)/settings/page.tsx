import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ManageSubscriptionButton } from "@/components/billing/manage-subscription-button";

export default function SettingsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-text-muted">Manage your org and billing</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Organization</CardTitle>
          <CardDescription>Your pharma IP workspace</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-1.5 block">Organization name</label>
            <Input defaultValue="Demo Pharma Corp" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Subscription</label>
            <div className="flex items-center gap-2">
              <Badge variant="default" className="bg-gradient-accent">Pro</Badge>
              <span className="text-sm text-text-muted">$2,499/month</span>
            </div>
          </div>
          <Button>Save changes</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Billing</CardTitle>
          <CardDescription>Manage your subscription via Stripe</CardDescription>
        </CardHeader>
        <CardContent>
          <ManageSubscriptionButton />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Danger zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="destructive">Delete organization</Button>
        </CardContent>
      </Card>
    </div>
  );
}
