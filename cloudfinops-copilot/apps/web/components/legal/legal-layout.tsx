"use client";
import { TopNav } from "@/components/layout/topnav";
import { Logo } from "@/components/brand/logo";

export function LegalPageLayout({ title, lastUpdated, children }: { title: string; lastUpdated: string; children: React.ReactNode }) {
  return (
    <>
      <TopNav />
      <main className="container mx-auto px-4 py-12 max-w-3xl">
        <div className="mb-8">
          <Logo />
        </div>
        <h1 className="text-4xl font-bold mb-2">{title}</h1>
        <p className="text-sm text-text-muted mb-8">Last updated: {lastUpdated}</p>
        <div className="prose prose-invert max-w-none space-y-6 text-text-muted leading-relaxed [&_h2]:text-2xl [&_h2]:font-semibold [&_h2]:text-text [&_h2]:mt-8 [&_h2]:mb-3 [&_h3]:text-lg [&_h3]:font-semibold [&_h3]:text-text [&_h3]:mt-6 [&_h3]:mb-2 [&_a]:text-accent [&_a]:underline [&_ul]:list-disc [&_ul]:ml-6 [&_ul]:space-y-1">
          {children}
        </div>
        <footer className="border-t border-border mt-16 pt-8 text-sm text-text-muted">
          © 2026 Maxie Made, Inc. · All rights reserved.
        </footer>
      </main>
    </>
  );
}
