#!/usr/bin/env python3
"""Convert a Markdown doc to a styled, self-contained HTML (images base64-embedded
so the file travels alone). Usage: python md_to_html.py FILE.md [FILE2.md ...]"""
from __future__ import annotations
import base64, re, sys
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:880px;margin:0 auto;
padding:40px 28px;color:#222;line-height:1.55;}
h1{color:#06477d;border-bottom:3px solid #06A77D;padding-bottom:10px;font-size:1.9em;}
h2{color:#06477d;border-bottom:1px solid #ccc;padding-bottom:5px;margin-top:1.8em;}
h3{color:#205;margin-top:1.3em;}
blockquote{border-left:4px solid #06A77D;background:#f4faf8;margin:1em 0;padding:10px 16px;border-radius:4px;}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.94em;}
th{background:#eafaf3;color:#06477d;border:1px solid #bbb;padding:7px;}
td{border:1px solid #bbb;padding:7px;}
img{max-width:100%;height:auto;display:block;margin:1.2em auto;border:1px solid #e0e0e0;border-radius:6px;
box-shadow:0 3px 12px rgba(0,0,0,.08);}
code{background:#eef;padding:1px 5px;border-radius:3px;}
em{color:#444;}
"""


def embed_images(html, base):
    def repl(m):
        src = m.group(1)
        p = (base / src).resolve()
        if p.exists() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif"):
            data = base64.b64encode(p.read_bytes()).decode()
            mt = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else p.suffix[1:]
            return f'src="data:image/{mt};base64,{data}"'
        return m.group(0)
    return re.sub(r'src="([^"]+)"', repl, html)


def main():
    for arg in sys.argv[1:]:
        md = (ROOT / arg) if not Path(arg).is_absolute() else Path(arg)
        body = markdown.markdown(md.read_text(encoding="utf-8"),
                                 extensions=["tables", "fenced_code", "sane_lists", "toc"])
        body = embed_images(body, md.parent)
        html = (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
                f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
                f"<title>{md.stem}</title><style>{CSS}</style></head><body>{body}</body></html>")
        out = md.with_suffix(".html")
        out.write_text(html, encoding="utf-8")
        print("Wrote", out.name, f"({round(len(html)/1024)} KB)")


if __name__ == "__main__":
    main()
