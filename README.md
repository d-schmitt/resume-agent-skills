# Resume Builder — AI Agent + Skills Package

An AI agent that turns your LinkedIn profile or CV and a job description into a tailored, ATS-optimized CV — with keyword scoring, gap analysis, and targeted clarifying questions at every step. Exports to DOCX and PDF. Use in Langdock, Perplexity, GitHub Copilot, Claude Code, or any AI tool that supports custom instructions.

**What it does** — four skills, usable together or independently:
1. **[cv-1-profile-extraction](skills/cv-1-profile-extraction/SKILL.md)** — parses your LinkedIn PDF, existing CV, LinkedIn URL, or pasted text into structured profile data
2. **[cv-2-job-analysis](skills/cv-2-job-analysis/SKILL.md)** — extracts requirements, ATS keywords, and priority ratings from any job description
3. **[cv-3-tailoring](skills/cv-3-tailoring/SKILL.md)** — performs gap analysis, asks targeted questions to surface achievements, writes the full CV, and scores it (0–100) on keyword coverage, role fit, and content quality
4. **[cv-4-export](skills/cv-4-export/SKILL.md)** — converts CV content to DOCX and PDF; the agent detects its environment and installs any required packages automatically

## Setup by Platform

### Langdock (Agents)
Langdock supports custom agents with instructions, knowledge files, and multi-agent delegation.

**Option A — Single agent (simplest):**
1. Go to **Agents** → **Create Agent**
2. Set name to `Resume Builder` and add a short description
3. Paste the contents of `resume-builder.agent.md` into the **Instructions** field
4. Under **Knowledge**, upload all skill files and the layout templates so the agent can read them during the workflow:
   - `skills/cv-1-profile-extraction/SKILL.md`
   - `skills/cv-2-job-analysis/SKILL.md`
   - `skills/cv-3-tailoring/SKILL.md`
   - `skills/cv-4-export/SKILL.md`
   - `templates/standard-ats.pdf` *(visual layout reference — the agent uses this to match fonts, margins, and structure at export time)*
   - `templates/standard-ats.docx` *(base DOCX template used by the export script)*
5. Under **Actions → Capabilities**, enable **Data Analysis** (lets the agent run the Python export scripts)
6. Set **Creativity** slider to low (0.2–0.3) for consistent, professional output
7. Optionally add **Conversation Starters** like: *"Build a CV from my LinkedIn profile for this job description"*

**Option B — Multi-agent (advanced):**
Create separate agents for each skill (cv-1-profile-extraction, cv-2-job-analysis, cv-3-tailoring, cv-4-export) with their respective `SKILL.md` as instructions. Then create an orchestrator agent using `resume-builder.agent.md` and attach the skill agents via **Actions → Other Agents** for delegation.

> **DOCX/PDF export:** With Data Analysis enabled, the agent will detect its environment, install any missing dependencies with `pip`, and run the export scripts automatically — no manual setup needed.

> **Tip:** If your Langdock workspace has the Slack or Teams integration, you can chat with the Resume Builder agent directly from Slack or Microsoft Teams.

### Perplexity (Spaces + Computer)
Perplexity doesn't support agent/skill files natively, but you can replicate the full workflow — including DOCX and PDF generation — using a **Space** with custom instructions and **Computer mode** for file export.

**Step 1: Create and configure the Space**
1. Go to **Spaces** in the left sidebar → **Create new Space**
2. Open the Space settings and paste the contents of `resume-builder.agent.md` into the **Custom AI Instructions** field
3. Upload the following files to the Space as knowledge:
   - `skills/cv-1-profile-extraction/SKILL.md`
   - `skills/cv-2-job-analysis/SKILL.md`
   - `skills/cv-3-tailoring/SKILL.md`
   - `skills/cv-4-export/SKILL.md`
   - `skills/cv-4-export/scripts/export_docx.py`
   - `skills/cv-4-export/scripts/export_pdf.py`
   - `templates/standard-ats.pdf` *(visual layout reference for the export step)*
   - `templates/standard-ats.docx` *(base DOCX template used by the export script)*

**Step 2: Run the CV workflow**
1. Start a new Thread in the Space and provide your LinkedIn profile + job description
2. Work through the profile extraction, job analysis, gap analysis, and clarifying questions steps in the thread

**Step 3: Export to DOCX and PDF using Computer mode**
1. Switch to **Computer** mode in Perplexity
2. Ask it to export your CV, for example:
   > *"Please export the CV we just built to DOCX and PDF. Use the export scripts from the knowledge files."*
3. Computer mode will install any required packages automatically and run both export scripts to generate the DOCX and PDF.

## Template Files

The `templates/` folder contains two files used at the export step:

| File | Purpose |
|---|---|
| `standard-ats.pdf` | Visual layout reference — the agent loads this to match Calibri font, A4 page size, narrow margins, and single-column section order |
| `standard-ats.docx` | Base DOCX template — the `export_docx.py` script builds on this so the output inherits the correct styles without needing to reconstruct them from scratch |

**Using the templates with any AI service:**
- Upload or attach **both files** to your agent, space, or conversation alongside the skill files listed above.
- The agent instructions reference `templates/standard-ats.pdf` by path. If your platform places uploaded files in a flat working directory (common in sandboxed environments like Langdock Data Analysis or Perplexity Computer mode), the agent will automatically fall back to looking for `standard-ats.pdf` in the current directory — no manual path adjustment needed.
- If your AI tool does not support file upload (e.g., a plain chat interface), paste the CV content into the conversation and ask the AI to generate DOCX/PDF using Path B (built-in AI generation) described in the agent instructions. The template's layout rules — Calibri 11pt body, bold section headers, reverse-chronological order, 1.5 cm margins — are already encoded in the skill files, so output will still be consistent.
