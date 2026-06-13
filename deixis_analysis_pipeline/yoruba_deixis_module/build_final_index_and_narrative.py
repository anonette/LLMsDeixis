#!/usr/bin/env python3
"""Build final master index and journal-style narrative report."""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


MODULE = Path(__file__).resolve().parent
OUT = MODULE / "outputs"
MASTER_DIR = OUT / "final_article_support_20260608"

YORUBA_MERGED = OUT / "open_yoruba_coding_merged_20260608" / "open_yoruba_coded_content_merged.json"
ENGLISH_CODED = OUT / "english_coded_content" / "english_open_comparison_coded_20260608_175242" / "coded_content.json"

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


def export_pdf(html_path: Path) -> Path | None:
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge.exists():
        return None
    pdf = html_path.with_suffix(".pdf")
    temp = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-final-narrative")
    temp.mkdir(parents=True, exist_ok=True)
    cmd = [str(edge), "--headless", "--disable-gpu", f"--user-data-dir={temp}", f"--print-to-pdf={pdf}", html_path.as_uri()]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not pdf.exists():
        return None
    return pdf


def dominant(counter: Counter) -> str:
    if not counter:
        return "none"
    return counter.most_common(1)[0][0]


def short(text: str, limit: int = 360) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def build_master_index() -> Path:
    path = MASTER_DIR / "MASTER_INDEX.md"
    text = f"""# Master Index

## Main report roots

- Full-scale comparison packages:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\full_scale_report_packages_20260608_140806`
- Open Yoruba coding merge:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_coding_merged_20260608`
- Open Yoruba vs English visual report:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_vs_english_visual_20260608`
- Trolley package:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\trolley_problem_share_20260529_182043`
- Deictic deep-dive handout:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\yoruba_english_deictic_deep_dive_handout_examples_20260531.pdf`

## Best summary PDFs

- Master merged full-scale PDF:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\full_scale_report_packages_20260608_140806\master_merged\handout.pdf`
- Open Yoruba vs English visual PDF:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_vs_english_visual_20260608\handout.pdf`
- Open Yoruba coding PDF:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_coding_merged_20260608\detailed_package_20260608\open_yoruba_coding_report.pdf`

## Key coding files

- Yoruba merged coding CSV:
  `{YORUBA_MERGED.with_suffix('.csv')}`
- Yoruba merged coding JSON:
  `{YORUBA_MERGED}`
- English aligned coding JSON:
  `{ENGLISH_CODED}`

## Adjudication files

- Review subset workbook:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_coding_merged_20260608\detailed_package_20260608\review_subset_adjudication_workbook.xlsx`
- Human-adjudicated template CSV:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_coding_merged_20260608\detailed_package_20260608\human_adjudicated_template.csv`

## Cross-tab files

- Yoruba framing cross-tabs:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_coding_merged_20260608\detailed_package_20260608\framing_crosstabs.md`
- English framing cross-tabs:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\open_yoruba_vs_english_visual_20260608\english_framing_crosstabs.md`

## This package

- Narrative report Markdown:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\final_article_support_20260608\narrative_report.md`
- Narrative report HTML:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\final_article_support_20260608\narrative_report.html`
- Narrative report PDF:
  `C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\final_article_support_20260608\narrative_report.pdf`
"""
    path.write_text(text, encoding="utf-8")
    return path


