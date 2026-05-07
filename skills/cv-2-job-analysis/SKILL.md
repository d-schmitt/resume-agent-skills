---
name: cv-2-job-analysis
description: "Analyze job descriptions to extract requirements, qualifications, keywords, and themes. Use when: parsing job postings, identifying ATS keywords, understanding role requirements, prioritizing job qualifications."
argument-hint: "Provide a job description URL or paste the job description text"
---

# Job Analysis

## Purpose
Analyze a job description to extract structured requirements, identify ATS-relevant keywords, and prioritize qualifications for CV tailoring.

## Accepted Inputs
1. **Job description URL** — Fetch and parse the job posting page
2. **Pasted text** — Raw job description text

If no input is provided, ask the user for the job description.

## Procedure

### Step 1: Acquire Job Description
- If given a **URL**: fetch the page content using web tools. If the page is blocked, ask the user to paste the text.
- If given **pasted text**: use it directly.

### Step 2: Extract Role Metadata
- Job title
- Company name
- Location (on-site / hybrid / remote)
- Seniority level (entry / mid / senior / lead / principal)
- Department or team (if mentioned)
- Employment type (full-time, part-time, contract)
- **Language of the job description** (e.g., English, German, French) — detect from the posting text

### Step 3: Extract Requirements
Categorize every requirement into one of these groups:

#### Key Responsibilities
List the main duties and responsibilities described in the role. For each, note:
- The core activity
- Domain or context (e.g., "cloud infrastructure", "customer-facing")
- Scale indicators (team size, budget, user count)

#### Required Qualifications (Must-Have)
Skills and qualifications explicitly marked as required. For each:
- Skill or qualification name
- Years of experience if specified
- Context (e.g., "Python for data pipelines" vs. just "Python")

#### Preferred Qualifications (Nice-to-Have)
Skills marked as "preferred", "bonus", "nice to have", or "a plus". Same format as above.

#### ATS Keywords
Extract all technical terms, tools, methodologies, certifications, and domain-specific phrases that an ATS system would likely scan for. Include:
- Exact phrases from the posting (preserve original wording)
- Acronyms and their expansions
- Tool/platform names with version numbers if mentioned

### Step 4: Identify Themes
Identify 3–5 overarching themes the role emphasizes. Examples:
- "Cross-functional leadership"
- "Data-driven decision making"
- "Cloud-native architecture"
- "Developer experience and tooling"
- "Stakeholder communication"

### Step 5: Priority Rating
Rate each extracted requirement:
- **Critical** — Explicitly required, mentioned multiple times, or in the job title
- **Important** — Listed in requirements, mentioned once
- **Nice-to-have** — Listed as preferred or bonus

### Step 6: Output
Return the structured analysis using the categories above. Include the **detected language** of the job description prominently in the metadata block — this is used by the orchestrator to determine whether to prompt for CV output language. End with a **"Tailoring Recommendations"** section: 3–5 bullet points advising which aspects of a candidate's profile should be emphasized most.

## Constraints
- Do NOT add requirements that are not in the job description.
- Do NOT interpret vague language as specific requirements (e.g., "team player" stays as-is, don't expand it into specific skills).
- Preserve the original language of the job posting when extracting keywords.
- If the job description is very short or vague, note this as a limitation.
