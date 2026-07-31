"""Minimal, dependency-light Markdown -> PDF for the Zenodo v2 submission.

Uses reportlab only (no pandoc/LaTeX in this environment). Handles the subset of
Markdown these documents use: ATX headings, paragraphs with **bold**/`code`/
[text](url), fenced code blocks, pipe tables, horizontal rules, blockquotes, and
- bullet / 1. numbered lists.

Fonts are registered from the system so math glyphs (Delta, minus sign, >=, ^2,
approx) render instead of dropping to boxes.

Usage:  python work/md_to_pdf.py INPUT.md OUTPUT.pdf ["Optional title"]
"""

import re
import sys
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle,
    HRFlowable,
)

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Body", F + "arial.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", F + "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", F + "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "consola.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", F + "consolab.ttf"))
pdfmetrics.registerFontFamily(
    "Body", normal="Body", bold="Body-Bold", italic="Body-Italic",
    boldItalic="Body-Bold",
)

styles = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=styles["Normal"], fontName="Body",
                      fontSize=9.5, leading=13.5, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Body-Bold", fontSize=16,
                    leading=20, spaceBefore=6, spaceAfter=10)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Body-Bold", fontSize=12.5,
                    leading=16, spaceBefore=12, spaceAfter=6)
H3 = ParagraphStyle("h3", parent=BODY, fontName="Body-Bold", fontSize=10.5,
                    leading=14, spaceBefore=9, spaceAfter=4)
QUOTE = ParagraphStyle("quote", parent=BODY, leftIndent=14, textColor=colors.HexColor("#333333"),
                       fontName="Body-Italic", borderPadding=0)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.5, leading=11, spaceAfter=0)
CELL_H = ParagraphStyle("cellh", parent=CELL, fontName="Body-Bold")
CODE = ParagraphStyle("code", parent=styles["Code"], fontName="Mono",
                      fontSize=8, leading=10.5, backColor=colors.HexColor("#f4f4f4"),
                      borderPadding=6, spaceBefore=4, spaceAfter=8, leftIndent=4)


def inline(text: str) -> str:
    """Markdown inline -> reportlab mini-HTML. Escapes first, then re-applies tags."""
    text = html.escape(text)
    # inline code first (protect its contents from bold/link parsing is not needed here)
    text = re.sub(r"`([^`]+)`", r'<font face="Mono" size="8.5">\1</font>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" color="#1a5fb4">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def flush_table(rows, story):
    if not rows:
        return
    # drop the |---|---| separator row
    body = [r for r in rows if not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", "|".join(r))]
    header, data = body[0], body[1:]
    tdata = [[Paragraph(inline(c), CELL_H) for c in header]]
    for r in data:
        tdata.append([Paragraph(inline(c), CELL) for c in r])
    ncol = len(header)
    t = Table(tdata, repeatRows=1, colWidths=[(17.0 / ncol) * cm] * ncol)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ececec")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))


def parse(md: str):
    story = []
    lines = md.split("\n")
    i = 0
    table_rows = []
    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            flush_table(table_rows, story); table_rows = []
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i]); i += 1
            story.append(Preformatted("\n".join(block), CODE))
            i += 1
            continue

        if line.lstrip().startswith("|") and "|" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table(table_rows, story); table_rows = []

        if re.match(r"^#\s", line):
            story.append(Paragraph(inline(line[2:].strip()), H1))
        elif re.match(r"^##\s", line):
            story.append(Paragraph(inline(line[3:].strip()), H2))
        elif re.match(r"^###\s", line):
            story.append(Paragraph(inline(line[4:].strip()), H3))
        elif re.match(r"^---+\s*$", line) or re.match(r"^===+\s*$", line):
            story.append(HRFlowable(width="100%", thickness=0.6,
                                    color=colors.HexColor("#cccccc"),
                                    spaceBefore=6, spaceAfter=8))
        elif line.strip().startswith(">"):
            story.append(Paragraph(inline(line.strip()[1:].strip()), QUOTE))
        elif re.match(r"^\s*[-*]\s+", line):
            story.append(Paragraph("&bull;&nbsp;" + inline(re.sub(r"^\s*[-*]\s+", "", line)),
                                   ParagraphStyle("li", parent=BODY, leftIndent=12, spaceAfter=3)))
        elif re.match(r"^\s*\d+\.\s+", line):
            story.append(Paragraph(inline(line.strip()),
                                   ParagraphStyle("oli", parent=BODY, leftIndent=12, spaceAfter=3)))
        elif line.strip() == "":
            pass
        else:
            story.append(Paragraph(inline(line.strip()), BODY))
        i += 1

    flush_table(table_rows, story)
    return story


def build(inp, outp):
    md = open(inp, encoding="utf-8").read()
    doc = SimpleDocTemplate(outp, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                            title=inp)
    doc.build(parse(md))
    print("wrote", outp)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
