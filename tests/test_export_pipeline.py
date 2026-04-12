#!/usr/bin/env python3
"""End-to-end test of the CV export pipeline.

Feeds fictional test data through export_docx.py and export_pdf.py independently,
then compares both outputs against their respective reference files.

Usage: python test_export_pipeline.py
"""

import os
import subprocess
import sys
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent
TESTS_DIR = Path(__file__).parent
TEST_DATA = TESTS_DIR / "test_data" / "fictional_cv_data.json"
OUTPUT_DIR = TESTS_DIR / "output"
REFERENCE_DOCX = TESTS_DIR / "test_data" / "reference_resume.docx"
REFERENCE_PDF = TESTS_DIR / "test_data" / "reference_resume.pdf"
EXPORT_DOCX_SCRIPT = REPO_ROOT / "skills" / "cv-export" / "scripts" / "export_docx.py"
EXPORT_PDF_SCRIPT = REPO_ROOT / "skills" / "cv-export" / "scripts" / "export_pdf.py"
COMPARE_SCRIPT = TESTS_DIR / "compare_formatting.py"
COMPARE_PDF_SCRIPT = TESTS_DIR / "compare_pdf_formatting.py"

OUTPUT_DOCX = OUTPUT_DIR / "test_resume.docx"
OUTPUT_PDF = OUTPUT_DIR / "test_resume.pdf"


def run(cmd, label):
    """Run a command and report result."""
    print(f"\n{'='*60}")
    print(f"STEP: {label}")
    print(f"CMD:  {' '.join(str(c) for c in cmd)}")
    print("-" * 60)
    result = subprocess.run(
        [str(c) for c in cmd],
        capture_output=True, text=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return result.returncode


def main():
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clean previous output
    for f in [OUTPUT_DOCX, OUTPUT_PDF]:
        if f.exists():
            f.unlink()

    python = sys.executable
    results = []

    # Step 1: Generate DOCX
    rc = run(
        [python, EXPORT_DOCX_SCRIPT, TEST_DATA, "--output", OUTPUT_DOCX],
        "Generate DOCX from test data",
    )
    if rc != 0:
        print("\nFATAL: DOCX generation failed")
        sys.exit(1)
    if not OUTPUT_DOCX.exists():
        print(f"\nFATAL: Expected output file not found: {OUTPUT_DOCX}")
        sys.exit(1)
    docx_size = OUTPUT_DOCX.stat().st_size
    print(f"\nDOCX generated: {OUTPUT_DOCX} ({docx_size:,} bytes)")
    results.append(("DOCX generation", "PASS"))

    # Step 2: Generate PDF from JSON directly
    rc = run(
        [python, EXPORT_PDF_SCRIPT, TEST_DATA, "--output", OUTPUT_PDF],
        "Generate PDF from test data",
    )
    if rc != 0:
        print("\nWARNING: PDF generation failed")
        results.append(("PDF generation", "FAIL"))
    elif OUTPUT_PDF.exists():
        pdf_size = OUTPUT_PDF.stat().st_size
        if pdf_size > 0:
            print(f"\nPDF generated: {OUTPUT_PDF} ({pdf_size:,} bytes)")
            results.append(("PDF generation", "PASS"))
        else:
            results.append(("PDF generation", "FAIL (empty file)"))
    else:
        results.append(("PDF generation", "FAIL (file not created)"))

    # Step 3: Compare DOCX formatting against reference
    if REFERENCE_DOCX.exists():
        rc = run(
            [python, COMPARE_SCRIPT, REFERENCE_DOCX, OUTPUT_DOCX],
            "Compare DOCX formatting with reference",
        )
        if rc == 0:
            results.append(("DOCX formatting comparison", "PASS"))
        else:
            results.append(("DOCX formatting comparison", "FAIL"))
    else:
        print(f"\nWARNING: Reference file not found: {REFERENCE_DOCX}")
        print("  To create it: cp tests/output/test_resume.docx tests/test_data/reference_resume.docx")
        results.append(("DOCX formatting comparison", "SKIP (no reference file)"))

    # Step 4: Compare PDF against reference
    if REFERENCE_PDF.exists():
        rc = run(
            [python, COMPARE_PDF_SCRIPT, REFERENCE_PDF, OUTPUT_PDF],
            "Compare PDF formatting with reference",
        )
        if rc == 0:
            results.append(("PDF formatting comparison", "PASS"))
        else:
            results.append(("PDF formatting comparison", "FAIL"))
    else:
        print(f"\nWARNING: Reference file not found: {REFERENCE_PDF}")
        print("  To create it: cp tests/output/test_resume.pdf tests/test_data/reference_resume.pdf")
        results.append(("PDF formatting comparison", "SKIP (no reference file)"))

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print("-" * 60)
    all_pass = True
    for label, status in results:
        icon = "✓" if status == "PASS" else ("⚠" if "SKIP" in status else "✗")
        print(f"  {icon} {label}: {status}")
        if status == "FAIL" or (status.startswith("FAIL")):
            all_pass = False

    print("-" * 60)
    if all_pass:
        print("OVERALL: PASS")
    else:
        print("OVERALL: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
