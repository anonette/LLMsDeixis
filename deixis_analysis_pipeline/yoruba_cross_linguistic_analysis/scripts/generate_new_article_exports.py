#!/usr/bin/env python3
"""Generate HTML and PDF exports for the new comparable article."""

from pathlib import Path
import markdown

BASE = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
MD_FILE = BASE / "New_Article_Comparable_English_Yoruba_Deixis.md"
HTML_FILE = BASE / "New_Article_Comparable_English_Yoruba_Deixis.html"
PDF_FILE = BASE / "New_Article_Comparable_English_Yoruba_Deixis.pdf"


def build_html() -> str:
    md_text = MD_FILE.read_text(encoding="utf-8")
    md_text = md_text.replace("visualizations/", f"file:///{(BASE / 'visualizations')}/")

    body = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "nl2br", "sane_lists"]
    ).convert(md_text)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Deixis Across Languages</title>
  <style>
    @page {{ size: A4; margin: 2.4cm; @bottom-center {{ content: counter(page); color: #666; font-size: 10pt; }} }}
    body {{ font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; line-height: 1.65; color: #222; }}
    h1 {{ font-size: 22pt; border-bottom: 2px solid #1f4e79; padding-bottom: 10px; page-break-before: always; }}
    h1:first-child {{ page-break-before: avoid; }}
    h2 {{ font-size: 16pt; color: #1f4e79; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 28px; }}
    h3 {{ font-size: 13pt; margin-top: 22px; }}
    h4 {{ font-size: 11.5pt; margin-top: 16px; }}
    p {{ text-align: justify; margin: 0 0 12px 0; }}
    ul, ol {{ margin: 8px 0 14px 24px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 18px 0; font-size: 10pt; page-break-inside: avoid; }}
    th, td {{ border: 1px solid #cfcfcf; padding: 8px; vertical-align: top; }}
    th {{ background: #f2f5f9; font-weight: 700; }}
    blockquote {{ border-left: 4px solid #999; background: #fafafa; padding: 10px 16px; margin: 14px 0; font-style: italic; }}
    code {{ background: #f3f3f3; padding: 2px 4px; font-family: 'Courier New', monospace; font-size: 10pt; }}
    img {{ display: block; max-width: 100%; height: auto; margin: 18px auto 10px auto; page-break-inside: avoid; }}
    img + em {{ display: block; text-align: center; color: #555; font-size: 10pt; margin: 0 24px 18px 24px; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    html = build_html()
    HTML_FILE.write_text(html, encoding="utf-8")
    print(f"HTML written to: {HTML_FILE}")


if __name__ == "__main__":
    main()
