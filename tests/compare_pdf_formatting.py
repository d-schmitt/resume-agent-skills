#!/usr/bin/env python3
"""Compare formatting between two PDF resume files.

Usage: python compare_pdf_formatting.py <reference.pdf> <generated.pdf>

Compares page count, page dimensions, and presence of all expected text content
(section headings, name header, role titles, company lines, bullet content).
Exit code 0 = pass, 1 = formatting drift detected.
"""

import sys
from pathlib import Path

import pypdf


# Tolerances
PAGE_SIZE_TOLERANCE_PT = 1.0  # points


def extract_info(pdf_path):
    """Return page count, page sizes, and full concatenated text per page."""
    reader = pypdf.PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        text = page.extract_text() or ""
        pages.append({"width_pt": width, "height_pt": height, "text": text})
    return pages


def extract_text_tokens(pages):
    """Return a flat set of non-empty lines across all pages, lowercased."""
    lines = set()
    for p in pages:
        for line in p["text"].splitlines():
            stripped = line.strip()
            if stripped:
                lines.add(stripped.lower())
    return lines


def compare_page_count(ref_pages, gen_pages):
    failures = []
    if len(ref_pages) != len(gen_pages):
        failures.append(
            f"  FAIL page_count: ref={len(ref_pages)}, gen={len(gen_pages)}"
        )
    return failures


def compare_page_dimensions(ref_pages, gen_pages):
    failures = []
    for i, (rp, gp) in enumerate(zip(ref_pages, gen_pages)):
        for key in ("width_pt", "height_pt"):
            diff = abs(rp[key] - gp[key])
            if diff > PAGE_SIZE_TOLERANCE_PT:
                failures.append(
                    f"  FAIL page[{i}].{key}: ref={rp[key]:.1f}, gen={gp[key]:.1f}"
                )
    return failures


def compare_text_content(ref_pages, gen_pages):
    """Check that every non-trivial line from the reference appears in the generated PDF."""
    failures = []
    ref_tokens = extract_text_tokens(ref_pages)
    gen_tokens = extract_text_tokens(gen_pages)

    # Lines present in reference but missing from generated
    missing = [t for t in ref_tokens if t not in gen_tokens and len(t) > 4]
    if missing:
        for m in sorted(missing)[:15]:  # cap output at 15
            failures.append(f"  FAIL missing text: \"{m}\"")

    return failures


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_pdf_formatting.py <reference.pdf> <generated.pdf>")
        sys.exit(1)

    ref_path = Path(sys.argv[1])
    gen_path = Path(sys.argv[2])

    if not ref_path.exists():
        print(f"Error: Reference file not found: {ref_path}")
        sys.exit(1)
    if not gen_path.exists():
        print(f"Error: Generated file not found: {gen_path}")
        sys.exit(1)

    print(f"Analyzing reference: {ref_path}")
    ref_pages = extract_info(ref_path)
    print(f"Analyzing generated: {gen_path}")
    gen_pages = extract_info(gen_path)

    all_failures = []

    print("\n--- Page Count ---")
    failures = compare_page_count(ref_pages, gen_pages)
    all_failures.extend(failures)
    print(failures[0] if failures else "  PASS")

    print("\n--- Page Dimensions ---")
    failures = compare_page_dimensions(ref_pages, gen_pages)
    all_failures.extend(failures)
    if failures:
        for f in failures:
            print(f)
    else:
        print("  PASS")

    print("\n--- Text Content ---")
    failures = compare_text_content(ref_pages, gen_pages)
    all_failures.extend(failures)
    if failures:
        for f in failures:
            print(f)
    else:
        print("  PASS")

    print(f"\n{'='*50}")
    if all_failures:
        print(f"RESULT: FAIL ({len(all_failures)} mismatches)")
        sys.exit(1)
    else:
        print("RESULT: PASS (PDF matches reference)")
        sys.exit(0)


if __name__ == "__main__":
    main()
