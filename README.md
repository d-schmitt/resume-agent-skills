# Resume Builder — AI Agent + Skills Package

Build a tailored, ATS-friendly CV for any job description using your LinkedIn profile or existing resume. Powered by modular AI skills that work with GitHub Copilot, Claude Code, Perplexity, Langdock, or any AI tool that supports custom instructions.

## What It Does

1. **Extracts** your professional profile from LinkedIn, pasted text, or a resume file
2. **Analyzes** the target job description for requirements, keywords, and themes
3. **Identifies gaps** and asks you targeted clarifying questions
4. **Writes** a complete, tailored CV with strong bullet points and ATS keywords
5. **Exports** to professional DOCX and PDF (Calibri, A4, single-column, ATS-optimized)

## Quick Start

### Prerequisites
- Python 3.13.7
- An AI tool that supports custom agents/skills (GitHub Copilot, Claude Code, Perplexity, Langdock, etc.)

### Install Dependencies
```bash
pip install -r skills/cv-export/scripts/requirements.txt
```

### Usage
In your AI chat, type `/build-resume` (or invoke the `resume-builder` agent) and provide:
- Your **LinkedIn URL**, or paste your profile text, or attach a resume file
- The **job description URL** or paste the job description

The agent will guide you through the full workflow.

## Installation by Platform

### VS Code GitHub Copilot
Copy files into your project's `.github/` directory:
```bash
# From the repo root:
cp resume-builder.agent.md  YOUR_PROJECT/.github/agents/
cp -r skills/*              YOUR_PROJECT/.github/skills/
cp -r prompts/*             YOUR_PROJECT/.github/prompts/
```

Or for personal (cross-workspace) use:
```bash
# macOS:
cp resume-builder.agent.md  ~/Library/Application\ Support/Code/User/agents/
# Linux:
cp resume-builder.agent.md  ~/.config/Code/User/agents/
```

### Claude Code
```bash
cp -r skills/*  YOUR_PROJECT/.claude/skills/
```

### Generic / Other AI Tools
Use the repository as-is. Point your AI tool to:
- `resume-builder.agent.md` as the main instructions
- `skills/*/SKILL.md` as the skill definitions
- `skills/cv-export/scripts/` for the export pipeline

### Perplexity (Spaces + Computer)
Perplexity doesn't support agent/skill files natively, but you can replicate the full workflow — including DOCX and PDF generation — using a **Space** with custom instructions and **Computer mode** for file export.

**Step 1: Create and configure the Space**
1. Go to **Spaces** in the left sidebar → **Create new Space**
2. Open the Space settings and paste the contents of `resume-builder.agent.md` into the **Custom AI Instructions** field
3. Upload the following files to the Space as knowledge:
   - `skills/profile-extraction/SKILL.md`
   - `skills/job-analysis/SKILL.md`
   - `skills/cv-tailoring/SKILL.md`
   - `skills/cv-tailoring/references/cv-structure.md`
   - `skills/cv-export/SKILL.md`
   - `skills/cv-export/scripts/export_docx.py`
   - `skills/cv-export/scripts/export_pdf.py`
   - `skills/cv-export/scripts/requirements.txt`
   - `examples/sample-output.md`

**Step 2: Run the CV workflow**
1. Start a new Thread in the Space and provide your LinkedIn profile + job description
2. Work through the profile extraction, job analysis, gap analysis, and clarifying questions steps in the thread

**Step 3: Export to DOCX and PDF using Computer mode**
1. Switch to **Computer** mode in Perplexity
2. Ask it to export your CV, for example:
   > *"Please export the CV we just built to DOCX and PDF. Use the export scripts from the knowledge files. Install Python and any required packages if they are not already available."*
3. Computer mode will take care of the rest — it can install Python if needed, install `python-docx` via pip, run `export_docx.py` to generate the DOCX, and produce a PDF using whichever tool it finds available (Microsoft Word, LibreOffice, or an online converter)

### Langdock (Agents)
Langdock supports custom agents with instructions, knowledge files, and multi-agent delegation.

**Option A — Single agent (simplest):**
1. Go to **Agents** → **Create Agent**
2. Set name to `Resume Builder` and add a short description
3. Paste the full contents of `resume-builder.agent.md` into the **Instructions** field (up to 40,000 characters — append the contents of each `SKILL.md` and `cv-structure.md` into the same instructions block)
4. Under **Knowledge**, upload:
   - `examples/sample-output.md`
   - `skills/cv-export/SKILL.md` (so the agent knows the exact JSON schema to produce)
   - `skills/cv-export/scripts/export_docx.py`
   - `skills/cv-export/scripts/export_pdf.py`
   - `skills/cv-export/scripts/requirements.txt`
