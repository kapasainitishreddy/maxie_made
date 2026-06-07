"use client";
import { Logo } from "@/components/brand/logo";
import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";

const NAV_LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/dashboard#savings", label: "Savings" },
];

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="min-h-screen bg-bg text-text">
      <nav className="sticky top-0 z-50 backdrop-blur-md bg-bg/80 border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/"><Logo /></Link>
          <div className="hidden md:flex items-center gap-6 text-sm">
            {NAV_LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="text-text-muted hover:text-text transition-colors">{l.label}</Link>
            ))}
          </div>
          <div className="flex items-center gap-3">
            <Link href="/" className="text-sm text-text-muted hover:text-text">← Back to site</Link>
            <button className="md:hidden p-2" onClick={() => setOpen(!open)} aria-label="Menu">
              {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
        {open && (
          <div className="md:hidden border-t border-border bg-bg-surface">
            {NAV_LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="block px-4 py-3 text-sm text-text-muted hover:text-text" onClick={() => setOpen(false)}>{l.label}</Link>
            ))}
          </div>
        )}
      </nav>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
