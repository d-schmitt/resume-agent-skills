# CV Structure Reference

This document defines the exact section structure, formatting conventions, and content patterns used when generating CV content.

## Section Structure

### 1. Header
```
[Full Name]
[City, Country]  ·  [email]  ·  [linkedin.com/in/handle]  ·  [github.com/handle]
[Languages: e.g., German (native)  ·  English (full professional proficiency)]
```

### 2. Professional Summary
- 3–4 lines of continuous prose (not bullets)
- Opens with: role identity + years of experience + core domain
- Highlights 2–3 top achievements with metrics
- Ends with: what you bring to this specific role/company
- Use justified alignment

### 3. Key Skills
A compact list of business and domain skills aligned to the job description.
Use a single paragraph or comma-separated list. Keep to 2–3 lines.

### 4. Technical Skills
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

### 5. Professional Experience
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

### 6. Education
For each entry:
```
[Degree and Field]
[Institution]  |  [Date Range]
[Optional: thesis topic, notable achievements]
```

### 7. Publications & Open Source (Optional)
Bulleted list. Include only if the profile contains patents, academic publications, or notable open-source contributions.

```
• [Project/Patent/Paper title] — [brief context and impact]
```


### 8. Certifications
One line per certification:
```
[Certification Name] — [Issuing Organization] ([Date])
```
- Certification name in **bold**, rest in normal weight

### 9. Awards (Optional)
Same format as certifications:
```
[Award Name] — [Context/description] ([Year])
```

### 10. Community & Speaking (Optional)
Bulleted list. Only include if there is evidence in the profile.

## Content Guidelines

### Bullet Point Patterns
Strong action verbs to use:
- Leadership: Led, Directed, Spearheaded, Championed, Founded, Orchestrated
- Technical: Built, Designed, Engineered, Implemented, Developed, Architected
- Impact: Delivered, Achieved, Reduced, Increased, Accelerated, Improved
- Innovation: Pioneered, Initiated, Introduced, Established, Launched

### Metrics
Always prefer quantified impact:
- Team/user counts: "adopted by 3 product teams", "mentored 4 engineers"
- Time savings: "reducing deployment time from 45 minutes to 8 minutes"
- Scale: "processing 500K+ daily events", "12 services migrated"
- Business impact: "cutting infrastructure costs by 25%", "reducing mean time to recovery by 40%"

### ATS Optimization
- Mirror exact phrasing from the job description where truthful
- Include both acronyms and full forms: "CI/CD (Continuous Integration/Continuous Deployment)"
- Place the most important keywords in the Professional Summary and first bullets of each role
- Avoid images, tables, headers/footers, or text boxes — use plain text with clear section headings

### Length Target
- **1 page**: Early career (0–5 years), 2–3 roles
- **2 pages**: Mid-senior career (5+ years), 3+ roles
- Never exceed 2 pages
