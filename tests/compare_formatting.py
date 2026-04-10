#!/usr/bin/env python3
"""Compare formatting between two DOCX files.

Usage: python compare_formatting.py <reference.docx> <generated.docx>

Compares page setup, font usage, paragraph spacing, heading styles,
and bullet formatting. Reports mismatches with tolerances.
Exit code 0 = pass, 1 = formatting drift detected.
"""

import json
import sys
from pathlib import Path

# Allow importing analyze_formatting from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from analyze_formatting import analyze


# Tolerances
MARGIN_TOLERANCE_IN = 0.02
SPACING_TOLERANCE_PT = 1.0
FONT_SIZE_TOLERANCE_PT = 0.5


def compare_values(label, ref_val, gen_val, tolerance=None):
    """Compare two values, return (pass, message)."""
    if ref_val is None and gen_val is None:
        return True, None
    if ref_val is None or gen_val is None:
        return False, f"  FAIL {label}: ref={ref_val}, gen={gen_val}"
    if tolerance is not None and isinstance(ref_val, (int, float)) and isinstance(gen_val, (int, float)):
        if abs(ref_val - gen_val) <= tolerance:
            return True, None
        return False, f"  FAIL {label}: ref={ref_val}, gen={gen_val} (tolerance={tolerance})"
    if ref_val != gen_val:
        return False, f"  FAIL {label}: ref={ref_val}, gen={gen_val}"
    return True, None


def compare_page_setup(ref, gen):
    """Compare page setup between reference and generated."""
    failures = []
    ref_s = ref["page_setup"][0] if ref["page_setup"] else {}
    gen_s = gen["page_setup"][0] if gen["page_setup"] else {}

    for key in ["page_width_in", "page_height_in"]:
        ok, msg = compare_values(f"page_setup.{key}", ref_s.get(key), gen_s.get(key), MARGIN_TOLERANCE_IN)
        if not ok:
            failures.append(msg)

    for key in ["margin_top_in", "margin_bottom_in", "margin_left_in", "margin_right_in"]:
        ok, msg = compare_values(f"page_setup.{key}", ref_s.get(key), gen_s.get(key), MARGIN_TOLERANCE_IN)
        if not ok:
            failures.append(msg)

    return failures


def compare_doc_defaults(ref, gen):
    """Compare document-level default fonts."""
    failures = []
    ref_d = ref.get("doc_defaults", {})
    gen_d = gen.get("doc_defaults", {})

    for key in ["font_ascii", "font_hAnsi"]:
        ok, msg = compare_values(f"doc_defaults.{key}", ref_d.get(key), gen_d.get(key))
        if not ok:
            failures.append(msg)

    return failures


def collect_formatting_patterns(data):
    """Extract formatting patterns from paragraphs for comparison."""
    patterns = {
        "name": None,           # First paragraph (name)
        "contact": None,        # Contact line
        "section_headings": [],  # Section headings (with borders)
        "job_titles": [],       # Job title paragraphs
        "company_lines": [],    # Company/date lines
        "bullets": [],          # Bullet paragraphs
        "tech_skills": [],      # Technical skill lines
        "cert_lines": [],       # Certification lines
    }

    for p in data["paragraphs"]:
        text = p.get("text_preview", "")
        if not text.strip():
            continue

        # Detect pattern by formatting characteristics
        runs = p.get("runs", [])
        if not runs:
            continue

        first_run = runs[0]
        has_border = "borders" in p and "bottom" in p.get("borders", {})
        has_numbering = "num_level" in p
        # Also detect text-based bullets (manual bullet char)
        has_text_bullet = text.lstrip().startswith("\u2022") or text.lstrip().startswith("\u00b7")
        font_size = first_run.get("font_size_pt")
        is_bold = first_run.get("bold", False)
        color = first_run.get("color", "")

        # Name: large bold text, first non-empty paragraph
        if patterns["name"] is None and font_size and font_size >= 16:
            patterns["name"] = {
                "font_size_pt": font_size,
                "bold": is_bold,
                "color": color,
                "space_after_pt": p.get("space_after_pt"),
            }
            continue

        # Section headings: bold + bottom border
        if has_border and is_bold:
            patterns["section_headings"].append({
                "bold": is_bold,
                "color": color,
                "space_before_pt": p.get("space_before_pt"),
                "space_after_pt": p.get("space_after_pt"),
                "border_color": p["borders"]["bottom"].get("color"),
            })
            continue

        # Contact lines: small muted text near the top
        if patterns["contact"] is None and font_size and font_size <= 9 and color in ("555555", "theme:NONE"):
            patterns["contact"] = {
                "font_size_pt": font_size,
                "color": color,
                "space_after_pt": p.get("space_after_pt"),
            }
            continue

        # Bullet points (numbering XML or text-based bullet char)
        if has_numbering or has_text_bullet:
            patterns["bullets"].append({
                "font_size_pt": font_size,
                "space_after_pt": p.get("space_after_pt"),
            })
            continue

        # Job titles: bold, ~9pt, dark color
        if is_bold and font_size and 8.5 <= font_size <= 10 and color in ("1A1A1A", None, ""):
            sp_before = p.get("space_before_pt")
            if sp_before and sp_before >= 4:
                patterns["job_titles"].append({
                    "font_size_pt": font_size,
                    "bold": is_bold,
                    "color": color,
                    "space_before_pt": sp_before,
                    "space_after_pt": p.get("space_after_pt"),
                })
                continue

        # Company lines: small, grey text
        if color in ("888888",) and font_size and font_size <= 8.5:
            patterns["company_lines"].append({
                "font_size_pt": font_size,
                "color": color,
                "space_after_pt": p.get("space_after_pt"),
            })
            continue

        # Tech skill lines: mixed bold label + normal value
        if len(runs) >= 2 and runs[0].get("bold") and not runs[1].get("bold", False):
            if font_size and font_size <= 9:
                patterns["tech_skills"].append({
                    "font_size_pt": font_size,
                    "space_after_pt": p.get("space_after_pt"),
                })
                continue

    return patterns


