#!/usr/bin/env python3
"""Build English-vs-open-Yoruba cross-tabs, visual report, and share bundle."""

from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


MODULE = Path(__file__).resolve().parent
YORUBA_JSON = MODULE / "outputs" / "open_yoruba_coding_merged_20260608" / "open_yoruba_coded_content_merged.json"
ENGLISH_DIR = MODULE / "outputs" / "english_coded_content" / "english_open_comparison_coded_20260608_175242"
ENGLISH_JSON = ENGLISH_DIR / "coded_content.json"
OUT_DIR = MODULE / "outputs" / "open_yoruba_vs_english_visual_20260608"

MODEL_ORDER = ["GPT-4o", "Claude", "DeepSeek"]
FRAMING_ORDER = ["impersonal", "second_person", "first_person", "first_person_plural", "reflexive", "dialogic", "spatial", "temporal", "cosmological"]
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


def short(text: str, limit: int = 420) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def export_pdf(html_path: Path) -> Path | None:
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge.exists():
        return None
    pdf = html_path.with_suffix(".pdf")
    temp = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-open-yoruba-vs-english")
    temp.mkdir(parents=True, exist_ok=True)
    cmd = [str(edge), "--headless", "--disable-gpu", f"--user-data-dir={temp}", f"--print-to-pdf={pdf}", html_path.as_uri()]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not pdf.exists():
        return None
    return pdf


def merge_rows() -> list[dict]:
    y_rows = load_json(YORUBA_JSON)["records"]
    e_rows = load_json(ENGLISH_JSON)["coded_records"]
    e_lookup = {(r["model_label"], r["dilemma_id"], r["framing_type"]): r for r in e_rows}
    merged = []
    for y in y_rows:
        key = (y["model_label"], y["dilemma_id"], y["framing_type"])
        e = e_lookup[key]
        merged.append({
            "model_label": y["model_label"],
            "dilemma_id": y["dilemma_id"],
            "framing_type": y["framing_type"],
            "yoruba_preferred_solution": y["preferred_solution"],
            "english_preferred_solution": e["preferred_solution"],
            "yoruba_ethical_preference_type": y["ethical_preference_type"],
            "english_ethical_preference_type": e["ethical_preference_type"],
            "yoruba_response_genre": y["response_genre"],
            "english_response_genre": e["response_genre"],
            "yoruba_deictic_uptake_quality": y["deictic_uptake_quality"],
            "english_deictic_uptake_quality": e["deictic_uptake_quality"],
            "yoruba_language_stability": y["language_stability"],
            "yoruba_needs_review": y["needs_second_coder_review"],
            "yoruba_evidence": y["evidence_span_yo"],
            "english_evidence": e["evidence_span_en"],
            "yoruba_rationale": y["coding_rationale"],
            "english_rationale": e["coding_rationale"],
        })
    return merged


def mismatch_score(row: dict) -> float:
    score = 0.0
    if row["yoruba_preferred_solution"] != row["english_preferred_solution"]:
        score += 2.0
    if row["yoruba_ethical_preference_type"] != row["english_ethical_preference_type"]:
        score += 1.5
    if row["yoruba_response_genre"] != row["english_response_genre"]:
        score += 1.5
    if row["yoruba_language_stability"] not in {"clean_yoruba", "yoruba_with_english_markers"}:
        score += 1.0
    if row["yoruba_needs_review"]:
        score += 0.5
    return score


def agreement_score(row: dict) -> float:
    score = 0.0
    if row["yoruba_preferred_solution"] == row["english_preferred_solution"]:
        score += 2.0
    if row["yoruba_ethical_preference_type"] == row["english_ethical_preference_type"]:
        score += 1.5
    if row["yoruba_response_genre"] == row["english_response_genre"]:
        score += 1.5
    if row["yoruba_deictic_uptake_quality"] == row["english_deictic_uptake_quality"]:
        score += 1.0
    if not row["yoruba_needs_review"]:
        score += 0.5
    return score


