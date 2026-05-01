#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["reportlab>=4.0"]
# ///
"""Generate a professionally formatted PDF resume directly from structured JSON data.

Usage:
  uv run export_pdf.py <cv_data.json> [--output <filename.pdf>]
  python export_pdf.py <cv_data.json> [--output <filename.pdf>]

Generates PDF using ReportLab — no Word, LibreOffice, or other external tools
required. Calibri is used if available on the system; Helvetica is the fallback.

The JSON input schema is defined in skills/cv-export/SKILL.md.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate


# ---------------------------------------------------------------------------
# Formatting constants (mirrored from export_docx.py)
# ---------------------------------------------------------------------------

# Page: A4 with narrow margins
MARGIN_TOP = 1.27 * cm
MARGIN_BOTTOM = 1.27 * cm
MARGIN_LEFT = 1.693 * cm
MARGIN_RIGHT = 1.693 * cm

# Font sizes (points)
SIZE_NAME = 20
SIZE_CONTACT = 8.5
SIZE_SECTION_HEADING = 10
SIZE_SUMMARY_BODY = 9
SIZE_TECH_SKILL = 8.5
SIZE_JOB_TITLE = 9
SIZE_COMPANY_LINE = 8
SIZE_BULLET = 8.5
SIZE_EDUCATION_TITLE = 8.5
SIZE_EDUCATION_SUBTITLE = 8
SIZE_EDUCATION_DETAIL = 8
SIZE_CERT = 8

# Colors
COLOR_NAME = HexColor("#1A1A1A")
COLOR_CONTACT = HexColor("#555555")
COLOR_HEADING = HexColor("#24292F")
COLOR_JOB_TITLE = HexColor("#1A1A1A")
COLOR_COMPANY = HexColor("#888888")
COLOR_BLACK = HexColor("#000000")
COLOR_BORDER = HexColor("#C8C8C8")

# Spacing (points)
SP_NAME_AFTER = 3
SP_CONTACT_AFTER = 1
SP_LANGUAGES_AFTER = 4
SP_HEADING_BEFORE = 10
SP_HEADING_AFTER = 3
SP_SUMMARY_AFTER = 2
SP_TECH_AFTER = 1
SP_JOB_TITLE_BEFORE = 5
SP_JOB_TITLE_AFTER = 1
SP_COMPANY_AFTER = 2
SP_BULLET_AFTER = 2
SP_EDU_TITLE_BEFORE = 4
SP_EDU_TITLE_AFTER = 1
SP_EDU_SUB_AFTER = 1
SP_CERT_AFTER = 1

# Bullet indent (matching DOCX: left=0.635cm, hanging=0.424cm)
BULLET_LEFT_INDENT = 0.635 * cm
BULLET_HANGING = 0.424 * cm


# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------

def _find_file(candidates):
    for p in candidates:
        if Path(p).exists():
            return p
    return None


def register_fonts():
    """Register Calibri TTF from system paths if available.

    Returns (regular_name, bold_name) — either Calibri variants or Helvetica.
    """
    base_paths = [
        "/Library/Fonts/Calibri.ttf",
        os.path.expanduser("~/Library/Fonts/Calibri.ttf"),
        "/Library/Fonts/Microsoft/Calibri.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/calibri.ttf",
        os.path.expanduser("~/.local/share/fonts/Calibri.ttf"),
    ]
    bold_paths = [
        p.replace("Calibri.ttf", "Calibrib.ttf").replace("calibri.ttf", "calibrib.ttf")
        for p in base_paths
    ]

    regular = _find_file(base_paths)
    bold = _find_file(bold_paths)

    if regular:
        try:
            pdfmetrics.registerFont(TTFont("Calibri", regular))
            pdfmetrics.registerFont(TTFont("Calibri-Bold", bold or regular))
            return "Calibri", "Calibri-Bold"
        except Exception as e:
            print(f"Note: Could not register Calibri ({e}). Using Helvetica.", file=sys.stderr)

    print("Note: Calibri not found on this system. Using Helvetica as fallback.", file=sys.stderr)
    return "Helvetica", "Helvetica-Bold"


# ---------------------------------------------------------------------------
# Style factory
# ---------------------------------------------------------------------------

def _style(name, font, bold_font, size, bold=False, color=None,
           alignment=TA_LEFT, space_before=0, space_after=0,
           left_indent=0, first_line_indent=0):
    return ParagraphStyle(
        name=name,
        fontName=bold_font if bold else font,
        fontSize=size,
        textColor=color or COLOR_BLACK,
        alignment=alignment,
        spaceBefore=space_before,
        spaceAfter=space_after,
        leading=round(size * 1.2, 1),
        leftIndent=left_indent,
        firstLineIndent=first_line_indent,
        wordWrap="LTR",
    )


def build_styles(font, bold_font):
    s = lambda n, size, **kw: _style(n, font, bold_font, size, **kw)
    return {
        "name":       s("name", SIZE_NAME, bold=True, color=COLOR_NAME,
                         space_after=SP_NAME_AFTER),
        "contact":    s("contact", SIZE_CONTACT, color=COLOR_CONTACT,
                         space_after=SP_CONTACT_AFTER),
        "languages":  s("languages", SIZE_CONTACT, color=COLOR_CONTACT,
                         space_after=SP_LANGUAGES_AFTER),
        "heading":    s("heading", SIZE_SECTION_HEADING, bold=True, color=COLOR_HEADING,
                         space_before=SP_HEADING_BEFORE, space_after=2),
        "summary":    s("summary", SIZE_SUMMARY_BODY, alignment=TA_JUSTIFY,
                         space_after=SP_SUMMARY_AFTER),
        "tech":       s("tech", SIZE_TECH_SKILL, space_after=SP_TECH_AFTER),
        "job_title":  s("job_title", SIZE_JOB_TITLE, bold=True, color=COLOR_JOB_TITLE,
                         space_before=SP_JOB_TITLE_BEFORE, space_after=SP_JOB_TITLE_AFTER),
        "company":    s("company", SIZE_COMPANY_LINE, color=COLOR_COMPANY,
                         space_after=SP_COMPANY_AFTER),
        "bullet":     s("bullet", SIZE_BULLET, space_after=SP_BULLET_AFTER,
                         left_indent=BULLET_LEFT_INDENT,
                         first_line_indent=-BULLET_HANGING),
        "edu_title":  s("edu_title", SIZE_EDUCATION_TITLE, bold=True, color=COLOR_JOB_TITLE,
                         space_before=SP_EDU_TITLE_BEFORE, space_after=SP_EDU_TITLE_AFTER),
        "edu_sub":    s("edu_sub", SIZE_EDUCATION_SUBTITLE, color=COLOR_COMPANY,
                         space_after=SP_EDU_SUB_AFTER),
        "edu_detail": s("edu_detail", SIZE_EDUCATION_DETAIL, space_after=SP_EDU_SUB_AFTER),
        "cert":       s("cert", SIZE_CERT, space_after=SP_CERT_AFTER),
    }


# ---------------------------------------------------------------------------
# Flowable helpers
# ---------------------------------------------------------------------------

def _x(text):
    """Escape text for use inside ReportLab XML markup."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def section_heading(text, st):
    """Return a KeepTogether([heading paragraph, thin HR rule])."""
    para = Paragraph(_x(text).upper(), st["heading"])
    rule = HRFlowable(
        width="100%",
        thickness=0.5,
        color=COLOR_BORDER,
        spaceBefore=0,
        spaceAfter=SP_HEADING_AFTER,
        lineCap="round",
    )
    return KeepTogether([para, rule])


