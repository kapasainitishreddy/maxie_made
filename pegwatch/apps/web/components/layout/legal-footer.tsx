import Link from "next/link";

export function LegalFooter() {
  return (
    <footer className="border-t border-border/40 mt-20">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 className="font-semibold mb-3">PegWatch</h4>
            <p className="text-sm text-text-muted">
              Statistical stablecoin depeg early-warning. Open source. Free tier.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-sm">Product</h4>
            <div className="flex flex-col gap-2 text-sm text-text-muted">
              <Link href="/dashboard" className="hover:text-text">Monitor</Link>
              <Link href="/alerts" className="hover:text-text">Alerts</Link>
              <Link href="/pricing" className="hover:text-text">Pricing</Link>
              <Link href="/docs" className="hover:text-text">API Docs</Link>
            </div>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-sm">Company</h4>
            <div className="flex flex-col gap-2 text-sm text-text-muted">
              <Link href="/about" className="hover:text-text">About</Link>
              <Link href="/contact" className="hover:text-text">Contact</Link>
              <a href="https://github.com/kapasainitishreddy/pegwatch" className="hover:text-text" target="_blank" rel="noreferrer">GitHub</a>
            </div>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-sm">Legal</h4>
            <div className="flex flex-col gap-2 text-sm text-text-muted">
              <Link href="/privacy" className="hover:text-text">Privacy</Link>
              <Link href="/terms" className="hover:text-text">Terms</Link>
              <Link href="/security" className="hover:text-text">Security</Link>
            </div>
          </div>
        </div>
        <div className="pt-6 border-t border-border/40 flex flex-col md:flex-row justify-between gap-4 text-xs text-text-muted">
          <p>© {new Date().getFullYear()} PegWatch. Not financial advice. Not affiliated with Circle, Tether, MakerDAO, or any stablecoin issuer.</p>
          <p>PegWatch is not a broker-dealer, exchange, or custodian.</p>
        </div>
      </div>
    </footer>
  );
}