def write_english_crosstabs(merged: list[dict]) -> tuple[Path, Path]:
    csv_path = OUT_DIR / "english_framing_crosstabs.csv"
    md_path = OUT_DIR / "english_framing_crosstabs.md"
    grouped = defaultdict(list)
    for row in merged:
        grouped[(row["model_label"], row["framing_type"])].append(row)
    out_rows = []
    lines = ["# English-side Matching Cross-Tabs", "", "These cross-tabs use the aligned English coding produced for direct comparison with the raw-Yoruba coding layer.", ""]
    for model in MODEL_ORDER:
        lines.extend([f"## {model}", ""])
        for framing in FRAMING_ORDER:
            subset = grouped[(model, framing)]
            if not subset:
                continue
            p = dict(Counter(r["english_preferred_solution"] for r in subset))
            e = dict(Counter(r["english_ethical_preference_type"] for r in subset))
            g = dict(Counter(r["english_response_genre"] for r in subset))
            ex = max(subset, key=lambda r: len(r["english_evidence"]))
            out_rows.append({
                "model": model,
                "framing_type": framing,
                "framing_label": FRAMING_LABELS[framing],
                "n": len(subset),
                "preferred_solution_distribution": json.dumps(p, ensure_ascii=False),
                "ethical_preference_distribution": json.dumps(e, ensure_ascii=False),
                "response_genre_distribution": json.dumps(g, ensure_ascii=False),
            })
            lines.extend([
                f"### {FRAMING_LABELS[framing]}",
                "",
                f"- Preferred solutions: `{p}`",
                f"- Ethical preference types: `{e}`",
                f"- Response genres: `{g}`",
                "",
                "**Representative English evidence**",
                "",
                ex["english_evidence"],
                "",
                "**Coding rationale**",
                "",
                ex["english_rationale"],
                "",
            ])
    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, md_path


