---
name: cv-tailoring
description: "Tailor CV content to a specific job by performing gap analysis, asking clarifying questions, and writing all CV sections. Use when: writing a resume, tailoring CV to job description, gap analysis between profile and job requirements, generating CV bullet points."
argument-hint: "Provide the extracted profile data and job analysis"
---

# CV Tailoring

## Purpose
Compare a candidate's profile against job requirements, identify gaps, gather missing information through targeted questions, and produce complete, tailored CV content in markdown.

## Required Inputs
1. **Structured profile data** — output from the `profile-extraction` skill
2. **Structured job analysis** — output from the `job-analysis` skill

If either input is missing, ask the user to run the corresponding skill first.

## Procedure

### Step 1: Gap Analysis
Compare the profile data against the job analysis. For each job requirement, assess:

| Rating | Meaning |
|--------|---------|
| **Strong match** | Profile clearly demonstrates this skill/experience with evidence |
| **Partial match** | Related experience exists but needs reframing or more detail |
| **Weak/missing** | No clear evidence in the profile |

Produce a summary table of matches.

#### Keyword Coverage
Count how many of the ATS keywords (from the job analysis) appear anywhere in the candidate's profile:

| Coverage | Tailoring level | Effort |
|---|---|---|
| ≥80% | Light — reorder and surface existing content | ~15 min |
| 60–79% | Medium — rewrite summary, expand matching bullets | ~30 min |
| 50–65% | Aggressive — complete summary rewrite, restructure skills | ~60 min |
| <50% | Significant gap — flag clearly; discuss with user before proceeding | — |

Include the coverage percentage and tailoring level in the gap analysis output.

### Step 2: Clarifying Questions
For each **weak/missing** or **partial match** area that is rated **Critical** or **Important** in the job analysis, generate 3–7 targeted questions.

Questions must be **specific**, not generic. Good examples:
- "In your Kubernetes migration, how many services did you move and what was the impact on uptime or latency?"
- "When you built the observability platform, which teams adopted it and how did you measure the reduction in incident response time?"
- "Did the CI/CD pipeline improvements affect deployment frequency or rollback rates beyond the build-time savings?"

Bad examples (too vague):
- "Can you tell me more about your projects?"
- "What metrics do you have?"

When a user says they don't have specific numbers, don't accept the vague answer. Use qualitative proxy probes to surface impact:
- "What did your manager or team say about the outcome? Any specific feedback you remember?"
- "How did things change for the people you worked with after you delivered this?"
- "What would have happened if this work hadn't been done, or had taken twice as long?"
- "How many people or teams were affected by it — even a rough order of magnitude helps."

These answers can be shaped into impact statements without fabricating numbers.

Additional question rules:
- If the profile flags an **employment gap** >6 months, ask how the candidate spent that time (upskilling, freelancing, sabbatical, personal reasons). Incorporate their answer naturally into the CV — e.g., as a brief note under the relevant date range or as context in the summary — rather than leaving the gap unexplained.
- For **patents**, ask whether the patent was filed or granted, and whether it was commercialized or adopted. Filed-only patents are weaker evidence; include them only when relevant to the target role.
- For **open-source contributions**, ask for specific PRs, issues, or maintainer roles to ensure claims are verifiable.

**STOP here and present the questions to the user. Wait for their answers before proceeding.**

### Step 3: Write CV Content
After receiving user answers, write the complete CV in markdown using the CV structure defined in the **CV Structure Reference** section of this file.

**Output language:** Write all CV content — bullets, summary, skills, section headings — in the output language confirmed in Step 3b of the orchestrator (default: English). If English, proceed as normal. If another language:
- Translate all written content into that language
- Use the translated section headings from the language table in the **CV Structure Reference** section of this file
- ATS keywords must be used in their original form as they appear in the (non-English) job description — do not translate them back to English
- If the job description language and the CV output language differ (e.g., English JD requested in German CV), flag this to the user: ATS keyword matching will be unreliable across languages

#### Section Order
1. Header (name, location, contact, links)
2. Professional Summary (3–4 lines)
3. Key Skills (business + technical, aligned to job)
4. Technical Skills (categorized)
5. Professional Experience (reverse-chronological)
6. Education
7. Publications & Open Source (if evidence exists)
8. Certifications
9. Awards (if present)
10. Community & Speaking (if evidence exists)

#### Bullet Writing Rules
Every experience bullet must follow this pattern:
> **Action verb** + what you did + how you did it + business/technical impact (with metrics when available)

Examples:
- "Architected an observability platform using Prometheus and Grafana, adopted by 3 product teams and reducing mean time to recovery by 40%."
- "Led migration of 12 services from EC2 to Kubernetes (EKS), achieving 99.95% uptime and cutting infrastructure costs by 25%."

