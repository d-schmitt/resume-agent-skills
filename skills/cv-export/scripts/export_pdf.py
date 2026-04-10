#!/usr/bin/env python3
"""Convert a DOCX resume to PDF.

Usage: python export_pdf.py <input.docx> [--output <filename.pdf>]

Conversion methods (tried in order):
1. docx2pdf (requires MS Word on macOS/Windows)
2. LibreOffice headless CLI (cross-platform)

If neither is available, prints an error with instructions.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def convert_with_docx2pdf(docx_path, pdf_path):
    """Try conversion using docx2pdf (requires MS Word)."""
    try:
        from docx2pdf import convert
        convert(str(docx_path), str(pdf_path))
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"docx2pdf failed: {e}", file=sys.stderr)
        return False


def convert_with_libreoffice(docx_path, pdf_path):
    """Try conversion using LibreOffice CLI."""
    lo_path = shutil.which("libreoffice") or shutil.which("soffice")
    if not lo_path:
        # Check common macOS path
        mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if Path(mac_path).exists():
            lo_path = mac_path
    if not lo_path:
        return False

    try:
        output_dir = pdf_path.parent
        result = subprocess.run(
            [lo_path, "--headless", "--convert-to", "pdf",
             "--outdir", str(output_dir), str(docx_path)],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"LibreOffice error: {result.stderr}", file=sys.stderr)
            return False

        # LibreOffice outputs to <stem>.pdf in outdir
        lo_output = output_dir / (docx_path.stem + ".pdf")
        if lo_output.exists() and lo_output != pdf_path:
            lo_output.rename(pdf_path)
        return pdf_path.exists()
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        print("LibreOffice conversion timed out.", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert DOCX to PDF")
    parser.add_argument("input", help="Path to input DOCX file")
    parser.add_argument("--output", "-o", default=None,
                        help="Output PDF filename (default: same name with .pdf)")
    args = parser.parse_args()

    docx_path = Path(args.input)
    if not docx_path.exists():
        print(f"Error: Input file not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        pdf_path = Path(args.output)
    else:
        pdf_path = docx_path.with_suffix(".pdf")

    print(f"Converting {docx_path} -> {pdf_path}")

    # Try method 1: docx2pdf
    if convert_with_docx2pdf(docx_path, pdf_path):
        print(f"PDF generated (via docx2pdf): {pdf_path}")
        return

    # Try method 2: LibreOffice
    if convert_with_libreoffice(docx_path, pdf_path):
        print(f"PDF generated (via LibreOffice): {pdf_path}")
        return

    # Nothing worked
    print(
        "Error: Could not convert to PDF. Install one of:\n"
        "  - Microsoft Word + pip install docx2pdf  (macOS/Windows)\n"
        "  - LibreOffice  (all platforms: brew install --cask libreoffice)",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
