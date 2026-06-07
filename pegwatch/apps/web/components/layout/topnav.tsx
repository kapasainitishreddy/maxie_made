import Link from "next/link";
import { Logo } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";

export function Topnav() {
  return (
    <header className="sticky top-0 z-50 border-b border-border/40 glass">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="hover:opacity-80 transition">
          <Logo />
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          <Link href="/dashboard" className="px-3 py-2 text-sm text-text-muted hover:text-text transition">
            Monitor
          </Link>
          <Link href="/alerts" className="px-3 py-2 text-sm text-text-muted hover:text-text transition">
            Alerts
          </Link>
          <Link href="/pricing" className="px-3 py-2 text-sm text-text-muted hover:text-text transition">
            Pricing
          </Link>
          <Link href="/docs" className="px-3 py-2 text-sm text-text-muted hover:text-text transition">
            Docs
          </Link>
        </nav>
        <div className="flex items-center gap-2">
          <Link href="/dashboard">
            <Button size="sm" variant="ghost">Sign in</Button>
          </Link>
          <Link href="/dashboard">
            <Button size="sm">Open Dashboard</Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
