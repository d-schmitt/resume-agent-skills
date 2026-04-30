# Resume Builder — AI Agent + Skills Package

An AI agent that turns your LinkedIn profile or CV and a job description into a tailored, ATS-optimized CV — with keyword scoring, gap analysis, and targeted clarifying questions at every step. Exports to DOCX and PDF. Use in Langdock, Perplexity, GitHub Copilot, Claude Code, or any AI tool that supports custom instructions.

**What it does** — four skills, usable together or independently:
1. **[cv_profile_extraction](skills/cv_profile_extraction/SKILL.md)** — parses your LinkedIn PDF, existing CV, LinkedIn URL, or pasted text into structured profile data
2. **[cv_job_analysis](skills/cv_job_analysis/SKILL.md)** — extracts requirements, ATS keywords, and priority ratings from any job description
3. **[cv_tailoring](skills/cv_tailoring/SKILL.md)** — performs gap analysis, asks targeted questions to surface achievements, writes the full CV, and scores it (0–100) on keyword coverage, role fit, and content quality
4. **[cv_export](skills/cv_export/SKILL.md)** — converts CV content to DOCX and PDF; the agent detects its environment and installs any required packages automatically

## Setup by Platform

### Langdock (Agents)
Langdock supports custom agents with instructions, knowledge files, and multi-agent delegation.

**Option A — Single agent (simplest):**
1. Go to **Agents** → **Create Agent**
2. Set name to `Resume Builder` and add a short description
3. Paste the contents of `resume-builder.agent.md` into the **Instructions** field
4. Under **Knowledge**, upload all skill files so the agent can read them during the workflow:
   - `skills/cv_profile_extraction/SKILL.md`
   - `skills/cv_job_analysis/SKILL.md`
   - `skills/cv_tailoring/SKILL.md`
   - `skills/cv_tailoring/references/cv-structure.md`
   - `skills/cv_export/SKILL.md`
   - `skills/cv_export/scripts/export_docx.py`
   - `skills/cv_export/scripts/export_pdf.py`
   - `examples/sample-output.md`
5. Under **Actions → Capabilities**, enable **Data Analysis** (lets the agent run the Python export scripts)
6. Set **Creativity** slider to low (0.2–0.3) for consistent, professional output
7. Optionally add **Conversation Starters** like: *"Build a CV from my LinkedIn profile for this job description"*

**Option B — Multi-agent (advanced):**
Create separate agents for each skill (cv_profile_extraction, cv_job_analysis, cv_tailoring, cv_export) with their respective `SKILL.md` as instructions. Then create an orchestrator agent using `resume-builder.agent.md` and attach the skill agents via **Actions → Other Agents** for delegation.

> **DOCX/PDF export:** With Data Analysis enabled, the agent will detect its environment, install any missing dependencies with `pip`, and run the export scripts automatically — no manual setup needed.

> **Tip:** If your Langdock workspace has the Slack or Teams integration, you can chat with the Resume Builder agent directly from Slack or Microsoft Teams.

### Perplexity (Spaces + Computer)
Perplexity doesn't support agent/skill files natively, but you can replicate the full workflow — including DOCX and PDF generation — using a **Space** with custom instructions and **Computer mode** for file export.

**Step 1: Create and configure the Space**
1. Go to **Spaces** in the left sidebar → **Create new Space**
2. Open the Space settings and paste the contents of `resume-builder.agent.md` into the **Custom AI Instructions** field
3. Upload the following files to the Space as knowledge:
   - `skills/cv_profile_extraction/SKILL.md`
   - `skills/cv_job_analysis/SKILL.md`
   - `skills/cv_tailoring/SKILL.md`
   - `skills/cv_tailoring/references/cv-structure.md`
   - `skills/cv_export/SKILL.md`
   - `skills/cv_export/scripts/export_docx.py`
   - `skills/cv_export/scripts/export_pdf.py`
   - `examples/sample-output.md`

**Step 2: Run the CV workflow**
1. Start a new Thread in the Space and provide your LinkedIn profile + job description
2. Work through the profile extraction, job analysis, gap analysis, and clarifying questions steps in the thread

**Step 3: Export to DOCX and PDF using Computer mode**
1. Switch to **Computer** mode in Perplexity
2. Ask it to export your CV, for example:
   > *"Please export the CV we just built to DOCX and PDF. Use the export scripts from the knowledge files."*
3. Computer mode will install any required packages automatically and run both export scripts to generate the DOCX and PDF.

## License

MIT

