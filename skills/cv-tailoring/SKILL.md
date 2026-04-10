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

### Step 2: Clarifying Questions
For each **weak/missing** or **partial match** area that is rated **Critical** or **Important** in the job analysis, generate 3–7 targeted questions.

Questions must be **specific**, not generic. Good examples:
- "In your Kubernetes migration, how many services did you move and what was the impact on uptime or latency?"
- "When you built the observability platform, which teams adopted it and how did you measure the reduction in incident response time?"
- "Did the CI/CD pipeline improvements affect deployment frequency or rollback rates beyond the build-time savings?"

Bad examples (too vague):
- "Can you tell me more about your projects?"
- "What metrics do you have?"

**STOP here and present the questions to the user. Wait for their answers before proceeding.**

### Step 3: Write CV Content
After receiving user answers, write the complete CV in markdown using the structure defined in [cv-structure.md](./references/cv-structure.md).

#### Section Order
1. Header (name, location, contact, links)
2. Professional Summary (3–4 lines)
3. Key Skills (business + technical, aligned to job)
4. Technical Skills (categorized)
5. Professional Experience (reverse-chronological)
6. Education
7. Open Source Contributions, Patents & Publications (if evidence exists)
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
- Do NOT invent metrics or achievements
- 3–7 bullets per role, ordered by relevance to the target job
- Most relevant responsibilities first within each role

#### Content Selection Strategy
- **Emphasize** experiences that match Critical and Important job requirements
- **Condense** experiences unrelated to the target role (fewer bullets, less detail)
- **Reframe** partial matches using job description language where truthful
- **Omit** only if a section would be empty or the content is truly irrelevant
- Use **ATS keywords** from the job analysis naturally in bullets and skills sections

### Step 4: Profile Advice
After the CV content, generate a **"Strengthening Advice"** section with 5–7 bullets:
- Additional metrics the user could add
- Projects worth highlighting more prominently
- Skills to surface more clearly
- Certifications that would strengthen the application
- Gaps that could be addressed in a cover letter

### Step 5: Output
Return:
1. The complete CV content in markdown (ready for the `cv-export` skill)
2. The Strengthening Advice section

## Constraints
- Stay **fully truthful** — rephrase and reorganize, but never fabricate
- Do NOT add roles, companies, or achievements not in the profile or user answers
- Do NOT skip the clarifying questions step — always pause for user input
- Target **1–2 pages** of content (guide: ~600–1000 words for the full CV body)
- Use English throughout
