---
name: profile-extraction
description: "Extract and structure professional profile data from LinkedIn URLs, pasted profile text, or uploaded resume files (PDF/DOCX). Use when: gathering candidate information, parsing LinkedIn profiles, extracting resume data, normalizing career history."
argument-hint: "Provide a LinkedIn URL, paste your profile text, or attach a resume file"
---

# Profile Extraction

## Purpose
Extract all professional profile data from any source the user provides and normalize it into a consistent structured format for downstream CV generation.

## Accepted Inputs
1. **LinkedIn URL** — Fetch and parse the full public profile
2. **Pasted text** — Raw text copied from LinkedIn or another source
3. **Resume file** — PDF or DOCX file attached by the user

If no input is provided, ask the user which source they prefer.

## Procedure

### Step 1: Acquire Raw Data
- If given a **URL**: fetch the page content using web tools. If the page is blocked or incomplete, ask the user to paste the text instead.
- If given **pasted text**: use it directly.
- If given a **file**: read the file contents.

### Step 2: Extract Structured Data
Parse the raw data into these categories:

#### Personal Information
- Full name
- Location (city, country)
- Email (if visible)
- LinkedIn URL
- GitHub / portfolio URL (if present)
- Languages spoken (with proficiency level)

#### Professional Experience (for each role)
- Job title
- Company name
- Location
- Start date – End date (or "Present")
- Bullet points: responsibilities, achievements, technologies used

#### Education (for each entry)
- Degree and field of study
- Institution name
- Date range
- Thesis topic (if mentioned)
- Notable achievements (honors, rankings)

#### Certifications
- Certification name
- Issuing organization
- Date obtained

#### Skills
- Technical skills (languages, tools, platforms)
- Domain/business skills
- Methodologies

#### Additional
- Patents and publications
- Awards
- Community activities, speaking engagements, volunteering
- Open-source contributions

### Step 3: Flag Gaps
Review the extracted data and flag:
- Roles with **missing dates** (no start/end)
- Roles with **vague descriptions** (no concrete achievements or technologies)
- **Employment gaps** longer than 6 months
- Sections that are **entirely missing** (e.g., no education, no skills listed)

### Step 4: Output
Return the structured data in a clear, organized format using the categories above. Include a **"Data Quality Notes"** section at the end listing any gaps or ambiguities found.

## Constraints
- Do NOT invent, embellish, or assume information not present in the source.
- Do NOT discard information — include everything, even if it seems minor.
- If something is ambiguous, include it with a note rather than omitting it.
- Preserve original date formats where possible (normalize to "Mon YYYY" if feasible).
