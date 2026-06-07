// Privacy-first analytics via Plausible. No cookies, no PII.
// Set NEXT_PUBLIC_PLAUSIBLE_DOMAIN to enable. Disabled in dev when env var is missing.
export function Plausible() {
  const domain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;
  if (!domain) return null;
  return (
    <script
      defer
      data-domain={domain}
      src="https://plausible.io/js/script.js"
      strategy="afterInteractive"
    />
  );
}
