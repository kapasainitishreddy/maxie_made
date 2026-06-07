import Link from "next/link";

export function LegalFooter() {
  return (
    <footer className="border-t border-border py-8 mt-16">
      <div className="container mx-auto px-4 text-center text-sm text-text-muted space-y-2">
        <div className="flex justify-center gap-6">
          <Link href="/privacy" className="hover:text-text">Privacy</Link>
          <Link href="/terms" className="hover:text-text">Terms</Link>
          <Link href="/security" className="hover:text-text">Security</Link>
        </div>
        <div>© 2026 PharmaIP Radar · All rights reserved</div>
      </div>
    </footer>
  );
}