def build_narrative() -> tuple[Path, Path, Path]:
    y_rows = load_json(YORUBA_MERGED)["records"]
    e_rows = load_json(ENGLISH_CODED)["coded_records"]
    e_lookup = {(r["model_label"], r["dilemma_id"], r["framing_type"]): r for r in e_rows}
    merged = []
    for y in y_rows:
        key = (y["model_label"], y["dilemma_id"], y["framing_type"])
        e = e_lookup[key]
        merged.append({
            **y,
            "english_preferred_solution": e["preferred_solution"],
            "english_ethical_preference_type": e["ethical_preference_type"],
            "english_response_genre": e["response_genre"],
            "english_deictic_uptake_quality": e["deictic_uptake_quality"],
            "english_evidence": e["evidence_span_en"],
            "english_rationale": e["coding_rationale"],
        })

    by_model = defaultdict(list)
    by_model_framing = defaultdict(list)
    for r in merged:
        by_model[r["model_label"]].append(r)
        by_model_framing[(r["model_label"], r["framing_type"])].append(r)

    # language problems
    def severe_language_problem(r):
        return r["language_stability"] in {"mixed_language", "translation_mode", "corrupted_or_unusable"}

    # biggest differences and strongest agreements
    def diff_score(r):
        s = 0
        if r["preferred_solution"] != r["english_preferred_solution"]: s += 2
        if r["ethical_preference_type"] != r["english_ethical_preference_type"]: s += 1.5
        if r["response_genre"] != r["english_response_genre"]: s += 1.5
        if severe_language_problem(r): s += 1
        return s

    def agree_score(r):
        s = 0
        if r["preferred_solution"] == r["english_preferred_solution"]: s += 2
        if r["ethical_preference_type"] == r["english_ethical_preference_type"]: s += 1.5
        if r["response_genre"] == r["english_response_genre"]: s += 1.5
        if r["deictic_uptake_quality"] == r["english_deictic_uptake_quality"]: s += 1
        if not severe_language_problem(r): s += 0.5
        return s

    biggest = sorted(merged, key=diff_score, reverse=True)[:12]
    agreements = sorted([r for r in merged if r["preferred_solution"] == r["english_preferred_solution"]], key=agree_score, reverse=True)[:12]

    # per model / framing summaries
    table_lines = []
    for model in MODEL_ORDER:
        table_lines.append(f"### {model}\n")
        table_lines.append("| Framing | Yoruba dominant decision | English dominant decision | Yoruba dominant ethical type | English dominant ethical type | Yoruba genre | English genre | Severe language problems |")
        table_lines.append("|---|---|---|---|---|---|---|---|")
        for framing in FRAMING_ORDER:
            subset = by_model_framing[(model, framing)]
            if not subset:
                continue
            table_lines.append(
                f"| {FRAMING_LABELS[framing]} | {dominant(Counter(r['preferred_solution'] for r in subset))} | {dominant(Counter(r['english_preferred_solution'] for r in subset))} | {dominant(Counter(r['ethical_preference_type'] for r in subset))} | {dominant(Counter(r['english_ethical_preference_type'] for r in subset))} | {dominant(Counter(r['response_genre'] for r in subset))} | {dominant(Counter(r['english_response_genre'] for r in subset))} | {sum(1 for r in subset if severe_language_problem(r))}/{len(subset)} |"
            )
        table_lines.append("")

    md = []
    md.append("# Narrative Report: How Deictic Framing Changes Ethical Outcomes in English vs Yoruba\n")
    md.append("## Main claim\n")
    md.append("The most important contrast between open Yoruba and English is not only which option is preferred, but how deictic framing changes the **genre**, **directive force**, and **ethical architecture** of the response. Across models, English remains predominantly analytical and framework-expository. Open Yoruba frequently becomes more advisory, more procedural, or more unstable, with the exact pattern depending strongly on the model and the deictic frame.\n")
    md.append("## How much of the difference is just language trouble?\n")
    for model in MODEL_ORDER:
        subset = by_model[model]
        severe = sum(1 for r in subset if severe_language_problem(r))
        any_non_clean = sum(1 for r in subset if r['language_stability'] != 'clean_yoruba')
        md.append(f"- {model}: severe language problems `{severe}/{len(subset)}`, any non-clean Yoruba `{any_non_clean}/{len(subset)}`")
    md.append("\nInterpretation: not all differences are language problems. GPT-4o and Claude still differ from English even when language stability is clean. The strongest pure language-instability problem is concentrated in DeepSeek.\n")
    md.append("## Model-level comparison\n")
    md.append("### GPT-4o\n")
    md.append("GPT-4o open Yoruba is overwhelmingly coded as `balanced_framework_exposition` with `conditional_or_mixed` preferred solutions. Relative to English, it often preserves the same broad moral space but speaks more like procedural guidance than like a detached moral theorist.\n")
    md.append("### Claude\n")
    md.append("Claude open Yoruba is the most action-codable model. It distributes across `supports_A`, `supports_B`, `conditional_or_mixed`, and `refuses_to_commit`, and shows the richest spread of ethical preference types. This makes it the best model for studying genuine framing effects on preferred ethical orientation rather than only on discourse form.\n")
    md.append("### DeepSeek\n")
    md.append("DeepSeek open Yoruba is the most unstable. It still yields interpretable ethical material, but its outputs often drift into `translation_or_gloss` or `meta_commentary`, especially in cells with the highest cross-linguistic divergence. For DeepSeek, many apparent stance differences are partly downstream of response-mode instability.\n")
    md.append("## Deictic framing by model and language\n")
    md.extend(table_lines)
    md.append("## Biggest differences first\n")
    for ex in biggest:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- Yoruba preferred solution: `{ex['preferred_solution']}`",
            f"- English preferred solution: `{ex['english_preferred_solution']}`",
            f"- Yoruba ethical preference: `{ex['ethical_preference_type']}`",
            f"- English ethical preference: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba response genre: `{ex['response_genre']}`",
            f"- English response genre: `{ex['english_response_genre']}`",
            f"- Language stability: `{ex['language_stability']}`",
            "",
            "**Why it matters**",
            "",
            short(ex['coding_rationale'], 700),
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
            f"- Yoruba ethical preference: `{ex['ethical_preference_type']}`",
            f"- English ethical preference: `{ex['english_ethical_preference_type']}`",
            f"- Yoruba response genre: `{ex['response_genre']}`",
            f"- English response genre: `{ex['english_response_genre']}`",
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
    md.append("## Bottom line\n")
    md.append("Open Yoruba and English often remain ethically adjacent at a broad level, but they are not rhetorically equivalent. The biggest surprises are where Yoruba becomes more directive than English, and where DeepSeek abandons stable in-frame ethical response altogether. The strongest agreements are concentrated in framework-expository cells where both languages continue to analyze rather than decisively command. Cross-linguistic comparison is therefore strongest when carried out simultaneously across preferred solution, ethical preference type, response genre, deictic uptake, and language stability.\n")

    report_md = MASTER_DIR / "narrative_report.md"
    report_md.write_text("\n".join(md), encoding="utf-8")

    # html
    cards = []
    for model in MODEL_ORDER:
        subset = by_model[model]
        severe = sum(1 for r in subset if severe_language_problem(r))
        cards.append(f"<section class='card'><h3>{model}</h3><p><strong>Yoruba preferred:</strong> {dict(Counter(r['preferred_solution'] for r in subset))}</p><p><strong>English preferred:</strong> {dict(Counter(r['english_preferred_solution'] for r in subset))}</p><p><strong>Severe language problems:</strong> {severe}/{len(subset)}</p></section>")
    diff_html = []
    for ex in biggest[:4]:
        diff_html.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Yoruba: <strong>{ex['preferred_solution']}</strong> | English: <strong>{ex['english_preferred_solution']}</strong> | Yoruba genre: <strong>{ex['response_genre']}</strong> | English genre: <strong>{ex['english_response_genre']}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{short(ex['evidence_span_yo'], 600)}</p></div><div class='panel'><h4>English evidence</h4><p>{short(ex['english_evidence'], 600)}</p></div></div></article>")
    agree_html = []
    for ex in agreements[:4]:
        agree_html.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS[ex['framing_type']]}</h3><p class='meta'>Shared preferred solution: <strong>{ex['preferred_solution']}</strong> | Yoruba ethical type: <strong>{ex['ethical_preference_type']}</strong> | English ethical type: <strong>{ex['english_ethical_preference_type']}</strong></p><div class='twocol'><div class='panel'><h4>Yoruba evidence</h4><p>{short(ex['evidence_span_yo'], 600)}</p></div><div class='panel'><h4>English evidence</h4><p>{short(ex['english_evidence'], 600)}</p></div></div></article>")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Narrative Report</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1120px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}img{{width:100%;height:auto;display:block}}figure{{margin:18px 0;border:1px solid #d9d0c4;background:#fff;padding:12px}}table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{border:1px solid #d9d0c4;padding:8px 10px;text-align:left;vertical-align:top}}th{{background:#f1ebe1}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>How Deictic Framing Changes Ethical Outcomes in English vs Yoruba</h1><p>This report compares the unrestricted Yoruba corpus and the published English baseline using aligned coding layers for preferred solution, ethical preference type, response genre, and deictic uptake. It begins with the biggest differences, then turns to the strongest agreements.</p><h2>Model Summary</h2><div class='cards'>{''.join(cards)}</div><h2>Visual Overview</h2><figure><img src='../open_yoruba_vs_english_visual_20260608/figures/preferred_solution_distribution.png'><figcaption>Preferred solution distribution in Open Yoruba versus English baseline.</figcaption></figure><figure><img src='../open_yoruba_vs_english_visual_20260608/figures/response_genre_distribution.png'><figcaption>Response genre distribution in Open Yoruba versus English baseline.</figcaption></figure><figure><img src='../open_yoruba_vs_english_visual_20260608/figures/difference_heatmap.png'><figcaption>Average cross-linguistic difference score by model and framing.</figcaption></figure><h2>Biggest Differences</h2>{''.join(diff_html)}<h2>Then the Strongest Agreements</h2>{''.join(agree_html)}<h2>Reference Files</h2><ul><li><a href='../open_yoruba_vs_english_visual_20260608/english_framing_crosstabs.md'>English framing cross-tabs</a></li><li><a href='../open_yoruba_coding_merged_20260608/detailed_package_20260608/framing_crosstabs.md'>Yoruba framing cross-tabs</a></li><li><a href='../open_yoruba_coding_merged_20260608/detailed_package_20260608/review_subset_adjudication_workbook.xlsx'>Adjudication workbook</a></li></ul></main></body></html>"""
    html_path = MASTER_DIR / "narrative_report.html"
    html_path.write_text(html, encoding="utf-8")
    pdf_path = export_pdf(html_path)
    return report_md, html_path, pdf_path


def main() -> None:
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    idx = build_master_index()
    report_md, html_path, pdf_path = build_narrative()
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "master_index": str(idx),
        "narrative_md": str(report_md),
        "narrative_html": str(html_path),
        "narrative_pdf": str(pdf_path),
    }
    with open(MASTER_DIR / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(MASTER_DIR)


if __name__ == "__main__":
    main()
