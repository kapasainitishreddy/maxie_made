import { LegalPage } from "@/components/legal/legal-page";
import { TERMS_MARKDOWN } from "@/content/legal/pegwatch-terms";

export default function TermsPage() {
  return <LegalPage title="Terms of Service" content={TERMS_MARKDOWN} lastUpdated="January 2026" />;
}