Rules:
- Start every bullet with a **strong action verb** (Led, Built, Designed, Pioneered, Championed, Delivered, etc.)
- Include **metrics** where the profile or user answers provide them
- When stating a technical improvement, also state the **downstream business effect** if known (e.g., "reducing response time by 85%, which improved checkout conversion by 12%" rather than just "reducing response time by 85%")
- If the user **cannot provide metrics**, use scope indicators instead: team size, user/customer count, number of services/systems, project duration, or budget range
- Expand **acronyms on first mention** in the Professional Summary (e.g., "Kubernetes (K8s)", "CI/CD (Continuous Integration/Continuous Deployment)"); use the short form in bullets thereafter
- Do NOT invent metrics or achievements
- **Anti-pattern — Responsibilities Without Outcomes**: Listing duties instead of impact is the most common CV weakness. If a bullet only describes what the person was responsible for, rewrite it to show what changed as a result.

  | ✗ Duty-only | ✓ With outcome |
  |---|---|
  | "Managed a team of engineers" | "Led a team of 5 engineers to deliver a payment integration on time, reducing checkout abandonment by 12%" |
  | "Responsible for onboarding new hires" | "Designed onboarding programme for 8 new joiners, cutting time-to-productivity from 6 weeks to 3" |
  | "Worked on data pipeline reliability" | "Refactored ETL pipeline, reducing failure rate from 15% to <1% and eliminating weekly manual intervention" |

- 3–7 bullets per role, ordered by relevance to the target job
- Most relevant responsibilities first within each role

#### Content Selection Strategy
- **Emphasize** experiences that match Critical and Important job requirements
- **Condense** experiences unrelated to the target role (fewer bullets, less detail)
- **Reframe** partial matches using job description language where truthful
- **Omit** only if a section would be empty or the content is truly irrelevant
- Use **ATS keywords** from the job analysis naturally in bullets and skills sections

### Step 4: ATS Score
After writing the CV, calculate a content-based ATS score (0–100). **Parseability** (layout, fonts, no images) is a binary gate handled by the cv-export skill and guaranteed by its fixed output format — it is not scored here. This score measures only what can be evaluated from the CV text.

| Category | Points | What it measures |
|---|---|---|
| Keyword coverage | 40 | How many Critical + Important job analysis keywords appear in the CV, and where |
| Role & level fit | 25 | How well the candidate's seniority, domain, and experience years match the target role |
| Content quality | 35 | Outcomes vs. duties, metrics or scope indicators, action verbs, no generic filler |

**Target: 80+ / 100**

#### Scoring Checklist

**Keyword Coverage (40 pts):**
Count how many of the Critical + Important keywords from the job analysis appear in the CV (Professional Summary, Skills sections, or bullet points). Calculate the coverage percentage:
- 80%+ present AND at least half in Summary or Skills = 40 pts
- 80%+ present but mostly buried in older roles = 32 pts
- 60–79% present = 24 pts
- 40–59% present = 16 pts
- <40% present = 8 pts

**Role & Level Fit (25 pts):**
- [ ] Job title or a closely matching equivalent appears in at least one recent role
- [ ] Candidate's years of experience meets, or is within 2 years of, the stated requirement
- [ ] Industry or domain matches, or a transferable domain is explicitly reframed for the target role
- [ ] Seniority of responsibilities matches the target level (not applying for senior roles with only junior-level bullets)
- ✓ All 4 checks = 25 pts | 1 fails = 18 pts | 2 fail = 12 pts | 3+ fail = 5 pts

**Content Quality (35 pts):**
- [ ] At least 5 bullets have quantifiable metrics (numbers, %, time saved) OR clear scope indicators (team size, user count, systems affected, budget)
- [ ] Every bullet starts with a strong action verb (Led, Built, Delivered, Designed, etc.)
- [ ] No generic filler language ("team player", "passionate about", "hardworking" without evidence)
- [ ] Professional Summary opens with role identity + years of experience + a specific achievement or metric
- [ ] Bullets for the 2 most recent roles emphasize outcomes, not just responsibilities
- ✓ All 5 checks = 35 pts | 1 fails = 28 pts | 2 fail = 21 pts | 3+ fail = 12 pts

Present the score in this format:
```
ATS Score: [X]/100
• Keyword coverage:  [n]/40
• Role & level fit:  [n]/25
• Content quality:   [n]/35
```
For any category scoring below 70% of its maximum, give one specific actionable fix.

### Step 5: Profile Advice
After the CV content, generate a **"Strengthening Advice"** section with 5–7 bullets:
- Additional metrics the user could add
- Projects worth highlighting more prominently
- Skills to surface more clearly
- Certifications that would strengthen the application
- Gaps that could be addressed in a cover letter

### Step 6: Output
Return:
1. The complete CV content in markdown (ready for the `cv-export` skill)
2. The ATS Score with per-category breakdown and any specific fixes
3. The Strengthening Advice section

## Constraints
- Stay **fully truthful** — rephrase and reorganize, but never fabricate
- Do NOT add roles, companies, or achievements not in the profile or user answers
- Do NOT skip the clarifying questions step — always pause for user input
- Target **1–2 pages** of content (guide: ~600–1000 words for the full CV body)
- Write the CV in **English by default** unless a different output language was confirmed in Step 3b of the orchestrator

