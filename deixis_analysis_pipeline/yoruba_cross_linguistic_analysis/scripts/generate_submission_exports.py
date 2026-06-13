#!/usr/bin/env python3
"""Generate HTML and PDF exports for the submission draft."""

from pathlib import Path
import markdown

try:
    from weasyprint import HTML
except Exception:
    HTML = None


BASE_PATH = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
MD_FILE = BASE_PATH / "Cultural_and_Linguistic_Prealignment_Submission_Draft.md"
HTML_FILE = BASE_PATH / "Cultural_and_Linguistic_Prealignment_Submission_Draft.html"
PDF_FILE = BASE_PATH / "Cultural_and_Linguistic_Prealignment_Submission_Draft.pdf"


def build_html() -> str:
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    viz_path = BASE_PATH / "visualizations"
    md_content = md_content.replace("visualizations/", f"file:///{viz_path}/")

    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "nl2br",
            "sane_lists",
        ]
    )
    body = md.convert(md_content)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Cultural and Linguistic Pre-Alignment in Multilingual LLMs</title>
  <style>
    @page {{
      size: A4;
      margin: 2.5cm;
      @bottom-center {{
        content: counter(page);
        font-size: 10pt;
        color: #666;
      }}
    }}

    body {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: 11pt;
      line-height: 1.65;
      color: #222;
      max-width: 100%;
      margin: 0;
      padding: 0;
    }}

    h1 {{
      font-size: 22pt;
      margin: 0 0 18px 0;
      padding-bottom: 10px;
      border-bottom: 2px solid #1f4e79;
      page-break-before: always;
    }}

    h1:first-child {{
      page-break-before: avoid;
    }}

    h2 {{
      font-size: 16pt;
      color: #1f4e79;
      margin-top: 28px;
      margin-bottom: 10px;
      border-bottom: 1px solid #d8d8d8;
      padding-bottom: 4px;
    }}

    h3 {{
      font-size: 13pt;
      margin-top: 22px;
      margin-bottom: 8px;
      color: #333;
    }}

    h4 {{
      font-size: 11.5pt;
      margin-top: 16px;
      margin-bottom: 6px;
      color: #444;
    }}

    p {{
      margin: 0 0 12px 0;
      text-align: justify;
    }}

    ul, ol {{
      margin: 8px 0 14px 24px;
    }}

    li {{
      margin: 4px 0;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      font-size: 10pt;
      page-break-inside: avoid;
    }}

    th, td {{
      border: 1px solid #cfcfcf;
      padding: 8px;
      vertical-align: top;
    }}

    th {{
      background: #f2f5f9;
      font-weight: 700;
    }}

    blockquote {{
      border-left: 4px solid #999;
      background: #fafafa;
      padding: 10px 16px;
      margin: 14px 0;
      font-style: italic;
    }}

    code {{
      background: #f3f3f3;
      padding: 2px 4px;
      font-family: "Courier New", monospace;
      font-size: 10pt;
    }}

    img {{
      display: block;
      max-width: 100%;
      height: auto;
      margin: 18px auto 10px auto;
      page-break-inside: avoid;
    }}

    img + em {{
      display: block;
      text-align: center;
      color: #555;
      font-size: 10pt;
      margin: 0 24px 18px 24px;
    }}

    hr {{
      border: none;
      border-top: 1px solid #ddd;
      margin: 28px 0;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    html = build_html()

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML written to: {HTML_FILE}")

    if HTML is None:
        print("WeasyPrint not available; skipped PDF generation.")
        return

    HTML(string=html).write_pdf(PDF_FILE)
    print(f"PDF written to: {PDF_FILE}")


if __name__ == "__main__":
    main()
