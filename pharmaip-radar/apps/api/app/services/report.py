"""PDF report builder (reportlab)."""

from __future__ import annotations

import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class ReportBuilder:
    def __init__(self) -> None:
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name="TitleX",
            parent=self.styles["Title"],
            fontSize=24,
            spaceAfter=20,
        ))
        self.styles.add(ParagraphStyle(
            name="H2X",
            parent=self.styles["Heading2"],
            fontSize=14,
            spaceBefore=14,
            spaceAfter=8,
            textColor=colors.HexColor("#1e40af"),
        ))

    def _to_para(self, text: str) -> Paragraph:
        safe = (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return Paragraph(safe, self.styles["BodyText"])

    def build_fto_report(
        self,
        title: str,
        target_drug: str | None,
        landscape: dict,
        alerts: list[dict],
    ) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, title=title)
        story = []

        story.append(Paragraph(title, self.styles["TitleX"]))
        story.append(Paragraph(
            f"Generated {_now_utc().strftime('%Y-%m-%d %H:%M UTC')}",
            self.styles["Italic"],
        ))
        story.append(Spacer(1, 0.2 * inch))

        if target_drug:
            story.append(Paragraph(f"Target: <b>{target_drug}</b>", self.styles["BodyText"]))
            story.append(Spacer(1, 0.1 * inch))

        # Executive summary
        story.append(Paragraph("Executive Summary", self.styles["H2X"]))
        total = landscape.get("total_patents", 0)
        unique = landscape.get("unique_assignees", 0)
        summary_text = (
            f"Freedom-to-Operate analysis covering {total} patents from {unique} unique assignees. "
        )
        if alerts:
            summary_text += (
                f"<b>{len(alerts)} potential infringement alert(s)</b> identified. "
                f"Highest risk score: {max((a.get('risk_score', 0) for a in alerts), default=0):.2f}."
            )
        else:
            summary_text += "No high-risk infringement vectors identified at this time."
        story.append(self._to_para(summary_text))
        story.append(Spacer(1, 0.2 * inch))

        # Top assignees
        story.append(Paragraph("Top Assignees", self.styles["H2X"]))
        assignees = landscape.get("top_assignees", [])
        if assignees:
            data = [["Assignee", "Patents", "Share"]]
            for a in assignees[:10]:
                data.append([
                    a["assignee"][:40],
                    str(a["patent_count"]),
                    f"{a['market_share'] * 100:.1f}%",
                ])
            t = Table(data, colWidths=[3.5 * inch, 1 * inch, 1 * inch])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]))
            story.append(t)
        else:
            story.append(self._to_para("No assignee data available."))

        # Infringement alerts
        if alerts:
            story.append(PageBreak())
            story.append(Paragraph("Infringement Alerts", self.styles["H2X"]))
            for a in alerts[:10]:
                story.append(self._to_para(
                    f"<b>Risk {a.get('risk_score', 0):.2f} ({a.get('severity', 'unknown')})</b>"
                ))
                if a.get("summary"):
                    story.append(self._to_para(a["summary"]))
                story.append(Spacer(1, 0.1 * inch))

        # White space
        story.append(PageBreak())
        story.append(Paragraph("White Space Opportunities", self.styles["H2X"]))
        ws = landscape.get("white_space", [])
        if ws:
            story.append(self._to_para(
                f"Years with below-average filing activity: {', '.join(ws)}. "
                "These may represent opportunities for novel IP."
            ))
        else:
            story.append(self._to_para(
                "Filing activity is consistent across years. No clear white space identified."
            ))

        doc.build(story)
        return buf.getvalue()

    def build_infringement_report(self, title: str, target_patent: dict, assessment: dict) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, title=title)
        story = []
        story.append(Paragraph(title, self.styles["TitleX"]))
        story.append(Paragraph(
            f"Generated {_now_utc().strftime('%Y-%m-%d %H:%M UTC')}",
            self.styles["Italic"],
        ))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Target Patent", self.styles["H2X"]))
        story.append(self._to_para(f"<b>{target_patent.get('title', '')}</b>"))
        story.append(self._to_para(
            f"{target_patent.get('patent_number', '')} ({target_patent.get('jurisdiction', '')})"
        ))
        story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Risk Assessment", self.styles["H2X"]))
        sev = assessment.get("severity", "low")
        risk = assessment.get("risk_score", 0)
        story.append(self._to_para(
            f"<b>Overall risk score: {risk:.2f} ({sev.upper()})</b>"
        ))

        chart = assessment.get("claim_chart", [])
        if chart:
            data = [["Claim #", "Overall", "Cosine", "Element Overlap"]]
            for c in chart[:15]:
                data.append([
                    str(c["claim_number"]),
                    f"{c['overall_similarity']:.2f}",
                    f"{c['cosine']:.2f}",
                    f"{c['element_overlap']:.2f}",
                ])
            t = Table(data, colWidths=[1 * inch, 1.2 * inch, 1.2 * inch, 1.5 * inch])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]))
            story.append(t)

        doc.build(story)
        return buf.getvalue()
