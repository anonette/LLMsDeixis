#!/usr/bin/env python3
"""Build detailed full-scale report packages for Yoruba and English comparisons."""

from __future__ import annotations

import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


MODULE = Path(__file__).resolve().parent
OUTPUTS = MODULE / "outputs"
COMPARISONS = OUTPUTS / "comparisons"

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
    "second_person": "2nd Person",
    "first_person": "1st Person",
    "first_person_plural": "1st Plural",
    "reflexive": "Reflexive",
    "dialogic": "Dialogic",
    "spatial": "Spatial",
    "temporal": "Temporal",
    "cosmological": "Cosmological",
}

MODEL_ORDER = ["GPT-4o", "Claude", "DeepSeek"]

CONSTRAINED_DIRS = {
    "GPT-4o": COMPARISONS / "gpt-4o_vs_published_english_20260608_133058",
    "Claude": COMPARISONS / "claude_35_sonnet_vs_published_english_20260608_133058",
    "DeepSeek": COMPARISONS / "deepseek_vs_published_english_20260608_133058",
}

CONTROL_DIRS = {
    "GPT-4o": COMPARISONS / "yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_vs_published_english_20260608_135541",
    "Claude": COMPARISONS / "yoruba_control_claude_20260608_122738_bilingual_20260608_134631_vs_published_english_20260608_135541",
    "DeepSeek": COMPARISONS / "yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_vs_published_english_20260608_135541",
}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def classify_decision(text: str) -> str:
    lowered = normalize_space(text).lower()
    lead = lowered[:240]
    lead_block = lowered.split(". ")[0][:240]
    lead_patterns_positive = [
        r"\bi would redirect\b", r"\bi will redirect\b", r"\bi would divert\b", r"\bi will divert\b",
        r"\bi choose to divert\b", r"\bi choose to redirect\b", r"\bi would choose to divert\b",
        r"\bmy decision: redirect\b", r"\bmy decision: divert\b", r"\bdecision: redirect\b",
        r"\bdecision: divert\b", r"\bredirect the train\b", r"\bredirect the trolley\b",
        r"\bdivert the train\b", r"\bdivert the trolley\b", r"\bpull the lever\b",
    ]
    lead_patterns_negative = [
        r"\bi would not redirect\b", r"\bi will not redirect\b", r"\bi would not divert\b", r"\bi will not divert\b",
        r"\bi choose not to divert\b", r"\brefrain from redirecting\b", r"\bdo not alter the train's course\b",
        r"\bdo not divert\b", r"\bdo not pull\b", r"\bmy decision: do not\b", r"\bnot to divert\b",
    ]
    ambivalent = [
        "no definitive", "no single clear-cut", "no easy answer", "cannot decide for you", "i cannot definitively tell you",
        "depends on your ethical", "each person must decide", "there is no entirely right", "no universally accepted",
        "reasonable people can disagree", "rather than advocate", "refrain from advocating", "explore this dilemma",
        "key considerations", "thought experiment", "structured approach", "here are some perspectives", "what factors do you think",
    ]

    lead_negative = any(re.search(p, lead_block) for p in lead_patterns_negative) or any(re.search(p, lead[:140]) for p in lead_patterns_negative)
    if lead_negative:
        return "no_divert"

    lead_positive = any(re.search(p, lead_block) for p in lead_patterns_positive) or any(re.search(p, lead) for p in lead_patterns_positive)
    if lead_positive:
        return "divert"

    if any(token in lowered for token in ambivalent):
        return "ambivalent"
    return "unclear"


def load_condition_records(source_dirs: dict[str, Path], label: str) -> list[dict]:
    rows = []
    for model_label, directory in source_dirs.items():
        payload = load_json(directory / "paired_comparison.json")
        for row in payload["paired_records"]:
            rows.append(
                {
                    "condition": label,
                    "model_label": model_label,
                    "dilemma_id": row["dilemma_id"],
                    "framing_type": row["framing_type"],
                    "prompt_yo": row["prompt_yo"],
                    "prompt_en_reference": row.get("prompt_en_reference", ""),
                    "response_yo": row["response_yo"],
                    "response_en_academic": row["response_en_academic"],
                    "baseline_response_en": row["baseline_response_en"],
                    "yoruba_response_length": row["yoruba_response_length"],
                    "baseline_response_length": row["baseline_response_length"],
                    "decision_yoruba": classify_decision(row["response_en_academic"]),
                    "decision_english": classify_decision(row["baseline_response_en"]),
                    "source_session": row["yoruba_source_session"],
                    "published_english_session": row["published_english_session"],
                }
            )
    return rows


