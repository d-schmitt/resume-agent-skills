---
name: cv-export
description: "Export CV content to professionally formatted DOCX and PDF files. Use when: generating resume documents, creating DOCX from CV content, converting resume to PDF, formatting CV for download."
argument-hint: "Provide the CV content in markdown format"
---

# CV Export

## Purpose
Convert CV content (markdown) into professionally formatted DOCX and PDF files matching a clean, ATS-friendly, single-column layout.

## Required Input
- **CV content in markdown** — output from the `cv-tailoring` skill
- **Output filename** (optional, defaults to `resume_output`)

## Procedure

### Step 1: Prepare CV Data
Parse the markdown CV content into a structured JSON format that the export script expects. The JSON structure must follow this schema:

```json
{
  "header": {
    "name": "Full Name",
    "contact_line": "City, Country  ·  email@example.com  ·  linkedin.com/in/handle",
    "languages": "German (native)  ·  English (full professional proficiency)"
  },
  "sections": [
    {
      "type": "summary",
      "heading": "PROFESSIONAL SUMMARY",
      "body": "Summary text as a single paragraph..."
    },
    {
      "type": "skills_list",
      "heading": "KEY SKILLS",
      "items": ["Skill 1", "Skill 2", "Skill 3"]
    },
    {
      "type": "technical_skills",
      "heading": "TECHNICAL SKILLS",
      "categories": [
        {"label": "Platforms & Tools", "value": "GitHub, Azure DevOps, Docker"},
        {"label": "Languages", "value": "Python, SQL, YAML"}
      ]
    },
    {
      "type": "experience",
      "heading": "PROFESSIONAL EXPERIENCE",
      "roles": [
        {
          "title": "Job Title",
          "company_line": "Company  |  Location  |  Date Range",
          "bullets": ["Bullet point 1", "Bullet point 2"]
        }
      ]
    },
    {
      "type": "education",
      "heading": "EDUCATION",
      "entries": [
        {
          "title": "Degree and Field",
          "subtitle": "Institution  |  Date Range",
          "detail": "Optional: thesis, achievements"
        }
      ]
    },
    {
      "type": "certifications",
      "heading": "CERTIFICATIONS",
      "items": [
        {"name": "Cert Name", "detail": " — Issuing Org (Date)"}
      ]
    },
    {
      "type": "awards",
      "heading": "AWARDS",
      "items": [
        {"name": "Award Name", "detail": " — Description (Year)"}
      ]
    },
    {
      "type": "bullets_section",
      "heading": "COMMUNITY & SPEAKING",
      "bullets": ["Bullet 1", "Bullet 2"]
    },
    {
      "type": "bullets_section",
      "heading": "PUBLICATIONS & OPEN SOURCE",
      "bullets": ["Bullet 1", "Bullet 2"]
    }
  ]
}
```

### Step 2: Save JSON
Write the structured JSON to a temporary file (e.g., `cv_data.json`) in the current working directory.

### Step 3: Content Integrity Check
Before generating files, check the JSON for content-level issues that the export scripts cannot correct. What can go wrong in the content fields:

- [ ] No HTML tags in any text field (e.g., `<b>`, `<br>`, `&amp;`)
- [ ] No emoji or decorative characters in section headings
- [ ] All `bullets` arrays contain plain strings — no nested arrays or objects
- [ ] Contact information is in `header.contact_line`, not embedded in a section `body` or bullet
- [ ] No single bullet is a multi-sentence paragraph that should be split into separate bullets

If any check fails, correct the JSON before proceeding.

### Step 4: Generate DOCX
Run the export script:
```bash
python skills/cv-export/scripts/export_docx.py cv_data.json --output resume_output.docx
```

### Step 5: Generate PDF
Run the PDF export script directly from the same JSON:
```bash
python skills/cv-export/scripts/export_pdf.py cv_data.json --output resume_output.pdf
```

### Step 6: Deliver
Present both files to the user for download.

## Dependencies
Install before first use:
```bash
pip install -r requirements.txt
```

Requires `python-docx` (DOCX generation) and `reportlab` (PDF generation). No external tools such as Microsoft Word or LibreOffice are needed.

## Constraints
- Output must be **single-column**, ATS-friendly layout
- Do NOT use tables, text boxes, images, or headers/footers in the DOCX
- Font: Calibri throughout
- Page size: A4 with narrow margins
- The formatting must match the reference document's visual style