def compare_patterns(ref_patterns, gen_patterns):
    """Compare extracted formatting patterns."""
    failures = []

    # Name formatting
    if ref_patterns["name"] and gen_patterns["name"]:
        rn = ref_patterns["name"]
        gn = gen_patterns["name"]
        ok, msg = compare_values("name.font_size", rn["font_size_pt"], gn["font_size_pt"], FONT_SIZE_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("name.bold", rn["bold"], gn["bold"])
        if not ok:
            failures.append(msg)

    # Section headings
    if ref_patterns["section_headings"] and gen_patterns["section_headings"]:
        rh = ref_patterns["section_headings"][0]
        gh = gen_patterns["section_headings"][0]
        ok, msg = compare_values("heading.bold", rh["bold"], gh["bold"])
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("heading.space_before", rh.get("space_before_pt"), gh.get("space_before_pt"), SPACING_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("heading.space_after", rh.get("space_after_pt"), gh.get("space_after_pt"), SPACING_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("heading.border_color", rh.get("border_color"), gh.get("border_color"))
        if not ok:
            failures.append(msg)
    elif ref_patterns["section_headings"] and not gen_patterns["section_headings"]:
        failures.append("  FAIL: Reference has section headings with borders, generated does not")

    # Bullets
    if ref_patterns["bullets"] and gen_patterns["bullets"]:
        rb = ref_patterns["bullets"][0]
        gb = gen_patterns["bullets"][0]
        ok, msg = compare_values("bullet.font_size", rb.get("font_size_pt"), gb.get("font_size_pt"), FONT_SIZE_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("bullet.space_after", rb.get("space_after_pt"), gb.get("space_after_pt"), SPACING_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
    elif ref_patterns["bullets"] and not gen_patterns["bullets"]:
        failures.append("  FAIL: Reference has bullet points, generated does not")

    # Job titles
    if ref_patterns["job_titles"] and gen_patterns["job_titles"]:
        rj = ref_patterns["job_titles"][0]
        gj = gen_patterns["job_titles"][0]
        ok, msg = compare_values("job_title.font_size", rj.get("font_size_pt"), gj.get("font_size_pt"), FONT_SIZE_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("job_title.bold", rj["bold"], gj["bold"])
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("job_title.space_before", rj.get("space_before_pt"), gj.get("space_before_pt"), SPACING_TOLERANCE_PT)
        if not ok:
            failures.append(msg)

    # Company lines
    if ref_patterns["company_lines"] and gen_patterns["company_lines"]:
        rc = ref_patterns["company_lines"][0]
        gc = gen_patterns["company_lines"][0]
        ok, msg = compare_values("company.font_size", rc.get("font_size_pt"), gc.get("font_size_pt"), FONT_SIZE_TOLERANCE_PT)
        if not ok:
            failures.append(msg)
        ok, msg = compare_values("company.color", rc.get("color"), gc.get("color"))
        if not ok:
            failures.append(msg)

    # Technical skills
    if ref_patterns["tech_skills"] and gen_patterns["tech_skills"]:
        rt = ref_patterns["tech_skills"][0]
        gt = gen_patterns["tech_skills"][0]
        ok, msg = compare_values("tech_skill.font_size", rt.get("font_size_pt"), gt.get("font_size_pt"), FONT_SIZE_TOLERANCE_PT)
        if not ok:
            failures.append(msg)

    return failures


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_formatting.py <reference.docx> <generated.docx>")
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
    ref_data = analyze(str(ref_path))
    print(f"Analyzing generated: {gen_path}")
    gen_data = analyze(str(gen_path))

    all_failures = []

    print("\n--- Page Setup ---")
    failures = compare_page_setup(ref_data, gen_data)
    all_failures.extend(failures)
    if failures:
        for f in failures:
            print(f)
    else:
        print("  PASS")

    print("\n--- Document Defaults ---")
    failures = compare_doc_defaults(ref_data, gen_data)
    all_failures.extend(failures)
    if failures:
        for f in failures:
            print(f)
    else:
        print("  PASS")

    print("\n--- Formatting Patterns ---")
    ref_patterns = collect_formatting_patterns(ref_data)
    gen_patterns = collect_formatting_patterns(gen_data)
    failures = compare_patterns(ref_patterns, gen_patterns)
    all_failures.extend(failures)
    if failures:
        for f in failures:
            print(f)
    else:
        print("  PASS")

    # Summary
    print(f"\n{'='*50}")
    if all_failures:
        print(f"RESULT: FAIL ({len(all_failures)} formatting mismatches)")
        sys.exit(1)
    else:
        print("RESULT: PASS (formatting matches reference)")
        sys.exit(0)


if __name__ == "__main__":
    main()
