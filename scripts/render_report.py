"""Render the editable QMD narrative to a styled PDF without requiring Quarto."""
from __future__ import annotations
from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "organoid_transplantation_evidence_mapping.qmd"
OUTPUT = ROOT / "reports" / "organoid_transplantation_evidence_mapping.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#123B5D"), spaceAfter=18))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#42677F"), spaceAfter=22))
styles.add(ParagraphStyle(name="Author", parent=styles["Normal"], fontSize=11, leading=17, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="FigureCaption", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#526B7A"), spaceBefore=3, spaceAfter=5))
styles.add(ParagraphStyle(name="Reference", parent=styles["BodyText"], fontSize=7.4, leading=9.2, spaceAfter=2.2))
styles["Heading1"].textColor = colors.HexColor("#123B5D"); styles["Heading1"].spaceBefore = 12; styles["Heading1"].spaceAfter = 8
styles["BodyText"].fontSize = 9.3; styles["BodyText"].leading = 13.2; styles["BodyText"].spaceAfter = 7

def header_footer(canvas, doc):
    canvas.saveState(); width, height = A4
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#B8C9D6")); canvas.line(20*mm, height-16*mm, width-20*mm, height-16*mm)
        canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#526B7A"))
        canvas.drawString(20*mm, height-12*mm, "Organoid Transplantation Evidence Mapping")
        canvas.drawRightString(width-20*mm, 11*mm, f"{doc.page}")
    canvas.restoreState()

text = SOURCE.read_text(encoding="utf-8")
body = re.sub(r"\A---.*?---\s*", "", text, flags=re.S)
story = [Spacer(1, 34*mm), Paragraph("Organoid Transplantation Research Landscape and Translational Applications", styles["ReportTitle"]), Paragraph("A Reproducible Computational Evidence-Mapping Study of Organoid Engraftment, Regenerative Medicine and Translational Readiness", styles["Subtitle"]), Spacer(1, 16*mm), Paragraph("<b>Tharuniya Anpalakan</b><br/>Department of Applied Sciences<br/>Northumbria University<br/>Newcastle upon Tyne, United Kingdom<br/>w25070895@northumbria.ac.lk", styles["Author"]), Spacer(1, 28*mm), Paragraph("Computational research report · 18 October 2026<br/><i>Independent report; not peer reviewed</i>", styles["Author"]), PageBreak()]

paragraphs: list[str] = []
def flush():
    global paragraphs
    if paragraphs:
        cleaned = " ".join(p.strip() for p in paragraphs)
        cleaned = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", cleaned)
        paragraph_style = styles["Reference"] if re.match(r"^\d+\.\s", cleaned) else styles["BodyText"]
        story.append(Paragraph(cleaned, paragraph_style)); paragraphs = []

for line in body.splitlines():
    if line.startswith("# "):
        flush(); story.append(Paragraph(line[2:].strip(), styles["Heading1"]))
    elif line.startswith("!["):
        flush(); match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if match:
            image_path = (SOURCE.parent / match.group(2)).resolve()
            if image_path.exists():
                img = Image(str(image_path)); img._restrictSize(165*mm, 110*mm)
                story.extend([KeepTogether([img, Paragraph(f"<i>{match.group(1)}</i>", styles["FigureCaption"])]), Spacer(1, 5*mm)])
    elif not line.strip():
        flush()
    else:
        paragraphs.append(line)
flush()

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=21*mm, bottomMargin=18*mm, title="Organoid Transplantation Research Landscape and Translational Applications", author="Tharuniya Anpalakan")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Rendered {OUTPUT}")

