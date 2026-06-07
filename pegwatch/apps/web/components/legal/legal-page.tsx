"use client";

import { Topnav } from "@/components/layout/topnav";
import { LegalFooter } from "@/components/layout/legal-footer";
import { Card } from "@/components/ui/card";

/** Minimal markdown renderer - handles h1-h3, paragraphs, lists, bold, inline code, tables. */
function renderMarkdown(md: string): React.ReactNode[] {
  const lines = md.split("\n");
  const out: React.ReactNode[] = [];
  let inList = false;
  let listItems: string[] = [];
  let inTable = false;
  let tableRows: string[][] = [];

  const flushList = () => {
    if (listItems.length) {
      out.push(
        <ul key={out.length} className="list-disc pl-6 space-y-1 my-3 text-text-muted">
          {listItems.map((item, i) => (
            <li key={i} dangerouslySetInnerHTML={{ __html: inlineMd(item) }} />
          ))}
        </ul>
      );
      listItems = [];
    }
    inList = false;
  };
  const flushTable = () => {
    if (tableRows.length) {
      const [header, ...body] = tableRows;
      out.push(
        <div key={out.length} className="overflow-x-auto my-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                {header.map((h, i) => (
                  <th key={i} className="text-left py-2 px-2 font-semibold" dangerouslySetInnerHTML={{ __html: inlineMd(h.trim()) }} />
                ))}
              </tr>
            </thead>
            <tbody>
              {body.map((row, ri) => (
                <tr key={ri} className="border-b border-border/40">
                  {row.map((cell, ci) => (
                    <td key={ci} className="py-2 px-2 text-text-muted" dangerouslySetInnerHTML={{ __html: inlineMd(cell.trim()) }} />
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      tableRows = [];
    }
    inTable = false;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith("# ")) {
      flushList(); flushTable();
      out.push(<h1 key={out.length} className="text-3xl font-bold mb-2">{trimmed.slice(2)}</h1>);
    } else if (trimmed.startsWith("## ")) {
      flushList(); flushTable();
      out.push(<h2 key={out.length} className="text-2xl font-semibold mt-8 mb-3">{trimmed.slice(3)}</h2>);
    } else if (trimmed.startsWith("### ")) {
      flushList(); flushTable();
      out.push(<h3 key={out.length} className="text-lg font-semibold mt-6 mb-2">{trimmed.slice(4)}</h3>);
    } else if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
      flushTable();
      inList = true;
      listItems.push(trimmed.slice(2));
    } else if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
      flushList();
      inTable = true;
      // Skip separator row |---|---|
      if (/^\|[\s\-:|]+\|$/.test(trimmed)) continue;
      tableRows.push(trimmed.slice(1, -1).split("|"));
    } else if (trimmed === "") {
      flushList(); flushTable();
    } else {
      flushList(); flushTable();
      out.push(<p key={out.length} className="text-text-muted my-3 leading-relaxed" dangerouslySetInnerHTML={{ __html: inlineMd(trimmed) }} />);
    }
  }
  flushList();
  flushTable();
  return out;
}

function inlineMd(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-text font-semibold">$1</strong>')
    .replace(/`([^`]+)`/g, '<code class="bg-bg-elevated px-1.5 py-0.5 rounded text-sm text-accent">$1</code>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-accent hover:underline" target="_blank" rel="noreferrer">$1</a>');
}

export function LegalPage({ title, content, lastUpdated }: { title: string; content: string; lastUpdated?: string }) {
  return (
    <>
      <Topnav />
      <main className="max-w-3xl mx-auto px-6 py-16">
        <Card>
          {lastUpdated && (
            <p className="text-xs text-text-muted mb-2">Last updated: {lastUpdated}</p>
          )}
          <div className="prose-invert">{renderMarkdown(content)}</div>
        </Card>
      </main>
      <LegalFooter />
    </>
  );
}
