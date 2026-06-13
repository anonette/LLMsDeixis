#!/usr/bin/env python3
"""Build a focused aligned English-vs-Yoruba comparison for GPT-4o and Claude."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


MODULE = Path(__file__).resolve().parent
OUT_ROOT = MODULE / "outputs" / "openai_claude_aligned_comparison_20260608"
YORUBA_JSON = MODULE / "outputs" / "open_yoruba_coding_merged_20260608" / "open_yoruba_coded_content_merged.json"
ENGLISH_JSON = MODULE / "outputs" / "english_coded_content" / "english_open_comparison_coded_20260608_175242" / "coded_content.json"

MODEL_ORDER = ["GPT-4o", "Claude"]
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


def short(text: str, limit: int = 360) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def export_pdf(html_path: Path) -> Path | None:
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge.exists():
        return None
    pdf_path = html_path.with_suffix(".pdf")
    temp_profile = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-openai-claude")
    temp_profile.mkdir(parents=True, exist_ok=True)
    cmd = [str(edge), "--headless", "--disable-gpu", f"--user-data-dir={temp_profile}", f"--print-to-pdf={pdf_path}", html_path.as_uri()]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not pdf_path.exists():
        return None
    return pdf_path


def merge_rows() -> list[dict]:
    y_rows = load_json(YORUBA_JSON)["records"]
    e_rows = load_json(ENGLISH_JSON)["coded_records"]
    e_lookup = {(r["model_label"], r["dilemma_id"], r["framing_type"]): r for r in e_rows}
    merged = []
    for y in y_rows:
        if y["model_label"] not in MODEL_ORDER:
            continue
        key = (y["model_label"], y["dilemma_id"], y["framing_type"])
        e = e_lookup[key]
        merged.append(
            {
                **y,
                "english_preferred_solution": e["preferred_solution"],
                "english_ethical_preference_type": e["ethical_preference_type"],
                "english_response_genre": e["response_genre"],
                "english_deictic_uptake_quality": e["deictic_uptake_quality"],
                "english_evidence": e["evidence_span_en"],
                "english_rationale": e["coding_rationale"],
            }
        )
    return merged


def mismatch_score(row: dict) -> float:
    score = 0.0
    if row["preferred_solution"] != row["english_preferred_solution"]:
        score += 2.0
    if row["ethical_preference_type"] != row["english_ethical_preference_type"]:
        score += 1.5
    if row["response_genre"] != row["english_response_genre"]:
        score += 1.5
    if row["language_stability"] in {"mixed_language", "translation_mode", "corrupted_or_unusable"}:
        score += 1.0
    return score


def dominant(values) -> str:
    c = Counter(values)
    return c.most_common(1)[0][0] if c else "none"


def write_crosstabs(merged: list[dict]) -> tuple[Path, Path]:
    csv_path = OUT_ROOT / "framing_crosstabs.csv"
    md_path = OUT_ROOT / "framing_crosstabs.md"
    grouped = defaultdict(list)
    for row in merged:
        grouped[(row["model_label"], row["framing_type"])].append(row)
    out_rows = []
    lines = ["# GPT-4o and Claude: English vs Yoruba Framing Cross-Tabs", ""]
    for model in MODEL_ORDER:
        lines.extend([f"## {model}", ""])
        for framing in FRAMING_ORDER:
            subset = grouped[(model, framing)]
            if not subset:
                continue
            out_rows.append(
                {
                    "model": model,
                    "framing_type": framing,
                    "framing_label": FRAMING_LABELS[framing],
                    "n": len(subset),
                    "yoruba_preferred_solution": dominant(r["preferred_solution"] for r in subset),
                    "english_preferred_solution": dominant(r["english_preferred_solution"] for r in subset),
                    "yoruba_ethical_preference_type": dominant(r["ethical_preference_type"] for r in subset),
                    "english_ethical_preference_type": dominant(r["english_ethical_preference_type"] for r in subset),
                    "yoruba_response_genre": dominant(r["response_genre"] for r in subset),
                    "english_response_genre": dominant(r["english_response_genre"] for r in subset),
                    "severe_language_problems": sum(1 for r in subset if r["language_stability"] in {"mixed_language", "translation_mode", "corrupted_or_unusable"}),
                }
            )
            lines.extend(
                [
                    f"### {FRAMING_LABELS[framing]}",
                    "",
                    f"- Yoruba dominant preferred solution: `{dominant(r['preferred_solution'] for r in subset)}`",
                    f"- English dominant preferred solution: `{dominant(r['english_preferred_solution'] for r in subset)}`",
                    f"- Yoruba dominant ethical type: `{dominant(r['ethical_preference_type'] for r in subset)}`",
                    f"- English dominant ethical type: `{dominant(r['english_ethical_preference_type'] for r in subset)}`",
                    f"- Yoruba dominant genre: `{dominant(r['response_genre'] for r in subset)}`",
                    f"- English dominant genre: `{dominant(r['english_response_genre'] for r in subset)}`",
                    f"- Severe language problems: `{sum(1 for r in subset if r['language_stability'] in {'mixed_language', 'translation_mode', 'corrupted_or_unusable'})}/{len(subset)}`",
                    "",
                ]
            )
    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, md_path


def make_figures(merged: list[dict]) -> None:
    fig_dir = OUT_ROOT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    # preferred solution bars
    categories = ["supports_A", "supports_B", "conditional_or_mixed", "refuses_to_commit", "uncodable"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharey=True)
    for row_idx, model in enumerate(MODEL_ORDER):
        subset = [r for r in merged if r["model_label"] == model]
        for col_idx, (field, title) in enumerate([("preferred_solution", "Yoruba"), ("english_preferred_solution", "English")]):
            ax = axes[row_idx][col_idx]
            vals = [sum(1 for r in subset if r[field] == cat) for cat in categories]
            ax.bar(categories, vals)
            ax.tick_params(axis='x', rotation=35)
            ax.set_title(f"{model} / {title}")
            ax.set_ylabel("Count")
    fig.suptitle("Preferred Solution Distribution")
    fig.tight_layout()
    fig.savefig(fig_dir / "preferred_solution_distribution_openai_claude.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # genre bars
    categories = ["balanced_framework_exposition", "procedural_advice", "direct_verdict", "translation_or_gloss", "meta_commentary", "mixed"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharey=True)
    for row_idx, model in enumerate(MODEL_ORDER):
        subset = [r for r in merged if r["model_label"] == model]
        for col_idx, (field, title) in enumerate([("response_genre", "Yoruba"), ("english_response_genre", "English")]):
            ax = axes[row_idx][col_idx]
            vals = [sum(1 for r in subset if r[field] == cat) for cat in categories]
            ax.bar(categories, vals)
            ax.tick_params(axis='x', rotation=35)
            ax.set_title(f"{model} / {title}")
            ax.set_ylabel("Count")
    fig.suptitle("Response Genre Distribution")
    fig.tight_layout()
    fig.savefig(fig_dir / "response_genre_distribution_openai_claude.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # difference heatmap
    data = []
    for model in MODEL_ORDER:
        row = []
        for framing in FRAMING_ORDER:
            subset = [r for r in merged if r["model_label"] == model and r["framing_type"] == framing]
            row.append(mean(mismatch_score(r) for r in subset))
        data.append(row)
    fig, ax = plt.subplots(figsize=(10, 4.8))
    im = ax.imshow(data, aspect="auto")
    ax.set_xticks(range(len(FRAMING_ORDER)))
    ax.set_xticklabels([FRAMING_LABELS[f] for f in FRAMING_ORDER], rotation=35, ha="right")
    ax.set_yticks(range(len(MODEL_ORDER)))
    ax.set_yticklabels(MODEL_ORDER)
    ax.set_title("Average English-Yoruba Difference Score")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(fig_dir / "difference_heatmap_openai_claude.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_report(merged: list[dict]) -> tuple[Path, Path, Path]:
    report_md = OUT_ROOT / "report.md"
    html_path = OUT_ROOT / "handout.html"
    biggest = sorted(merged, key=mismatch_score, reverse=True)[:12]
    agreements = sorted([r for r in merged if r["preferred_solution"] == r["english_preferred_solution"]], key=lambda r: (r["ethical_preference_type"] == r["english_ethical_preference_type"], r["response_genre"] == r["english_response_genre"]), reverse=True)[:12]

    md = [
        "# GPT-4o and Claude Only: English vs Yoruba Deictic Framing Report",
        "",
        "## Main comparison claim",
        "",
        "For GPT-4o and Claude, unrestricted Yoruba is comparable to English at the level of deictic design and ethical content, but the strongest cross-linguistic differences often appear in response genre and directive force rather than in final preferred solution alone.",
        "",
        "## Language-problem rates",
        "",
    ]
    for model in MODEL_ORDER:
        subset = [r for r in merged if r["model_label"] == model]
        severe = sum(1 for r in subset if r["language_stability"] in {"mixed_language", "translation_mode", "corrupted_or_unusable"})
        md.append(f"- {model}: severe language problems `{severe}/{len(subset)}`")
    md.append("\n## Biggest differences first\n")
    for ex in biggest:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- Yoruba preferred solution: `{ex['preferred_solution']}`",
            f"- English preferred solution: `{ex['english_preferred_solution']}`",
            f"- Yoruba ethical type: `{ex['ethical_preference_type']}`",
            f"- English ethical type: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba response genre: `{ex['response_genre']}`",
            f"- English response genre: `{ex['english_response_genre']}`",
            f"- Language stability: `{ex['language_stability']}`",
            "",
            "**Yoruba evidence**",
            "",
            short(ex['evidence_span_yo'], 700),
            "",
            "**English evidence**",
            "",
            short(ex['english_evidence'], 700),
            "",
        ])
    md.append("## Then the strongest agreements\n")
    for ex in agreements:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- Shared preferred solution: `{ex['preferred_solution']}`",
            f"- Yoruba ethical type: `{ex['ethical_preference_type']}` | English ethical type: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba genre: `{ex['response_genre']}` | English genre: `{ex['english_response_genre']}`",
            "",
            "**Yoruba evidence**",
            "",
            short(ex['evidence_span_yo'], 700),
            "",
            "**English evidence**",
            "",
            short(ex['english_evidence'], 700),
            "",
        ])
    report_md.write_text("\n".join(md), encoding="utf-8")

    cards = []
    for model in MODEL_ORDER:
        subset = [r for r in merged if r["model_label"] == model]
        cards.append(f"<section class='card'><h3>{model}</h3><p><strong>Yoruba preferred:</strong> {dict(Counter(r['preferred_solution'] for r in subset))}</p><p><strong>English preferred:</strong> {dict(Counter(r['english_preferred_solution'] for r in subset))}</p><p><strong>Yoruba dominant genre:</strong> {dominant([r['response_genre'] for r in subset])}</p><p><strong>English dominant genre:</strong> {dominant([r['english_response_genre'] for r in subset])}</p></section>" )
    diff_examples = []
    for ex in biggest[:4]:
        diff_examples.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Yoruba: <strong>{ex['preferred_solution']}</strong> | English: <strong>{ex['english_preferred_solution']}</strong> | Yoruba genre: <strong>{ex['response_genre']}</strong> | English genre: <strong>{ex['english_response_genre']}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{short(ex['evidence_span_yo'], 600)}</p><p>{short(ex['coding_rationale'], 300)}</p></div><div class='panel'><h4>English evidence</h4><p>{short(ex['english_evidence'], 600)}</p><p>{short(ex['english_rationale'], 300)}</p></div></div></article>")
    agree_examples = []
    for ex in agreements[:4]:
        agree_examples.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Shared preferred solution: <strong>{ex['preferred_solution']}</strong> | Yoruba ethical type: <strong>{ex['ethical_preference_type']}</strong> | English ethical type: <strong>{ex['english_ethical_preference_type']}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{short(ex['evidence_span_yo'], 600)}</p></div><div class='panel'><h4>English evidence</h4><p>{short(ex['english_evidence'], 600)}</p></div></div></article>")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>OpenAI and Claude: English vs Yoruba</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1120px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}img{{width:100%;height:auto;display:block}}figure{{margin:18px 0;border:1px solid #d9d0c4;background:#fff;padding:12px}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>OpenAI and Claude Only: English vs Yoruba Deictic Framing</h1><p>This focused report uses the same coding scheme on English and Yoruba to show what deictic framing does across language for the two strongest and most stable model families.</p><h2>Model Summary</h2><div class='cards'>{''.join(cards)}</div><h2>Visualizations</h2><figure><img src='figures/preferred_solution_distribution_openai_claude.png'><figcaption>Preferred solution distributions for GPT-4o and Claude in Yoruba and English.</figcaption></figure><figure><img src='figures/response_genre_distribution_openai_claude.png'><figcaption>Response genre distributions for GPT-4o and Claude in Yoruba and English.</figcaption></figure><figure><img src='figures/difference_heatmap_openai_claude.png'><figcaption>Average difference score by deictic framing.</figcaption></figure><h2>Biggest Differences</h2>{''.join(diff_examples)}<h2>Strongest Agreements</h2>{''.join(agree_examples)}</main></body></html>"""
    html_path.write_text(html, encoding='utf-8')
    pdf_path = export_pdf(html_path)
    return report_md, html_path, pdf_path


def build_share_bundle() -> Path:
    bundle = OUT_ROOT / "share_bundle"
    bundle.mkdir(parents=True, exist_ok=True)
    files = {
        OUT_ROOT / "handout.pdf": bundle / "00_openai_claude_report.pdf",
        OUT_ROOT / "report.md": bundle / "01_openai_claude_report.md",
        OUT_ROOT / "english_framing_crosstabs.md": bundle / "02_english_framing_crosstabs.md",
        OUT_ROOT / "english_framing_crosstabs.csv": bundle / "03_english_framing_crosstabs.csv",
        OUT_ROOT / "figures" / "preferred_solution_distribution_openai_claude.png": bundle / "10_preferred_solution_distribution.png",
        OUT_ROOT / "figures" / "response_genre_distribution_openai_claude.png": bundle / "11_response_genre_distribution.png",
        OUT_ROOT / "figures" / "difference_heatmap_openai_claude.png": bundle / "12_difference_heatmap.png",
    }
    for src, dst in files.items():
        shutil.copy2(src, dst)
    return bundle


if __name__ == "__main__":
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    merged = merge_rows()
    english_csv, english_md = write_crosstabs(merged)
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
    with open(OUT_ROOT / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(OUT_ROOT)
