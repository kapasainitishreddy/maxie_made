"use client";
// Simple markdown renderer for legal pages. Supports headers (h1-h3), paragraphs, lists, bold, code, and tables.
// Avoids dependencies (no react-markdown) to keep the bundle small.
import * as React from "react";

export function LegalPage({ markdown }: { markdown: string }) {
  return (
    <article className="container mx-auto px-4 py-16 max-w-3xl prose prose-invert">
      <div className="text-text">
        {markdown.split("\n").map((line, i) => {
          // Headings
          if (line.startsWith("# ")) return <h1 key={i} className="text-4xl font-bold mb-4 mt-8 text-text">{line.slice(2)}</h1>;
          if (line.startsWith("## ")) return <h2 key={i} className="text-2xl font-bold mb-3 mt-8 text-text">{line.slice(3)}</h2>;
          if (line.startsWith("### ")) return <h3 key={i} className="text-xl font-semibold mb-2 mt-6 text-text">{line.slice(4)}</h3>;
          // Lists
          if (line.startsWith("- ")) return <li key={i} className="ml-6 list-disc text-text-muted leading-relaxed">{formatInline(line.slice(2))}</li>;
          if (/^\d+\.\s/.test(line)) return <li key={i} className="ml-6 list-decimal text-text-muted leading-relaxed">{formatInline(line.replace(/^\d+\.\s/, ""))}</li>;
          if (line.startsWith("| ")) return <div key={i} className="font-mono text-xs text-text-muted py-0.5">{line}</div>;
          // Tables (simple)
          if (line.startsWith("|---")) return null;
          // Bold + code inline
          if (line.trim() === "") return <br key={i} />;
          return <p key={i} className="text-text-muted leading-relaxed mb-3">{formatInline(line)}</p>;
        })}
      </div>
    </article>
  );
}

function formatInline(text: string): React.ReactNode {
  // Bold **text**
  const parts: React.ReactNode[] = [];
  const regex = /\*\*([^*]+)\*\*|`([^`]+)`/g;
  let lastIdx = 0;
  let m;
  let k = 0;
  while ((m = regex.exec(text)) !== null) {
    if (m.index > lastIdx) parts.push(text.slice(lastIdx, m.index));
    if (m[1]) parts.push(<strong key={k++} className="text-text font-semibold">{m[1]}</strong>);
    else if (m[2]) parts.push(<code key={k++} className="px-1.5 py-0.5 rounded bg-bg-elevated text-accent text-sm font-mono">{m[2]}</code>);
    lastIdx = m.index + m[0].length;
  }
  if (lastIdx < text.length) parts.push(text.slice(lastIdx));
  return <>{parts}</>;
}
