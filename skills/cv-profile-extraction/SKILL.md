---
name: cv-profile-extraction
description: "Extract and structure professional profile data from a LinkedIn PDF export, an uploaded CV/resume file (PDF/DOCX), a LinkedIn URL, or pasted profile text. Use when: gathering candidate information, parsing LinkedIn profiles, extracting resume data, normalizing career history."
argument-hint: "Attach your LinkedIn PDF export or CV file, or provide a LinkedIn URL or pasted text"
---

# Profile Extraction

## Purpose
Extract all professional profile data from any source the user provides and normalize it into a consistent structured format for downstream CV generation.

## Accepted Inputs
1. **LinkedIn PDF export** — Download your LinkedIn profile as a PDF (Profile → More → Save to PDF) and attach it
2. **CV or resume file** — An existing CV or resume as a PDF or DOCX file attached by the user
3. **LinkedIn URL** — Fetch and parse the full public profile (available on platforms with web access)
4. **Pasted text** — Raw text copied from LinkedIn or another source

If no input is provided, ask the user which source they prefer.

## Procedure

### Step 1: Detect Input Type and Acquire Raw Data

First, identify which input type was provided:

- **LinkedIn PDF**: A PDF whose content contains LinkedIn's standard section headers ("Experience", "Education", "Skills", "Languages", "Certifications") and typically opens with the person's name and a professional headline.
- **CV/Resume file**: A PDF or DOCX following a CV/resume structure — may have custom section names, more detailed bullet points, and is unlikely to contain LinkedIn-style formatting.
- **LinkedIn URL**: A URL starting with `linkedin.com/in/`
- **Pasted text**: Raw text provided inline by the user

Then acquire the raw data:
- **LinkedIn PDF / CV file**: Read the file contents.
- **LinkedIn URL**: Fetch the page content using web tools. If the page is blocked or returns incomplete data, ask the user to attach a LinkedIn PDF export instead.
- **Pasted text**: Use it directly.

### Step 1b: LinkedIn PDF — Parsing Notes

LinkedIn-generated PDFs follow a consistent structure. Map sections as follows:

| LinkedIn PDF section | Profile schema field |
|---|---|
| Name and headline (top of PDF) | `name`; note the headline as context but do not copy it verbatim into the CV |
| Contact Info block | `location`, `email`, `linkedin_url` — email is often absent |
| About | Use as raw input when writing the Professional Summary |
| Experience | `professional_experience` — each entry: company, title, date range, location, bullet points |
| Education | `education` |
| Licenses & Certifications | `certifications` |
| Skills | `skills.technical` and `skills.domain` |
| Languages | `languages` |
| Honors & Awards | `awards` |
| Projects | Include under `additional` |
| Recommendations | Ignore — do not include in the CV |

**Known limitations of LinkedIn PDFs:**
- Email address is rarely exported — must ask the user
- GitHub, portfolio, or personal website URLs are not included unless the user manually added them to their LinkedIn contact section
- Role bullet points may lack quantified metrics (numbers, percentages, scale indicators)
- Date precision is sometimes month-only or year-only for older entries

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

Review the extracted data and flag issues. Tailor the flags based on the detected input type:

#### All input types
- Roles with **missing dates** (no start/end)
- Roles with **vague descriptions** (no concrete achievements or technologies)
- **Employment gaps** longer than 6 months
- Sections that are **entirely missing** (e.g., no education, no skills listed)

#### LinkedIn PDF inputs (additional flags)
- **Email address missing** — LinkedIn PDFs rarely export the email address
- **No GitHub or portfolio URL**
- **Role bullets lack metrics** — no numbers, percentages, team/user scale, or measurable impact

#### CV/Resume file inputs (additional flags)
- **Most recent role ends more than 12 months ago** — the CV may be outdated; the user may have a more recent role to add
- **LinkedIn URL not present**

### Step 3b: Generate Missing Info Questions

Based on the flags above, generate a focused set of questions to fill the gaps. Group by topic and keep them specific — reference exact roles, companies, and dates from the extracted data. Aim for 3–8 questions total.

**For all inputs — always ask (achievement mining):**
People frequently have impactful work they don’t think of as CV-worthy. Ask 2–3 of these regardless of input type to surface it:
- "What’s an accomplishment you’re proud of that might not be obvious from your CV or LinkedIn — something a colleague or manager praised, or where you saw a real difference?"
- "What do colleagues or your manager most often come to you for? What are you the go-to person for?"
- "Is there a project, initiative, or change you drove that had a clear before/after — even if you don’t have hard numbers for it?"

**For LinkedIn PDF inputs — always ask:**
- What is your email address?
- Do you have a GitHub profile, portfolio site, or other relevant URL to include?
- For each role that has no quantified achievements: "In your role as [title] at [company], can you share specific numbers or outcomes — e.g. team size, users served, cost savings, or performance improvements?"

**For LinkedIn PDF inputs — ask if flagged:**
- For year-only or imprecise dates on recent roles: "Can you confirm the start and end month for your role at [company]?"

**For CV/Resume file inputs — ask if flagged:**
- If most recent role ends >12 months ago: "Is your CV fully up to date? Have you started a new role or taken on any significant project since [last role end date]?"
- If LinkedIn URL is missing: "Do you have a LinkedIn profile URL you'd like to include?"

**For all inputs — ask if flagged:**
- For employment gaps >6 months: "I noticed a gap between [end date] and [start date] — is there anything from that period you'd like to include, such as freelance work, study, a personal project, or caregiving?"

> **Note:** Present the Missing Info Questions to the user and wait for their answers before returning the final structured profile. Once answered, merge the provided information into the structured data.

### Step 4: Output
Return the structured data in a clear, organized format using the categories above. Include a **"Data Quality Notes"** section at the end listing any gaps or ambiguities found.

> **Note:** Data Quality Notes are internal working notes used only by the tailoring step to ask better clarifying questions. They never appear in the final CV.

## Constraints
- Do NOT invent, embellish, or assume information not present in the source.
- Do NOT discard information — include everything, even if it seems minor.
- If something is ambiguous, include it with a note rather than omitting it.
- Preserve original date formats where possible (normalize to "Mon YYYY" if feasible).
