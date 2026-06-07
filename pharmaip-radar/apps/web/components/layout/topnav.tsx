import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/brand/logo";

export function TopNav() {
  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-bg/80 border-b border-border">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/">
          <Logo />
        </Link>

        <div className="hidden md:flex items-center gap-6 text-sm">
          <Link href="/pricing" className="text-text-muted hover:text-text transition-colors">Pricing</Link>
          <Link href="/#features" className="text-text-muted hover:text-text transition-colors">Features</Link>
          <Link href="/#scenario" className="text-text-muted hover:text-text transition-colors">Case study</Link>
          <Link href="/#faq" className="text-text-muted hover:text-text transition-colors">FAQ</Link>
        </div>

        <div className="flex items-center gap-3">
          <Button asChild variant="ghost" size="sm">
            <Link href="/sign-in">Sign in</Link>
          </Button>
          <Button asChild size="sm">
            <Link href="/sign-up">Get started</Link>
          </Button>
        </div>
      </div>
    </nav>
  );
}
