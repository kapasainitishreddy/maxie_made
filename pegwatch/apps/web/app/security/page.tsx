import { LegalPage } from "@/components/legal/legal-page";
import { SECURITY_MARKDOWN } from "@/content/legal/pegwatch-security";

export default function SecurityPage() {
  return <LegalPage title="Security Disclosure" content={SECURITY_MARKDOWN} lastUpdated="January 2026" />;
}
