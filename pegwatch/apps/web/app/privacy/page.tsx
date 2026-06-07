import { LegalPage } from "@/components/legal/legal-page";
import { PRIVACY_MARKDOWN } from "@/content/legal/pegwatch-privacy";

export default function PrivacyPage() {
  return <LegalPage title="Privacy Policy" content={PRIVACY_MARKDOWN} lastUpdated="January 2026" />;
}
