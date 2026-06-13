#!/usr/bin/env python3
"""Convert project Markdown docs to PDF with embedded Unicode font (Yoruba-safe)
and inline figures. Uses markdown + xhtml2pdf (pisa); no pandoc needed.

Usage:
    python md_to_pdf.py            # converts the default doc set
    python md_to_pdf.py FILE.md    # converts one file
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import markdown as md
from xhtml2pdf import pisa

ANALYSIS_ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
DEJAVU = (FONT_DIR / "DejaVuSans.ttf").as_uri()
DEJAVU_B = (FONT_DIR / "DejaVuSans-Bold.ttf").as_uri()
DEJAVU_I = (FONT_DIR / "DejaVuSans-Oblique.ttf").as_uri()

DEFAULT_DOCS = [
    "Open_All_Models_Dilemma_Framing_Account.md",
    "Constrained_All_Models_Dilemma_Framing_Account.md",
    "Discussion_Open_NATLaS_Yoruba_Moral_Stance.md",
    "Open_NATLaS_vs_Cloud_Summary.md",
    "Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md",
    "Deixis_Decision_Effects_Summary.md",
]

CSS = f"""
@font-face {{ font-family: 'DejaVu'; src: url('{DEJAVU}'); }}
@font-face {{ font-family: 'DejaVu'; src: url('{DEJAVU_B}'); font-weight: bold; }}
@font-face {{ font-family: 'DejaVu'; src: url('{DEJAVU_I}'); font-style: italic; }}
@page {{ size: A4; margin: 1.8cm 1.6cm; }}
body {{ font-family: 'DejaVu'; font-size: 10pt; line-height: 1.4; color: #222; }}
h1 {{ font-size: 18pt; color: #06477d; border-bottom: 2px solid #06A77D; padding-bottom: 3pt; }}
h2 {{ font-size: 14pt; color: #06477d; margin-top: 14pt; border-bottom: 1px solid #ccc; }}
h3 {{ font-size: 11.5pt; color: #205; margin-top: 10pt; }}
h4 {{ font-size: 10.5pt; color: #444; }}
p, li {{ font-size: 10pt; }}
code {{ font-family: 'DejaVu'; background: #eef; font-size: 8.5pt; }}
pre {{ background: #f4f4f4; padding: 6pt; font-size: 8pt; }}
blockquote {{ border-left: 3px solid #06A77D; margin-left: 0; padding-left: 8pt; color: #333; background: #f7faf9; }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.5pt; -pdf-keep-with-next: false; }}
th {{ background: #eafaf3; color: #06477d; border: 0.5pt solid #bbb; padding: 3pt; }}
td {{ border: 0.5pt solid #bbb; padding: 3pt; }}
img {{ width: 16.8cm; }}
"""


def convert(md_path: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    body = md.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
        output_format="html5",
    )
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    pdf_path = md_path.with_suffix(".pdf")

    def link_callback(uri, rel):
        if uri.startswith("file:") or uri.startswith("http"):
            return uri
        p = (md_path.parent / uri).resolve()
        return str(p) if p.exists() else uri

    with open(pdf_path, "wb") as fh:
        result = pisa.CreatePDF(html, dest=fh, link_callback=link_callback, encoding="utf-8")
    status = "OK" if not result.err else f"{result.err} errors"
    print(f"  {status}: {pdf_path.name}")
    return pdf_path


def main():
    args = sys.argv[1:]
    docs = [Path(a) for a in args] if args else [ANALYSIS_ROOT / d for d in DEFAULT_DOCS]
    for d in docs:
        d = d if d.is_absolute() else (ANALYSIS_ROOT / d)
        if not d.exists():
            print(f"  SKIP (missing): {d.name}")
            continue
        print(f"Converting {d.name} ...")
        convert(d)


if __name__ == "__main__":
    main()