def short_excerpt(text: str, limit: int = 320) -> str:
    text = normalize_space(text)
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def get_examples(records: list[dict], condition_label: str) -> list[dict]:
    examples = []
    by_model = defaultdict(list)
    for row in records:
        if row["condition"] == condition_label:
            by_model[row["model_label"]].append(row)
    for model in MODEL_ORDER:
        subset = by_model[model]
        if not subset:
            continue
        opposite = [r for r in subset if r["decision_yoruba"] != r["decision_english"] and not (r["decision_yoruba"] == "unclear" and r["decision_english"] == "unclear")]
        chosen = max(opposite or subset, key=lambda r: abs(r["yoruba_response_length"] - r["baseline_response_length"]))
        examples.append(chosen)
    return examples


def make_three_way_records(constrained: list[dict], control: list[dict]) -> list[dict]:
    c_lookup = {(r["model_label"], r["dilemma_id"], r["framing_type"]): r for r in constrained}
    u_lookup = {(r["model_label"], r["dilemma_id"], r["framing_type"]): r for r in control}
    rows = []
    for key in sorted(c_lookup):
        if key not in u_lookup:
            continue
        c = c_lookup[key]
        u = u_lookup[key]
        rows.append(
            {
                "model_label": c["model_label"],
                "dilemma_id": c["dilemma_id"],
                "framing_type": c["framing_type"],
                "prompt_yo": c["prompt_yo"],
                "prompt_en_reference": c["prompt_en_reference"],
                "constrained_response_yo": c["response_yo"],
                "constrained_response_en": c["response_en_academic"],
                "control_response_yo": u["response_yo"],
                "control_response_en": u["response_en_academic"],
                "english_response_en": c["baseline_response_en"],
                "constrained_length": c["yoruba_response_length"],
                "control_length": u["yoruba_response_length"],
                "english_length": c["baseline_response_length"],
                "constrained_decision": c["decision_yoruba"],
                "control_decision": u["decision_yoruba"],
                "english_decision": c["decision_english"],
            }
        )
    return rows


def export_pdf(html_path: Path) -> Path | None:
    edge_path = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge_path.exists():
        return None
    pdf_path = html_path.with_suffix(".pdf")
    tmp_profile = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-fullscale")
    tmp_profile.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(edge_path), "--headless", "--disable-gpu", f"--user-data-dir={tmp_profile}",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not pdf_path.exists():
        return None
    return pdf_path