## CV Structure Reference

This section defines the exact section structure, formatting conventions, and content patterns used when generating CV content.

### Section Structure

#### 1. Header
```
[Full Name]
[City, Country]  ·  [email]  ·  [linkedin.com/in/handle]  ·  [github.com/handle]
[Languages: e.g., German (native)  ·  English (full professional proficiency)]
```

#### 2. Professional Summary
- 3–4 lines of continuous prose (not bullets)
- Opens with: role identity + years of experience + core domain
- Highlights 2–3 top achievements with metrics
- Ends with: what you bring to this specific role/company
- Use justified alignment

#### 3. Key Skills
A compact list of business and domain skills aligned to the job description.
Use a single paragraph or comma-separated list. Keep to 2–3 lines.

#### 4. Technical Skills
Categorized as label–value pairs, one line per category:
```
Platforms & Tools: GitHub, AWS, Docker, Kubernetes
Languages: Python, TypeScript, Go, SQL
Cloud & DevOps: Terraform, GitHub Actions, EKS, Lambda
Frameworks: FastAPI, React, Next.js, Celery
Methodologies: Scrum, Kanban, TDD, SRE  ← include only if JD mentions methodology requirements
```
- Category name in **bold**, followed by the list
- Order categories by relevance to the target job
- **Methodologies** category is optional — include only when the job description explicitly lists methodology requirements (e.g., "Scrum experience required"). For most engineering roles, methodologies are assumed and add no signal.

#### 5. Professional Experience
For each role (reverse-chronological):

```
[Job Title]
[Company]  |  [Location]  |  [Start Date] – [End Date or Present]
• Bullet point 1
• Bullet point 2
• ...
```

- **Job title**: bold, slightly larger than body text
- **Company line**: smaller, muted color, separated by pipes
- **Bullets**: 3–7 per role, ordered by relevance to target job
- Each bullet follows the pattern: action verb + what + how + impact

#### 6. Education
For each entry:
```
[Degree and Field]
[Institution]  |  [Date Range]
[Optional: thesis topic, notable achievements]
```

#### 7. Publications & Open Source (Optional)
Bulleted list. Include only if the profile contains patents, academic publications, or notable open-source contributions.

```
• [Project/Patent/Paper title] — [brief context and impact]
```


#### 8. Certifications
One line per certification:
```
[Certification Name] — [Issuing Organization] ([Date])
```
- Certification name in **bold**, rest in normal weight

#### 9. Awards (Optional)
Same format as certifications:
```
[Award Name] — [Context/description] ([Year])
```

#### 10. Community & Speaking (Optional)
Bulleted list. Only include if there is evidence in the profile.

### Content Guidelines

#### Bullet Point Patterns
Strong action verbs to use:
- Leadership: Led, Directed, Spearheaded, Championed, Founded, Orchestrated
- Technical: Built, Designed, Engineered, Implemented, Developed, Architected
- Impact: Delivered, Achieved, Reduced, Increased, Accelerated, Improved
- Innovation: Pioneered, Initiated, Introduced, Established, Launched

#### Metrics
Always prefer quantified impact:
- Team/user counts: "adopted by 3 product teams", "mentored 4 engineers"
- Time savings: "reducing deployment time from 45 minutes to 8 minutes"
- Scale: "processing 500K+ daily events", "12 services migrated"
- Business impact: "cutting infrastructure costs by 25%", "reducing mean time to recovery by 40%"

#### ATS Optimization
- Mirror exact phrasing from the job description where truthful
- Include both acronyms and full forms: "CI/CD (Continuous Integration/Continuous Deployment)"
- Place the most important keywords in the Professional Summary and first bullets of each role
- Avoid images, tables, headers/footers, or text boxes — use plain text with clear section headings

#### Length Target
- **1 page**: Early career (0–5 years), 2–3 roles
- **2 pages**: Mid-senior career (5+ years), 3+ roles
- Never exceed 2 pages

### Section Headings by Language
Use these translated headings when the CV output language is not English. All other layout and structure rules remain the same.

| Section | English | German |
|---|---|---|
| Professional Summary | PROFESSIONAL SUMMARY | BERUFLICHES PROFIL |
| Key Skills | KEY SKILLS | KERNKOMPETENZEN |
| Technical Skills | TECHNICAL SKILLS | TECHNISCHE KENNTNISSE |
| Professional Experience | PROFESSIONAL EXPERIENCE | BERUFSERFAHRUNG |
| Education | EDUCATION | AUSBILDUNG |
| Certifications | CERTIFICATIONS | WEITERBILDUNG |
| Awards | AWARDS | AUSZEICHNUNGEN |
| Publications & Open Source | PUBLICATIONS & OPEN SOURCE | PUBLIKATIONEN & OPEN SOURCE |
| Community & Speaking | COMMUNITY & SPEAKING | EHRENAMT & VORTRÄGE |

To add another language, extend this table.
