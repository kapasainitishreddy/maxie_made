"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  Map as MapIcon,
  AlertTriangle,
  BarChart3,
  Settings,
  Activity,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { UserButton } from "@clerk/nextjs";

const hasClerk = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

const nav = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/patents", label: "Patents", icon: FileText },
  { href: "/landscapes", label: "Landscapes", icon: MapIcon },
  { href: "/infringement", label: "Infringement", icon: AlertTriangle },
  { href: "/reports", label: "Reports", icon: BarChart3 },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="hidden md:flex md:w-64 border-r border-border bg-bg-surface/40 backdrop-blur-md flex-col">
      <div className="h-16 flex items-center gap-2 px-6 border-b border-border">
        <div className="h-8 w-8 rounded-lg bg-gradient-accent flex items-center justify-center">
          <Activity className="h-5 w-5 text-white" />
        </div>
        <span className="font-bold">PharmaIP</span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {nav.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all",
                active
                  ? "bg-gradient-accent/10 text-accent border border-accent/20"
                  : "text-text-muted hover:bg-bg-elevated hover:text-text"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-border flex items-center gap-3">
        {hasClerk ? <UserButton afterSignOutUrl="/" /> : <Link href="/sign-in" className="text-xs text-text-muted hover:text-text">Sign in</Link>}
        <div className="text-xs text-text-muted">Your account</div>
      </div>
    </aside>
  );
}