def render_condition_graphs(records: list[dict], out_dir: Path, title_prefix: str, field_label: str) -> None:
    figs = out_dir / "figures"
    figs.mkdir(parents=True, exist_ok=True)

    models = MODEL_ORDER
    yoruba_means = []
    english_means = []
    for model in models:
        subset = [r for r in records if r["model_label"] == model]
        yoruba_means.append(mean(r["yoruba_response_length"] for r in subset))
        english_means.append(mean(r["baseline_response_length"] for r in subset))

    x = range(len(models))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar([i - width/2 for i in x], yoruba_means, width=width, label=field_label, color="#1f6f8b")
    ax.bar([i + width/2 for i in x], english_means, width=width, label="Published English baseline", color="#b86a3b")
    ax.set_xticks(list(x))
    ax.set_xticklabels(models)
    ax.set_ylabel("Mean response length")
    ax.set_title(f"{title_prefix}: Mean Response Length")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs / "mean_response_length_by_model.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    categories = ["divert", "no_divert", "ambivalent", "unclear"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax_idx, kind in enumerate(["decision_yoruba", "decision_english"]):
        ax = axes[ax_idx]
        bottom = [0] * len(models)
        for cat in categories:
            vals = []
            for model in models:
                subset = [r for r in records if r["model_label"] == model]
                vals.append(sum(1 for r in subset if r[kind] == cat))
            ax.bar(models, vals, bottom=bottom, label=cat if ax_idx == 0 else None)
            bottom = [b + v for b, v in zip(bottom, vals)]
        ax.set_title(field_label if kind == "decision_yoruba" else "Published English baseline")
        ax.set_ylabel("Count across 54 cells")
    axes[0].legend()
    fig.suptitle(f"{title_prefix}: Preferred-Solution Distribution")
    fig.tight_layout()
    fig.savefig(figs / "decision_distribution_by_model.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_three_way_graphs(records: list[dict], out_dir: Path) -> None:
    figs = out_dir / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    models = MODEL_ORDER
    constrained = []
    control = []
    english = []
    for model in models:
        subset = [r for r in records if r["model_label"] == model]
        constrained.append(mean(r["constrained_length"] for r in subset))
        control.append(mean(r["control_length"] for r in subset))
        english.append(mean(r["english_length"] for r in subset))
    x = range(len(models))
    width = 0.25
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar([i-width for i in x], constrained, width=width, label="Constrained Yoruba")
    ax.bar(list(x), control, width=width, label="Unrestricted Yoruba control")
    ax.bar([i+width for i in x], english, width=width, label="Published English baseline")
    ax.set_xticks(list(x))
    ax.set_xticklabels(models)
    ax.set_ylabel("Mean response length")
    ax.set_title("Three-way Mean Response Length")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs / "three_way_mean_length.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_condition_package(records: list[dict], label: str, out_root: Path, field_label: str) -> Path:
    out_root.mkdir(parents=True, exist_ok=True)
    render_condition_graphs(records, out_root, label, field_label)
    examples = get_examples(records, label.lower().split()[0]) if False else get_examples(records, records[0]["condition"])
    # build markdown
    md = []
    md.append(f"# {label}\n")
    md.append(f"Source condition: `{field_label}`\n")
    md.append("## Summary Metrics\n")
    for model in MODEL_ORDER:
        subset = [r for r in records if r["model_label"] == model]
        y_mean = mean(r["yoruba_response_length"] for r in subset)
        e_mean = mean(r["baseline_response_length"] for r in subset)
        counts = Counter(r["decision_yoruba"] for r in subset)
        md.append(f"- {model}: mean {field_label.lower()} length `{y_mean:.1f}`, mean English baseline length `{e_mean:.1f}`, decisions {dict(counts)}")
    md.append("\n## Representative Examples\n")
    for ex in get_examples(records, records[0]["condition"]):
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- {field_label} decision: `{ex['decision_yoruba']}`",
            f"- English baseline decision: `{ex['decision_english']}`",
            "",
            f"**Yoruba ({field_label})**",
            "",
            short_excerpt(ex['response_yo'], 700),
            "",
            "**Academic English translation**",
            "",
            short_excerpt(ex['response_en_academic'], 700),
            "",
            "**Published English baseline**",
            "",
            short_excerpt(ex['baseline_response_en'], 900),
            "",
        ])
    report_md = out_root / "report.md"
    report_md.write_text("\n".join(md), encoding="utf-8")

    # handout html
    cards = []
    for model in MODEL_ORDER:
        subset = [r for r in records if r["model_label"] == model]
        counts = Counter(r["decision_yoruba"] for r in subset)
        cards.append(f"<section class='card'><h3>{model}</h3><p><strong>Mean {field_label.lower()} length:</strong> {mean(r['yoruba_response_length'] for r in subset):.1f}</p><p><strong>Mean English length:</strong> {mean(r['baseline_response_length'] for r in subset):.1f}</p><p><strong>Decision distribution:</strong> {dict(counts)}</p></section>")
    examples_html = []
    for ex in get_examples(records, records[0]["condition"]):
        examples_html.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS.get(ex['framing_type'], ex['framing_type'])}</h3><p class='meta'>{field_label} decision: <strong>{ex['decision_yoruba']}</strong> | English baseline: <strong>{ex['decision_english']}</strong></p><div class='twocol'><div class='panel'><h4>{field_label}</h4><p>{ex['response_yo']}</p><h4>Translation</h4><p>{ex['response_en_academic']}</p></div><div class='panel'><h4>Published English baseline</h4><p>{ex['baseline_response_en']}</p></div></div></article>")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>{label}</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1100px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}img{{width:100%;height:auto;display:block}}figure{{margin:18px 0;border:1px solid #d9d0c4;background:#fff;padding:12px}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>{label}</h1><p>Detailed full-scale report for {field_label.lower()} compared with the published English baseline across all 54 cells per model.</p><h2>Model Summary</h2><div class='cards'>{''.join(cards)}</div><h2>Figures</h2><figure><img src='figures/mean_response_length_by_model.png'><figcaption>Mean response length by model.</figcaption></figure><figure><img src='figures/decision_distribution_by_model.png'><figcaption>Preferred-solution distribution by model.</figcaption></figure><h2>Representative Examples</h2>{''.join(examples_html)}</main></body></html>"""
    handout_html = out_root / "handout.html"
    handout_html.write_text(html, encoding="utf-8")
    export_pdf(handout_html)
    return out_root