def make_figures(merged: list[dict]) -> None:
    figs = OUT_DIR / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    # preferred solution comparison by model
    categories = ["supports_A", "supports_B", "conditional_or_mixed", "refuses_to_commit", "uncodable"]
    models = MODEL_ORDER
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for idx, side in enumerate([("yoruba_preferred_solution", "Open Yoruba"), ("english_preferred_solution", "Published English")]):
        kind, title = side
        ax = axes[idx]
        bottom = [0] * len(models)
        for cat in categories:
            vals = [sum(1 for r in merged if r["model_label"] == m and r[kind] == cat) for m in models]
            ax.bar(models, vals, bottom=bottom, label=cat if idx == 0 else None)
            bottom = [b + v for b, v in zip(bottom, vals)]
        ax.set_title(title)
        ax.set_ylabel("Count across 54 cells")
    axes[0].legend(fontsize=8)
    fig.suptitle("Preferred Solution Distribution: Open Yoruba vs English")
    fig.tight_layout()
    fig.savefig(figs / "preferred_solution_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # genre comparison by model
    categories = ["balanced_framework_exposition", "procedural_advice", "direct_verdict", "translation_or_gloss", "meta_commentary", "mixed"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for idx, side in enumerate([("yoruba_response_genre", "Open Yoruba"), ("english_response_genre", "Published English")]):
        kind, title = side
        ax = axes[idx]
        bottom = [0] * len(models)
        for cat in categories:
            vals = [sum(1 for r in merged if r["model_label"] == m and r[kind] == cat) for m in models]
            ax.bar(models, vals, bottom=bottom, label=cat if idx == 0 else None)
            bottom = [b + v for b, v in zip(bottom, vals)]
        ax.set_title(title)
        ax.set_ylabel("Count across 54 cells")
    axes[0].legend(fontsize=8)
    fig.suptitle("Response Genre Distribution: Open Yoruba vs English")
    fig.tight_layout()
    fig.savefig(figs / "response_genre_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # mismatch heatmap
    data = []
    for model in models:
        row = []
        for framing in FRAMING_ORDER:
            subset = [r for r in merged if r["model_label"] == model and r["framing_type"] == framing]
            row.append(mean(mismatch_score(r) for r in subset))
        data.append(row)
    fig, ax = plt.subplots(figsize=(10, 4.8))
    im = ax.imshow(data, aspect="auto")
    ax.set_xticks(range(len(FRAMING_ORDER)))
    ax.set_xticklabels([FRAMING_LABELS[f] for f in FRAMING_ORDER], rotation=35, ha="right")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_title("Average Yoruba-English Difference Score by Model and Framing")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(figs / "difference_heatmap.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_report(merged: list[dict]) -> tuple[Path, Path, Path]:
    report_md = OUT_DIR / "report.md"
    html_path = OUT_DIR / "handout.html"
    biggest = sorted(merged, key=mismatch_score, reverse=True)[:9]
    agreements = sorted([r for r in merged if r["yoruba_preferred_solution"] == r["english_preferred_solution"]], key=agreement_score, reverse=True)[:9]

    md = [
        "# Open Yoruba vs English: Visual Comparison Report",
        "",
        "## What this report does",
        "",
        "This report compares the unrestricted Yoruba corpus to the published English baseline using aligned coding layers for preferred solution, ethical preference type, response genre, and deictic uptake. It starts with the largest divergences, then turns to the clearest cross-linguistic agreements.",
        "",
        "## Biggest differences",
        "",
    ]
    for ex in biggest:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- Yoruba preferred solution: `{ex['yoruba_preferred_solution']}`",
            f"- English preferred solution: `{ex['english_preferred_solution']}`",
            f"- Yoruba ethical type: `{ex['yoruba_ethical_preference_type']}`",
            f"- English ethical type: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba genre: `{ex['yoruba_response_genre']}`",
            f"- English genre: `{ex['english_response_genre']}`",
            f"- Difference score: `{mismatch_score(ex):.1f}`",
            "",
            "**Yoruba evidence**",
            "",
            short(ex['yoruba_evidence'], 700),
            "",
            "**English evidence**",
            "",
            short(ex['english_evidence'], 700),
            "",
            "**Interpretation**",
            "",
            f"Yoruba coding rationale: {ex['yoruba_rationale']} English coding rationale: {ex['english_rationale']}",
            "",
        ])
    md.extend(["## Strongest agreements", ""])
    for ex in agreements:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- Shared preferred solution: `{ex['yoruba_preferred_solution']}`",
            f"- Yoruba ethical type: `{ex['yoruba_ethical_preference_type']}` | English ethical type: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba genre: `{ex['yoruba_response_genre']}` | English genre: `{ex['english_response_genre']}`",
            f"- Agreement score: `{agreement_score(ex):.1f}`",
            "",
            "**Yoruba evidence**",
            "",
            short(ex['yoruba_evidence'], 700),
            "",
            "**English evidence**",
            "",
            short(ex['english_evidence'], 700),
            "",
        ])
    report_md.write_text("\n".join(md), encoding="utf-8")

    top_cards = []
    by_model = defaultdict(list)
    for r in merged:
        by_model[r['model_label']].append(r)
    for model in MODEL_ORDER:
        subset = by_model[model]
        top_cards.append(f"<section class='card'><h3>{model}</h3><p><strong>Yoruba preferred solutions:</strong> {dict(Counter(r['yoruba_preferred_solution'] for r in subset))}</p><p><strong>English preferred solutions:</strong> {dict(Counter(r['english_preferred_solution'] for r in subset))}</p><p><strong>Avg difference score:</strong> {mean(mismatch_score(r) for r in subset):.2f}</p></section>")
    diff_examples = []
    for ex in biggest[:3]:
        diff_examples.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Yoruba: <strong>{ex['yoruba_preferred_solution']}</strong> | English: <strong>{ex['english_preferred_solution']}</strong> | Difference score: <strong>{mismatch_score(ex):.1f}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{ex['yoruba_evidence']}</p><h4>Yoruba rationale</h4><p>{ex['yoruba_rationale']}</p></div><div class='panel'><h4>English evidence</h4><p>{ex['english_evidence']}</p><h4>English rationale</h4><p>{ex['english_rationale']}</p></div></div></article>")
    agreement_examples = []
    for ex in agreements[:3]:
        agreement_examples.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Shared preferred solution: <strong>{ex['yoruba_preferred_solution']}</strong> | Agreement score: <strong>{agreement_score(ex):.1f}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{ex['yoruba_evidence']}</p></div><div class='panel'><h4>English evidence</h4><p>{ex['english_evidence']}</p></div></div></article>")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Open Yoruba vs English Visual Report</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1100px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}img{{width:100%;height:auto;display:block}}figure{{margin:18px 0;border:1px solid #d9d0c4;background:#fff;padding:12px}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>Open Yoruba vs English: How Deictic Framing Changes Ethical Outcomes</h1><p>This visual report compares the unrestricted Yoruba corpus to the published English baseline across models, dilemmas, and deictic framings. It begins with the biggest divergences, then turns to the strongest agreements.</p><h2>Model Summary</h2><div class='cards'>{''.join(top_cards)}</div><h2>Visualizations</h2><figure><img src='figures/preferred_solution_distribution.png'><figcaption>Preferred solution distribution in Open Yoruba versus English baseline.</figcaption></figure><figure><img src='figures/response_genre_distribution.png'><figcaption>Response genre distribution in Open Yoruba versus English baseline.</figcaption></figure><figure><img src='figures/difference_heatmap.png'><figcaption>Average cross-linguistic difference score by model and framing. Higher values mark bigger gaps in outcome, ethical type, or genre.</figcaption></figure><h2>Biggest Differences</h2>{''.join(diff_examples)}<h2>Strongest Agreements</h2>{''.join(agreement_examples)}<h2>Supporting Files</h2><ul><li><a href='english_framing_crosstabs.md'>English-side matching cross-tabs</a></li><li><a href='../open_yoruba_coding_merged_20260608/detailed_package_20260608/framing_crosstabs.md'>Open Yoruba framing cross-tabs</a></li><li><a href='../open_yoruba_coding_merged_20260608/detailed_package_20260608/review_subset.csv'>Second-coder review subset</a></li><li><a href='../open_yoruba_coding_merged_20260608/detailed_package_20260608/review_subset_adjudication_workbook.xlsx'>Adjudication workbook</a></li></ul></main></body></html>"""
    html_path.write_text(html, encoding='utf-8')
    pdf_path = export_pdf(html_path)
    return report_md, html_path, pdf_path