5. Under **Actions → Capabilities**, enable **Data Analysis** (lets the agent run the Python export scripts)
6. Set **Creativity** slider to low (0.2–0.3) for consistent, professional output
7. Optionally add **Conversation Starters** like: *"Build a CV from my LinkedIn profile for this job description"*

**Option B — Multi-agent (advanced):**
Create separate agents for each skill (profile-extraction, job-analysis, cv-tailoring, cv-export) with their respective `SKILL.md` as instructions. Then create an orchestrator agent using `resume-builder.agent.md` and attach the skill agents via **Actions → Other Agents** for delegation.

> **DOCX/PDF export:** With Data Analysis enabled, the agent can run the Python export scripts directly. The scripts require `python-docx` — if the sandbox doesn't have it pre-installed, add a line to the agent instructions telling it to run `pip install python-docx` before executing the export. PDF conversion via `docx2pdf` requires Microsoft Word, which won't be available in the sandbox; the agent will produce the DOCX and you can convert to PDF locally if needed.

> **Tip:** If your Langdock workspace has the Slack or Teams integration, you can chat with the Resume Builder agent directly from Slack or Microsoft Teams.

### Single-File Use
If your tool doesn't support the skills folder structure, you can use `resume-builder.agent.md` on its own — it contains the full workflow and references to the skill files. The AI will read the skill files as needed.

## Project Structure

```
resume-agent-skills/
├── resume-builder.agent.md           # Main orchestrator agent
├── skills/
│   ├── profile-extraction/
│   │   └── SKILL.md                  # Extract profile data from any source
│   ├── job-analysis/
│   │   └── SKILL.md                  # Analyze job description
│   ├── cv-tailoring/
│   │   ├── SKILL.md                  # Gap analysis + CV writing
│   │   └── references/
│   │       └── cv-structure.md       # Section templates, bullet patterns
│   └── cv-export/
│       ├── SKILL.md                  # Export orchestration
│       └── scripts/
│           ├── export_docx.py        # DOCX generation (python-docx)
│           ├── export_pdf.py         # PDF conversion (docx2pdf / LibreOffice)
│           └── requirements.txt      # Python dependencies
├── prompts/
│   └── build-resume.prompt.md        # Quick-start /build-resume command
├── tests/                            # Formatting validation tests
│   ├── analyze_formatting.py
│   ├── compare_formatting.py
│   ├── test_export_pipeline.py
│   └── test_data/
└── examples/
    └── sample-output.md              # Example CV structure
```

## Skills Overview

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `profile-extraction` | Parse professional profile | LinkedIn URL, text, or file | Structured profile data |
| `job-analysis` | Analyze job requirements | Job description URL or text | Requirements, keywords, priorities |
| `cv-tailoring` | Write tailored CV content | Profile + job analysis | CV in markdown + advice |
| `cv-export` | Generate formatted documents | CV markdown | DOCX + PDF files |

Each skill can be used independently or as part of the full pipeline.

## Output Format

The generated CV uses a clean, ATS-friendly format:
- **Font**: Calibri throughout
- **Page**: A4, narrow margins (0.5in top/bottom, 0.67in left/right)
- **Layout**: Single-column, no tables/images/text boxes
- **Sections**: Name → Contact → Summary → Key Skills → Technical Skills → Experience → Education → Certifications → Awards → Community

## PDF Generation

PDF conversion requires one of:
- **Microsoft Word** + `docx2pdf` (macOS/Windows) — best fidelity
- **LibreOffice** (all platforms) — `brew install --cask libreoffice` on macOS

The export script tries both automatically and reports which method was used.

## Running Tests

The test suite validates that the export pipeline produces DOCX files matching the reference formatting:

```bash
# Install test dependencies (same as export)
pip install -r skills/cv-export/scripts/requirements.txt

# Run the full pipeline test
python tests/test_export_pipeline.py
```

This generates a DOCX from fictional test data and compares its formatting against the reference document.

## Future Extensions

- **Cover letter generation** — reuses profile-extraction and job-analysis skills
- **Multi-language support** — CV generation in German, French, etc.
- **Interview preparation** — skill that uses job analysis to generate prep questions

## License

MIT