def bullet_para(text, st):
    """Return a bullet paragraph with hanging indent."""
    return Paragraph(f"\u2022\u2002{_x(text)}", st["bullet"])


# ---------------------------------------------------------------------------
# Section renderers — each returns a list of Flowables
# ---------------------------------------------------------------------------

def render_header(header, st):
    items = [Paragraph(_x(header["name"]), st["name"])]
    if header.get("contact_line"):
        items.append(Paragraph(_x(header["contact_line"]), st["contact"]))
    if header.get("languages"):
        items.append(Paragraph(_x(header["languages"]), st["languages"]))
    return items


def render_summary(section, st, bold_font):
    return [
        section_heading(section["heading"], st),
        Paragraph(_x(section["body"]), st["summary"]),
    ]


def render_skills_list(section, st, bold_font):
    text = ", ".join(section.get("items", []))
    return [
        section_heading(section["heading"], st),
        Paragraph(_x(text), st["tech"]),
    ]


def render_technical_skills(section, st, bold_font):
    items = [section_heading(section["heading"], st)]
    for cat in section.get("categories", []):
        markup = f'<font name="{bold_font}">{_x(cat["label"])}:</font> {_x(cat["value"])}'
        items.append(Paragraph(markup, st["tech"]))
    return items


def render_experience(section, st, bold_font):
    items = [section_heading(section["heading"], st)]
    for role in section.get("roles", []):
        title = Paragraph(_x(role["title"]), st["job_title"])
        company = Paragraph(_x(role["company_line"]), st["company"])
        items.append(KeepTogether([title, company]))
        for b in role.get("bullets", []):
            items.append(bullet_para(b, st))
    return items


def render_education(section, st, bold_font):
    items = [section_heading(section["heading"], st)]
    for entry in section.get("entries", []):
        group = [
            Paragraph(_x(entry["title"]), st["edu_title"]),
            Paragraph(_x(entry.get("subtitle", "")), st["edu_sub"]),
        ]
        if entry.get("detail"):
            group.append(Paragraph(_x(entry["detail"]), st["edu_detail"]))
        items.append(KeepTogether(group))
    return items


def render_certifications(section, st, bold_font):
    items = [section_heading(section["heading"], st)]
    for item in section.get("items", []):
        name = _x(item["name"])
        detail = _x(item.get("detail", ""))
        markup = f'<font name="{bold_font}">{name}</font>{detail}'
        items.append(Paragraph(markup, st["cert"]))
    return items


def render_bullets_section(section, st, bold_font):
    items = [section_heading(section["heading"], st)]
    for b in section.get("bullets", []):
        items.append(bullet_para(b, st))
    return items


SECTION_RENDERERS = {
    "summary":          render_summary,
    "skills_list":      render_skills_list,
    "technical_skills": render_technical_skills,
    "experience":       render_experience,
    "education":        render_education,
    "certifications":   render_certifications,
    "awards":           render_certifications,
    "bullets_section":  render_bullets_section,
}


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_pdf(cv_data, output_path):
    """Generate a PDF file from structured CV data."""
    font, bold_font = register_fonts()
    st = build_styles(font, bold_font)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
    )

    story = render_header(cv_data["header"], st)
    for sec in cv_data.get("sections", []):
        renderer = SECTION_RENDERERS.get(sec.get("type"))
        if renderer:
            story.extend(renderer(sec, st, bold_font))
        else:
            print(f"Warning: Unknown section type '{sec.get('type')}', skipping.",
                  file=sys.stderr)

    doc.build(story)
    print(f"PDF generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate PDF resume from JSON")
    parser.add_argument("input", help="Path to CV data JSON file")
    parser.add_argument("--output", "-o", default="resume_output.pdf",
                        help="Output PDF filename (default: resume_output.pdf)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        cv_data = json.load(f)

    generate_pdf(cv_data, Path(args.output))


if __name__ == "__main__":
    main()