def build_share_bundle() -> Path:
    bundle = OUT_DIR / "share_bundle"
    bundle.mkdir(parents=True, exist_ok=True)
    mappings = {
        OUT_DIR / "handout.pdf": bundle / "00_visual_report.pdf",
        OUT_DIR / "report.md": bundle / "01_visual_report.md",
        OUT_DIR / "english_framing_crosstabs.md": bundle / "02_english_framing_crosstabs.md",
        OUT_DIR / "english_framing_crosstabs.csv": bundle / "03_english_framing_crosstabs.csv",
        OUT_DIR / "figures" / "preferred_solution_distribution.png": bundle / "10_preferred_solution_distribution.png",
        OUT_DIR / "figures" / "response_genre_distribution.png": bundle / "11_response_genre_distribution.png",
        OUT_DIR / "figures" / "difference_heatmap.png": bundle / "12_difference_heatmap.png",
        MODULE / "outputs" / "open_yoruba_coding_merged_20260608" / "detailed_package_20260608" / "review_subset_adjudication_workbook.xlsx": bundle / "20_review_subset_workbook.xlsx",
        MODULE / "outputs" / "open_yoruba_coding_merged_20260608" / "detailed_package_20260608" / "review_subset.csv": bundle / "21_review_subset.csv",
        MODULE / "outputs" / "open_yoruba_coding_merged_20260608" / "detailed_package_20260608" / "english_yoruba_coding_alignment.md": bundle / "22_english_yoruba_coding_alignment.md",
    }
    for src, dst in mappings.items():
        shutil.copy2(src, dst)
    readme = bundle / "README.md"
    readme.write_text(
        "# Share Bundle\n\n"
        "Recommended order:\n\n"
        "1. `00_visual_report.pdf`\n"
        "2. `10_preferred_solution_distribution.png`\n"
        "3. `11_response_genre_distribution.png`\n"
        "4. `12_difference_heatmap.png`\n"
        "5. `20_review_subset_workbook.xlsx`\n",
        encoding="utf-8",
    )
    return bundle


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    merged = merge_rows()
    english_csv, english_md = write_english_crosstabs(merged)
    make_figures(merged)
    report_md, html_path, pdf_path = build_report(merged)
    bundle = build_share_bundle()
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "report_md": str(report_md),
        "handout_html": str(html_path),
        "handout_pdf": str(pdf_path),
        "english_crosstab_csv": str(english_csv),
        "english_crosstab_md": str(english_md),
        "share_bundle": str(bundle),
    }
    with open(OUT_DIR / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(OUT_DIR)