def build_three_way_package(records: list[dict], out_root: Path) -> Path:
    out_root.mkdir(parents=True, exist_ok=True)
    render_three_way_graphs(records, out_root)
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model_label"]].append(r)
    md = ["# English vs Constrained Yoruba vs Unrestricted Yoruba\n", "## Summary Metrics\n"]
    for model in MODEL_ORDER:
        subset = by_model[model]
        md.append(f"- {model}: mean constrained `{mean(r['constrained_length'] for r in subset):.1f}`, mean control `{mean(r['control_length'] for r in subset):.1f}`, mean English `{mean(r['english_length'] for r in subset):.1f}`")
        md.append(f"  - constrained decisions: {dict(Counter(r['constrained_decision'] for r in subset))}")
        md.append(f"  - control decisions: {dict(Counter(r['control_decision'] for r in subset))}")
        md.append(f"  - English decisions: {dict(Counter(r['english_decision'] for r in subset))}")
    md.append("\n## Representative Three-Way Examples\n")
    examples = []
    for model in MODEL_ORDER:
        subset = by_model[model]
        chosen = max(subset, key=lambda r: abs(r['control_length'] - r['constrained_length']))
        examples.append(chosen)
    for ex in examples:
        md.extend([
            f"### {ex['model_label']} / {ex['dilemma_id']} / {ex['framing_type']}",
            "",
            f"- constrained decision: `{ex['constrained_decision']}`",
            f"- unrestricted control decision: `{ex['control_decision']}`",
            f"- English baseline decision: `{ex['english_decision']}`",
            "",
            "**Constrained Yoruba**",
            "",
            short_excerpt(ex['constrained_response_yo'], 700),
            "",
            "**Unrestricted Yoruba control**",
            "",
            short_excerpt(ex['control_response_yo'], 700),
            "",
            "**Published English baseline**",
            "",
            short_excerpt(ex['english_response_en'], 900),
            "",
        ])
    (out_root / "report.md").write_text("\n".join(md), encoding="utf-8")
    cards = []
    for model in MODEL_ORDER:
        subset = by_model[model]
        cards.append(f"<section class='card'><h3>{model}</h3><p><strong>Constrained:</strong> {mean(r['constrained_length'] for r in subset):.1f}</p><p><strong>Control:</strong> {mean(r['control_length'] for r in subset):.1f}</p><p><strong>English:</strong> {mean(r['english_length'] for r in subset):.1f}</p></section>")
    examples_html = []
    for ex in examples:
        examples_html.append(f"<article class='example'><h3>{ex['model_label']} / {ex['dilemma_id']} / {FRAMING_LABELS.get(ex['framing_type'], ex['framing_type'])}</h3><p class='meta'>Constrained: <strong>{ex['constrained_decision']}</strong> | Control: <strong>{ex['control_decision']}</strong> | English: <strong>{ex['english_decision']}</strong></p><div class='twocol'><div class='panel'><h4>Constrained Yoruba</h4><p>{ex['constrained_response_yo']}</p><h4>Control Yoruba</h4><p>{ex['control_response_yo']}</p></div><div class='panel'><h4>Published English baseline</h4><p>{ex['english_response_en']}</p></div></div></article>")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Three-way comparison</title><style>body{{margin:0;background:#f4f0e8;color:#1a1a1a;font:16px/1.55 Georgia,serif}}.page{{width:min(1100px,calc(100vw - 32px));margin:24px auto;background:#fffdfa;border:1px solid #d9d0c4;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:40px 46px 52px}}h1,h2,h3,h4{{line-height:1.2}}h2{{margin-top:30px;padding-top:10px;border-top:2px solid #d9d0c4;color:#6d3d14}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.card,.panel,.example{{border:1px solid #d9d0c4;background:#fff;padding:16px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}img{{width:100%;height:auto;display:block}}figure{{margin:18px 0;border:1px solid #d9d0c4;background:#fff;padding:12px}}.meta{{color:#5f5a54}}@media(max-width:900px){{.cards,.twocol{{grid-template-columns:1fr}}.page{{padding:24px}}}}@media print{{body{{background:#fff}}.page{{width:auto;margin:0;border:0;box-shadow:none}}}}</style></head><body><main class='page'><h1>English vs Constrained Yoruba vs Unrestricted Yoruba</h1><p>Detailed three-way comparison across the full 6×9×3 design.</p><h2>Model Summary</h2><div class='cards'>{''.join(cards)}</div><h2>Figure</h2><figure><img src='figures/three_way_mean_length.png'><figcaption>Three-way mean response length by model.</figcaption></figure><h2>Representative Examples</h2>{''.join(examples_html)}</main></body></html>"""
    html_path = out_root / "handout.html"
    html_path.write_text(html, encoding="utf-8")
    export_pdf(html_path)
    return out_root


def main() -> None:
    constrained = load_condition_records(CONSTRAINED_DIRS, "constrained")
    control = load_condition_records(CONTROL_DIRS, "control")
    three_way = make_three_way_records(constrained, control)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = OUTPUTS / f"full_scale_report_packages_{timestamp}"
    constrained_root = root / "constrained_vs_english"
    control_root = root / "control_vs_english"
    three_way_root = root / "three_way"

    build_condition_package(constrained, "Constrained Yoruba vs Published English", constrained_root, "Constrained Yoruba")
    build_condition_package(control, "Unrestricted Yoruba Control vs Published English", control_root, "Unrestricted Yoruba control")
    build_three_way_package(three_way, three_way_root)

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "root": str(root),
        "constrained_records": len(constrained),
        "control_records": len(control),
        "three_way_records": len(three_way),
    }
    with open(root / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print(root)


if __name__ == "__main__":
    main()
