#!/usr/bin/env python3
"""Build detailed reports from merged open Yoruba coding outputs."""

from __future__ import annotations

import csv
import json
import os
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


MODULE = Path(__file__).resolve().parent
MERGED_DIR = MODULE / "outputs" / "open_yoruba_coding_merged_20260608"
SOURCE_JSON = MERGED_DIR / "open_yoruba_coded_content_merged.json"
OUT_DIR = MERGED_DIR / "detailed_package_20260608"

MODEL_ORDER = ["GPT-4o", "Claude", "DeepSeek"]
FRAMING_ORDER = [
    "impersonal",
    "second_person",
    "first_person",
    "first_person_plural",
    "reflexive",
    "dialogic",
    "spatial",
    "temporal",
    "cosmological",
]

FRAMING_LABELS = {
    "impersonal": "Impersonal",
    "second_person": "Second Person",
    "first_person": "First Person",
    "first_person_plural": "First Person Plural",
    "reflexive": "Reflexive",
    "dialogic": "Dialogic",
    "spatial": "Spatial",
    "temporal": "Temporal",
    "cosmological": "Cosmological",
}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_rows() -> list[dict]:
    with open(SOURCE_JSON, "r", encoding="utf-8") as handle:
        return json.load(handle)["records"]


def short(text: str, limit: int = 500) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def export_pdf(html_path: Path) -> Path | None:
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge.exists():
        return None
    pdf_path = html_path.with_suffix(".pdf")
    temp_profile = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-open-yoruba-coding")
    temp_profile.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(edge),
        "--headless",
        "--disable-gpu",
        f"--user-data-dir={temp_profile}",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not pdf_path.exists():
        return None
    return pdf_path


def write_review_subset(rows: list[dict], out_dir: Path) -> tuple[Path, Path, Path]:
    subset = [r for r in rows if r.get("needs_second_coder_review")]
    subset_json = out_dir / "review_subset.json"
    subset_csv = out_dir / "review_subset.csv"
    subset_md = out_dir / "review_subset.md"

    with open(subset_json, "w", encoding="utf-8") as handle:
        json.dump({"records": subset, "generated_at": datetime.now().isoformat()}, handle, indent=2, ensure_ascii=False)

    with open(subset_csv, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(subset[0].keys()) if subset else [])
        if subset:
            writer.writeheader()
            writer.writerows(subset)

    lines = [
        "# Second-Coder Review Subset",
        "",
        f"Rows flagged for adjudication: `{len(subset)}`",
        "",
    ]
    for row in subset[:30]:
        lines.extend([
            f"## {row['model_label']} / {row['dilemma_id']} / {row['framing_type']}",
            "",
            f"- preferred_solution: `{row['preferred_solution']}`",
            f"- ethical_preference_type: `{row['ethical_preference_type']}`",
            f"- response_genre: `{row['response_genre']}`",
            f"- language_stability: `{row['language_stability']}`",
            f"- confidence: `{row['confidence']}`",
            "",
            "**Evidence span (Yoruba)**",
            "",
            row['evidence_span_yo'],
            "",
            "**Evidence span (English support)**",
            "",
            row['evidence_span_en'],
            "",
            "**Coding rationale**",
            "",
            row['coding_rationale'],
            "",
        ])
    subset_md.write_text("\n".join(lines), encoding="utf-8")
    return subset_json, subset_csv, subset_md


def write_framing_crosstabs(rows: list[dict], out_dir: Path) -> tuple[Path, Path]:
    crosstab_csv = out_dir / "framing_crosstabs.csv"
    crosstab_md = out_dir / "framing_crosstabs.md"

    output_rows = []
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["model_label"], row["framing_type"])].append(row)

    for model in MODEL_ORDER:
        for framing in FRAMING_ORDER:
            subset = grouped[(model, framing)]
            if not subset:
                continue
            output_rows.append({
                "model": model,
                "framing_type": framing,
                "framing_label": FRAMING_LABELS[framing],
                "n": len(subset),
                "preferred_solution_distribution": json.dumps(dict(Counter(r["preferred_solution"] for r in subset)), ensure_ascii=False),
                "ethical_preference_distribution": json.dumps(dict(Counter(r["ethical_preference_type"] for r in subset)), ensure_ascii=False),
                "response_genre_distribution": json.dumps(dict(Counter(r["response_genre"] for r in subset)), ensure_ascii=False),
                "review_count": sum(1 for r in subset if r["needs_second_coder_review"]),
            })

    with open(crosstab_csv, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0].keys()) if output_rows else [])
        if output_rows:
            writer.writeheader()
            writer.writerows(output_rows)

    lines = ["# Framing Cross-Tabs", ""]
    for model in MODEL_ORDER:
        lines.extend([f"## {model}", ""])
        for framing in FRAMING_ORDER:
            subset = grouped[(model, framing)]
            if not subset:
                continue
            solution_counts = dict(Counter(r["preferred_solution"] for r in subset))
            ethics_counts = dict(Counter(r["ethical_preference_type"] for r in subset))
            genre_counts = dict(Counter(r["response_genre"] for r in subset))
            chosen = max(subset, key=lambda r: (r["needs_second_coder_review"], len(r["evidence_span_yo"])))
            lines.extend([
                f"### {FRAMING_LABELS[framing]}",
                "",
                f"- Preferred solutions: `{solution_counts}`",
                f"- Ethical preference types: `{ethics_counts}`",
                f"- Response genres: `{genre_counts}`",
                f"- Review count: `{sum(1 for r in subset if r['needs_second_coder_review'])}`",
                "",
                "**Representative Yoruba evidence**",
                "",
                chosen["evidence_span_yo"],
                "",
                "**Why this framing matters**",
                "",
                chosen["coding_rationale"],
                "",
            ])
    crosstab_md.write_text("\n".join(lines), encoding="utf-8")
    return crosstab_csv, crosstab_md


