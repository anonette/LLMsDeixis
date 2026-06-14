#!/usr/bin/env python3
"""Generic Markdown -> Word .docx with embedded figures, tables, blockquotes.
Usage: python build_docx_from_md.py SOURCE.md OUTPUT.docx"""
from __future__ import annotations
import re, sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
NAVY = RGBColor(0x06, 0x47, 0x7D)


def add_runs(p, text):
    # bold **..**, italic *..* / _.._, code `..`
    i = 0
    for m in re.finditer(r'\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`', text):
        if m.start() > i:
            p.add_run(text[i:m.start()])
        if m.group(1) is not None:
            r = p.add_run(m.group(1)); r.bold = True
        elif m.group(2) is not None:
            r = p.add_run(m.group(2)); r.italic = True
        else:
            r = p.add_run(m.group(3)); r.font.name = "Consolas"
        i = m.end()
    if i < len(text):
        p.add_run(text[i:])


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_absolute():
        src = ROOT / src
    if not out.is_absolute():
        out = ROOT / out
    lines = src.read_text(encoding="utf-8").splitlines()
    doc = Document()
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip("\n")
        s = ln.strip()
        # image
        mimg = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', s)
        # table block
        if "|" in s and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:|-]+\|', lines[i + 1]):
            rows = []
            while i < len(lines) and "|" in lines[i]:
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            header = rows[0]; body = [r for r in rows[2:]]
            t = doc.add_table(rows=1, cols=len(header)); t.style = "Light Grid Accent 1"
            for j, c in enumerate(header):
                cell = t.rows[0].cells[j]; cell.paragraphs[0].clear(); add_runs(cell.paragraphs[0], c)
                for run in cell.paragraphs[0].runs: run.bold = True
            for r in body:
                cells = t.add_row().cells
                for j, c in enumerate(r[:len(header)]):
                    cells[j].paragraphs[0].clear(); add_runs(cells[j].paragraphs[0], c)
            continue
        if mimg:
            p = ROOT / mimg.group(2)
            if not p.exists():
                p = (src.parent / mimg.group(2))
            if p.exists():
                doc.add_picture(str(p), width=Inches(6.3))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1; continue
        if s.startswith("#"):
            lvl = len(s) - len(s.lstrip("#"))
            txt = s.lstrip("#").strip()
            h = doc.add_heading("", level=min(lvl, 4)); add_runs(h, txt)
            i += 1; continue
        if s.startswith(">"):
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.3)
            add_runs(p, s.lstrip(">").strip())
            for run in p.runs: run.italic = True
            i += 1; continue
        if re.match(r'^[-*]\s+', s):
            p = doc.add_paragraph(style="List Bullet"); add_runs(p, re.sub(r'^[-*]\s+', '', s))
            i += 1; continue
        if re.match(r'^\d+\.\s+', s):
            p = doc.add_paragraph(style="List Number"); add_runs(p, re.sub(r'^\d+\.\s+', '', s))
            i += 1; continue
        if s == "":
            i += 1; continue
        p = doc.add_paragraph(); add_runs(p, s)
        i += 1
    doc.save(str(out))
    print("Saved", out.name)


if __name__ == "__main__":
    main()