def build_report(rows: list[dict], out_dir: Path) -> tuple[Path, Path, Path]:
    report_md = out_dir / "open_yoruba_coding_report.md"
    handout_html = out_dir / "open_yoruba_coding_report.html"

    lines = [
        "# Open Yoruba Content Coding Report",
        "",
        "## What was coded",
        "",
        "This report summarizes the Yoruba-first content coding pass performed directly on the raw unrestricted Yoruba sessions. The coding agent assigned labels for preferred solution, ethical preference type, response genre, deictic uptake quality, language stability, and review burden.",
        "",
        "## Model summaries",
        "",
    ]

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model_label"]].append(row)

    for model in MODEL_ORDER:
        subset = by_model[model]
        lines.extend([
            f"### {model}",
            "",
            f"- Records coded: `{len(subset)}`",
            f"- Preferred solution distribution: `{dict(Counter(r['preferred_solution'] for r in subset))}`",
            f"- Ethical preference distribution: `{dict(Counter(r['ethical_preference_type'] for r in subset))}`",
            f"- Response genre distribution: `{dict(Counter(r['response_genre'] for r in subset))}`",
            f"- Needs second coder review: `{sum(1 for r in subset if r['needs_second_coder_review'])}`",
            "",
        ])

    lines.extend([
        "## Key comparisons",
        "",
        "- GPT-4o is overwhelmingly expository and mixed in ethical preference under open Yoruba conditions.",
        "- Claude is the most action-codable model in the unrestricted condition and shows the widest spread across utilitarian, deontological, care, and procedural caution coding.",
        "- DeepSeek shows the strongest instability and the largest second-coder review burden, with non-trivial rates of translation_or_gloss and meta_commentary.",
        "",
        "## Representative examples",
        "",
    ])

    examples = []
    for model in MODEL_ORDER:
        subset = by_model[model]
        examples.append(max(subset, key=lambda r: (r["needs_second_coder_review"], len(r["evidence_span_yo"]))))

    for ex in examples:
        lines.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- preferred_solution: `{ex['preferred_solution']}`",
            f"- ethical_preference_type: `{ex['ethical_preference_type']}`",
            f"- response_genre: `{ex['response_genre']}`",
            f"- language_stability: `{ex['language_stability']}`",
            f"- needs_second_coder_review: `{ex['needs_second_coder_review']}`",
            "",
            "**Yoruba evidence**",
            "",
            ex['evidence_span_yo'],
            "",
            "**English support**",
            "",
            ex['evidence_span_en'],
            "",
            "**Coding rationale**",
            "",
            ex['coding_rationale'],
            "",
        ])

    report_md.write_text("\n".join(lines), encoding="utf-8")

    cards = []
    for model in MODEL_ORDER:
        subset = by_model[model]
        cards.append(
            f"<section class='card'><h3>{model}</h3><p><strong>Records:</strong> {len(subset)}</p><p><strong>Preferred solutions:</strong> {dict(Counter(r['preferred_solution'] for r in subset))}</p><p><strong>Genres:</strong> {dict(Counter(r['response_genre'] for r in subset))}</p><p><strong>Review burden:</strong> {sum(1 for r in subset if r['needs_second_coder_review'])}</p></section>"
        )
    examples_html = []
    for ex in examples:
        examples_html.append(
            f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}</h3><p class='meta'>Preferred solution: <strong>{ex['preferred_solution']}</strong> | Ethical preference: <strong>{ex['ethical_preference_type']}</strong> | Genre: <strong>{ex['response_genre']}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{ex['evidence_span_yo']}</p></div><div class='panel'><h4>English support</h4><p>{ex['evidence_span_en']}</p><h4>Coding rationale</h4><p>{ex['coding_rationale']}</p></div></div></article>"
        )

    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Open Yoruba Coding Report</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1100px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>Open Yoruba Content Coding Report</h1><p>This report summarizes the raw-session content coding pass over the unrestricted Yoruba corpus.</p><h2>Model Summary</h2><div class='cards'>{''.join(cards)}</div><h2>Representative Examples</h2>{''.join(examples_html)}</main></body></html>"""
    handout_html.write_text(html, encoding="utf-8")

    # pdf export
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    pdf_path = handout_html.with_suffix(".pdf")
    if edge.exists():
        temp_profile = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-open-coding-report")
        temp_profile.mkdir(parents=True, exist_ok=True)
        cmd = [str(edge), "--headless", "--disable-gpu", f"--user-data-dir={temp_profile}", f"--print-to-pdf={pdf_path}", handout_html.as_uri()]
        subprocess.run(cmd, capture_output=True, text=True)

    return report_md, handout_html, pdf_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_json(SOURCE_JSON)["records"]
    report_md, handout_html, pdf_path = build_report(rows, OUT_DIR)
    review_json, review_csv, review_md = write_review_subset(rows, OUT_DIR)
    crosstab_csv, crosstab_md = write_framing_crosstabs(rows, OUT_DIR)
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "source_json": str(SOURCE_JSON),
        "report_md": str(report_md),
        "handout_html": str(handout_html),
        "handout_pdf": str(pdf_path),
        "review_json": str(review_json),
        "review_csv": str(review_csv),
        "review_md": str(review_md),
        "crosstab_csv": str(crosstab_csv),
        "crosstab_md": str(crosstab_md),
    }
    with open(OUT_DIR / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(OUT_DIR)


if __name__ == "__main__":
    main()
