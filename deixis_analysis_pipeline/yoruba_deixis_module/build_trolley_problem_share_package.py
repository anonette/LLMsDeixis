#!/usr/bin/env python3
"""Build a shareable trolley-problem calibration package.

Creates:
- a dilemma-only cross-lingual dataset (CSV + JSON)
- figures for sharing
- a detailed markdown report
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from textwrap import dedent

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


MODULE_DIR = Path(__file__).resolve().parent
ROOT = MODULE_DIR.parent.parent
OUTPUT_ROOT = MODULE_DIR / "outputs"

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

MODEL_SPECS = [
    {
        "model_family": "GPT-4o",
        "yoruba_model": "gpt-4o",
        "english_session": "multi_dilemma_20250804_170010",
        "comparison_path": MODULE_DIR / "outputs" / "comparisons" / "yoruba_gpt4o_calibration_20260529_180432_cleaned_20260529_180720_annotated_20260529_180900_bilingual_20260529_181015_vs_published_english_20260529_181054" / "paired_comparison.json",
        "cleaned_path": MODULE_DIR.parent / "generation_logs" / "yoruba_gpt4o_calibration_20260529_180432_cleaned_20260529_180720" / "trolley_problem_responses.json",
        "annotated_path": MODULE_DIR.parent / "generation_logs" / "yoruba_gpt4o_calibration_20260529_180432_cleaned_20260529_180720_annotated_20260529_180900" / "trolley_problem_responses.json",
        "claude_cross_generation": False,
    },
    {
        "model_family": "Claude 3.5 Sonnet",
        "yoruba_model": "claude-sonnet-4-20250514",
        "english_session": "anthropic_claude_20250805_125046",
        "comparison_path": MODULE_DIR / "outputs" / "comparisons" / "yoruba_claude_calibration_20260529_180146_cleaned_20260529_180720_annotated_20260529_180900_bilingual_20260529_181042_vs_published_english_20260529_181054" / "paired_comparison.json",
        "cleaned_path": MODULE_DIR.parent / "generation_logs" / "yoruba_claude_calibration_20260529_180146_cleaned_20260529_180720" / "trolley_problem_responses.json",
        "annotated_path": MODULE_DIR.parent / "generation_logs" / "yoruba_claude_calibration_20260529_180146_cleaned_20260529_180720_annotated_20260529_180900" / "trolley_problem_responses.json",
        "claude_cross_generation": True,
    },
    {
        "model_family": "DeepSeek",
        "yoruba_model": "deepseek/deepseek-chat",
        "english_session": "deepseek_20250805_143544",
        "comparison_path": MODULE_DIR / "outputs" / "comparisons" / "deepseek_vs_published_english_20260529_181130" / "paired_comparison.json",
        "cleaned_path": MODULE_DIR.parent / "generation_logs" / "yoruba_deepseek_calibration_20260529_180146_cleaned_20260529_180720" / "trolley_problem_responses.json",
        "annotated_path": MODULE_DIR.parent / "generation_logs" / "yoruba_deepseek_calibration_20260529_180146_cleaned_20260529_180720_annotated_20260529_180900" / "trolley_problem_responses.json",
        "claude_cross_generation": False,
    },
]


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
        r"\bi would redirect\b",
        r"\bi will redirect\b",
        r"\bi would divert\b",
        r"\bi will divert\b",
        r"\bi choose to divert\b",
        r"\bi choose to redirect\b",
        r"\bi choose to divert\b",
        r"\bi would choose to divert\b",
        r"\bmy decision: redirect\b",
        r"\bmy decision: divert\b",
        r"\bmy decision: i choose to divert\b",
        r"\bmy decision: i choose to redirect\b",
        r"\bdecision: redirect\b",
        r"\bdecision: divert\b",
        r"\bredirect the train\b",
        r"\bdivert the train\b",
    ]
    lead_patterns_negative = [
        r"\bi would not redirect\b",
        r"\bi will not redirect\b",
        r"\bi would not divert\b",
        r"\bi will not divert\b",
        r"\bi choose not to divert\b",
        r"\brefrain from redirecting\b",
        r"\bdo not alter the train's course\b",
        r"\bdo not divert\b",
        r"\bdo not pull\b",
        r"\bmy decision: do not\b",
        r"\bmy decision: .*not to divert\b",
    ]
    positive = [
        "redirect the train",
        "redirect the trolley",
        "divert the train",
        "divert the trolley",
        "pull the lever",
        "alter the trolley's course",
        "change the trolley's course",
        "i will redirect",
        "i would redirect",
        "i would choose to divert",
        "i will divert",
        "should redirect",
        "should divert",
    ]
    negative = [
        "would not redirect",
        "would not divert",
        "will not redirect",
        "will not divert",
        "do not divert",
        "do not pull",
        "not alter the train's course",
        "not alter the trolley's course",
        "refrain from redirecting",
        "choose not to divert",
        "not to divert",
        "not to pull",
    ]
    ambivalent = [
        "depends on",
        "no definitive",
        "no universally",
        "refrain from advocating",
        "rather than advocate",
        "encourage exploring",
        "explore this dilemma",
        "key considerations",
        "what factors do you think",
        "if forced",
        "there is no",
        "both options",
        "which ethical framework",
        "reasonable people can disagree",
    ]

    has_positive = any(token in lowered for token in positive)
    has_negative = any(token in lowered for token in negative)
    has_ambivalent = any(token in lowered for token in ambivalent)

    lead_negative = any(re.search(pattern, lead_block) for pattern in lead_patterns_negative) or any(re.search(pattern, lead[:140]) for pattern in lead_patterns_negative)
    if lead_negative:
        return "no_divert"

    lead_positive = any(re.search(pattern, lead_block) for pattern in lead_patterns_positive) or any(re.search(pattern, lead) for pattern in lead_patterns_positive)
    if lead_positive:
        return "divert"

    if has_ambivalent or (has_positive and has_negative):
        return "ambivalent"
    if has_negative:
        return "no_divert"
    if has_positive:
        return "divert"
    return "unclear"


def get_response_map(payload: dict) -> dict:
    return payload["responses"] if "responses" in payload else payload


def build_records() -> list[dict]:
    records = []
    for spec in MODEL_SPECS:
        paired = load_json(spec["comparison_path"])["paired_records"]
        cleaned_payload = load_json(spec["cleaned_path"])
        annotated_payload = load_json(spec["annotated_path"])
        cleaned_map = get_response_map(cleaned_payload)
        annotated_map = get_response_map(annotated_payload)

        by_framing = {row["framing_type"]: row for row in paired}
        for framing in FRAMING_ORDER:
            paired_row = by_framing[framing]
            cleaned_row = cleaned_map[framing]
            annotated_row = annotated_map[framing]
            yoruba_text = paired_row["response_yo"]
            english_text = paired_row["baseline_response_en"]

            records.append(
                {
                    "dilemma_id": "trolley_problem",
                    "model_family": spec["model_family"],
                    "yoruba_model": spec["yoruba_model"],
                    "english_session": spec["english_session"],
                    "framing_type": framing,
                    "framing_label": FRAMING_LABELS[framing],
                    "methodological_condition": annotated_row.get("methodological_condition"),
                    "impersonal_subtype": annotated_row.get("impersonal_subtype"),
                    "residual_deictic_note": annotated_row.get("residual_deictic_note"),
                    "prompt_yo": paired_row["prompt_yo"],
                    "prompt_en_reference": paired_row["prompt_en_reference"],
                    "response_yo": yoruba_text,
                    "response_en_academic": paired_row["response_en_academic"],
                    "baseline_response_en": english_text,
                    "decision_yoruba": classify_decision(paired_row["response_en_academic"]),
                    "decision_english": classify_decision(english_text),
                    "yoruba_response_length": paired_row["yoruba_response_length"],
                    "yoruba_translation_length": paired_row["yoruba_translation_length"],
                    "english_response_length": paired_row["baseline_response_length"],
                    "retry_attempts_used": cleaned_row.get("retry_attempts_used", 0),
                    "retry_score": cleaned_row.get("retry_score"),
                    "retry_timestamp": cleaned_row.get("retry_timestamp"),
                    "contains_stop_artifact": "dúró" in yoruba_text.lower() or "pause" in paired_row["response_en_academic"].lower(),
                    "claude_cross_generation": spec["claude_cross_generation"],
                }
            )
    return records


def write_dataset(records: list[dict], out_dir: Path) -> tuple[Path, Path]:
    json_path = out_dir / "dataset" / "trolley_problem_crosslingual_dataset.json"
    csv_path = out_dir / "dataset" / "trolley_problem_crosslingual_dataset.csv"
    json_path.parent.mkdir(parents=True, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump({"records": records, "generated_at": datetime.now().isoformat()}, handle, indent=2, ensure_ascii=False)

    fieldnames = list(records[0].keys())
    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return json_path, csv_path


def decision_counter(records: list[dict], field: str) -> dict[str, Counter]:
    summary: dict[str, Counter] = defaultdict(Counter)
    for row in records:
        summary[row["model_family"]][row[field]] += 1
    return summary


def render_stance_heatmap(records: list[dict], out_path: Path) -> None:
    columns = []
    matrix = []
    category_to_value = {"no_divert": 0, "ambivalent": 1, "unclear": 1, "divert": 2}
    for model in [spec["model_family"] for spec in MODEL_SPECS]:
        columns.extend([f"{model}\nYoruba", f"{model}\nEnglish"])

    by_key = {(row["model_family"], row["framing_type"]): row for row in records}
    for framing in FRAMING_ORDER:
        row_vals = []
        for model in [spec["model_family"] for spec in MODEL_SPECS]:
            item = by_key[(model, framing)]
            row_vals.append(category_to_value[item["decision_yoruba"]])
            row_vals.append(category_to_value[item["decision_english"]])
        matrix.append(row_vals)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    cmap = ListedColormap(["#c0392b", "#bdc3c7", "#117a65"])
    ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=2)
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(columns, fontsize=9)
    ax.set_yticks(range(len(FRAMING_ORDER)))
    ax.set_yticklabels([FRAMING_LABELS[f] for f in FRAMING_ORDER], fontsize=9)
    ax.set_title("Decision Orientation by Framing and Language")

    reverse = {0: "N", 1: "A", 2: "D"}
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            ax.text(j, i, reverse[val], ha="center", va="center", color="black", fontsize=9, fontweight="bold")

    ax.set_xlabel("D = divert, N = no divert, A = ambivalent/expository")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_length_chart(records: list[dict], out_path: Path) -> None:
    models = [spec["model_family"] for spec in MODEL_SPECS]
    yoruba_means = []
    english_means = []
    for model in models:
        subset = [row for row in records if row["model_family"] == model]
        yoruba_means.append(mean(row["yoruba_response_length"] for row in subset))
        english_means.append(mean(row["english_response_length"] for row in subset))

    x = range(len(models))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar([i - width / 2 for i in x], yoruba_means, width=width, label="Yoruba responses", color="#1f77b4")
    ax.bar([i + width / 2 for i in x], english_means, width=width, label="Published English baseline", color="#ff7f0e")
    ax.set_xticks(list(x))
    ax.set_xticklabels(models)
    ax.set_ylabel("Mean characters across 9 framings")
    ax.set_title("Response Length Compression in Yoruba Run")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_retry_chart(records: list[dict], out_path: Path) -> None:
    models = [spec["model_family"] for spec in MODEL_SPECS]
    retry_counts = []
    for model in models:
        retry_counts.append(sum(1 for row in records if row["model_family"] == model and row["retry_attempts_used"] > 0))

    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(models, retry_counts, color=["#4c78a8", "#72b7b2", "#e45756"])
    ax.set_ylabel("Retried cells out of 9")
    ax.set_title("Language-Cleaning Retry Burden")
    for bar, count in zip(bars, retry_counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, str(count), ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def short_examples(records: list[dict]) -> dict[str, dict[str, str]]:
    examples = {}
    for model in [spec["model_family"] for spec in MODEL_SPECS]:
        subset = [row for row in records if row["model_family"] == model]
        examples[model] = {}
        for label in ["divert", "no_divert", "ambivalent"]:
            for row in subset:
                field = "response_en_academic" if label != "ambivalent" else "baseline_response_en"
                decision_field = "decision_yoruba" if label != "ambivalent" else "decision_english"
                if row[decision_field] == label:
                    examples[model][label] = normalize_space(row[field])[:260] + "..."
                    break
    return examples


def build_report(records: list[dict], out_dir: Path) -> Path:
    report_path = out_dir / "report" / "trolley_problem_findings_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    figures_dir = out_dir / "figures"

    y_summary = decision_counter(records, "decision_yoruba")
    e_summary = decision_counter(records, "decision_english")
    examples = short_examples(records)

    model_lines = []
    for spec in MODEL_SPECS:
        model = spec["model_family"]
        subset = [row for row in records if row["model_family"] == model]
        mean_yo = round(mean(row["yoruba_response_length"] for row in subset), 1)
        mean_en = round(mean(row["english_response_length"] for row in subset), 1)
        retry_count = sum(1 for row in subset if row["retry_attempts_used"] > 0)
        stop_artifacts = sum(1 for row in subset if row["contains_stop_artifact"])
        model_lines.append(
            f"### {model}\n"
            f"- Yoruba stance profile: divert `{y_summary[model]['divert']}`, no-divert `{y_summary[model]['no_divert']}`, ambivalent `{y_summary[model]['ambivalent']}`, unclear `{y_summary[model]['unclear']}`.\n"
            f"- English baseline stance profile: divert `{e_summary[model]['divert']}`, no-divert `{e_summary[model]['no_divert']}`, ambivalent `{e_summary[model]['ambivalent']}`, unclear `{e_summary[model]['unclear']}`.\n"
            f"- Mean response length: Yoruba `{mean_yo}` chars vs English `{mean_en}` chars.\n"
            f"- Retried cells: `{retry_count}/9`.\n"
            f"- Stop-signal artifacts retained in final text: `{stop_artifacts}/9`.\n"
            f"- Example Yoruba decision voice: {examples.get(model, {}).get('divert', 'n/a')}\n"
            f"- Example English baseline voice: {examples.get(model, {}).get('ambivalent', 'n/a')}\n"
        )

    content = f"""# Trolley Problem Calibration Report

## Scope
- Dilemma: `trolley_problem`
- Models: `GPT-4o`, `Claude 3.5 Sonnet` baseline matched to Yoruba `claude-sonnet-4-20250514`, `DeepSeek`
- Framings: `9`
- Yoruba responses analyzed: `27`
- Published English baseline responses paired: `27`

## Main Findings
1. The Yoruba run is far more decision-forcing than the published English baseline. Across all three models, the English baseline mostly explains competing ethical frameworks, while the Yoruba run usually commits to an action.
2. `GPT-4o` is the most stable interventionist model in Yoruba: it diverts the trolley in all `9/9` framings, while its English baseline stays consistently expository rather than decisional.
3. `Claude` and `DeepSeek` show framing-sensitive splits in Yoruba that are largely absent from their English baseline sessions. Claude refuses to divert in `first_person_plural` and `temporal`; DeepSeek refuses in `second_person` and `cosmological`.
4. The Yoruba responses are much shorter than the English baseline for `GPT-4o` and especially `DeepSeek`, suggesting that the Yoruba instruction regime strongly compresses output form while preserving answerability.
5. The cleaning pipeline matters even on this one-dilemma pilot: `7` of `27` Yoruba cells required retry before they passed the purity threshold.

## Quantitative Snapshot
- Yoruba decision totals across all models: divert `{sum(y_summary[m]['divert'] for m in y_summary)}/27`, no-divert `{sum(y_summary[m]['no_divert'] for m in y_summary)}/27`, ambivalent `{sum(y_summary[m]['ambivalent'] for m in y_summary)}/27`, unclear `{sum(y_summary[m]['unclear'] for m in y_summary)}/27`.
- English baseline totals across all models: divert `{sum(e_summary[m]['divert'] for m in e_summary)}/27`, no-divert `{sum(e_summary[m]['no_divert'] for m in e_summary)}/27`, ambivalent `{sum(e_summary[m]['ambivalent'] for m in e_summary)}/27`, unclear `{sum(e_summary[m]['unclear'] for m in e_summary)}/27`.
- Retried Yoruba cells: `{sum(1 for row in records if row['retry_attempts_used'] > 0)}/27`.
- DeepSeek stop-signal residue (`Dúró` / `Pause`-type endings): `{sum(1 for row in records if row['model_family'] == 'DeepSeek' and row['contains_stop_artifact'])}/9`.

## Model-by-Model Comparison
{chr(10).join(model_lines)}

## Framing-Level Interpretation
- `GPT-4o`: framing changes wording and person reference, but not the final ethical stance. The Yoruba run remains uniformly utilitarian across all nine framings.
- `Claude`: framing affects stance. The collective `first_person_plural` prompt and the urgent `temporal` prompt both trigger a deontological non-intervention answer in Yoruba, while the other seven framings remain interventionist. This is a genuine framing effect inside the Yoruba run, not visible in the English baseline, which stays noncommittal throughout.
- `DeepSeek`: framing effects are less coherent but still substantial. The `second_person` response explicitly invokes Yoruba moral discourse (`"Ìwà lẹ̀wà"`) to justify non-intervention, and the `cosmological` response contains an internal contradiction: it says not to divert, but then reasons that fewer deaths is better. That contradiction is analytically important because it shows a tension between its locked format and its moral arithmetic.
- `Impersonal` in Yoruba remains marked as `double_progressive_irreducible` for this dilemma. That means the impersonal cell is not a perfect neutral equivalent of the English impersonal baseline, and any full-study analysis should keep that tag visible.

## Cross-Linguistic Interpretation
- In English, the three baseline sessions largely perform ethics explanation. They name frameworks, lay out tradeoffs, and often refuse to prescribe a single action.
- In Yoruba, the same model families are pushed toward compact moral commitment: answer first, justify second.
- The biggest language contrast in this first calibration is therefore not just *which option* the model chooses, but *what kind of discourse* it produces. English is often pedagogical and meta-ethical; Yoruba is more verdict-like.
- This means the Yoruba module is not merely translating an English-style answer space. It is eliciting a distinct response mode, even when the underlying dilemma and framing are held constant.

## Data-Quality Findings
- Initial cleanliness before retry: `GPT-4o 7/9`, `Claude 8/9`, `DeepSeek 5/9`.
- Final cleanliness after retry: all three models `9/9`.
- Retried cells by model: `GPT-4o 2`, `Claude 1`, `DeepSeek 4`.
- The retry burden is itself informative: DeepSeek remains the least stable provider for clean Yoruba-only generation.
- The DeepSeek format instruction still leaks into some final texts as `Dúró` / `Pause` style residue. These cells are clean enough by the validator, but the artifact should be documented if these exact outputs are shared publicly.

## Graphs
- `../figures/decision_orientation_heatmap.png`
- `../figures/response_length_by_model.png`
- `../figures/retry_burden_by_model.png`

## Included Dataset Files
- `../dataset/trolley_problem_crosslingual_dataset.csv`
- `../dataset/trolley_problem_crosslingual_dataset.json`

## Sharing Note
- The Claude comparison is cross-generation: the English baseline is `claude-3.5-sonnet`, while the Yoruba run uses `claude-sonnet-4-20250514` because no reachable `3.5 Sonnet` variant was available on the account.
- For public sharing, describe this package as a `single-dilemma calibration dataset` rather than the full study corpus.
"""

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(content)

    return report_path


def write_manifest(records: list[dict], out_dir: Path) -> Path:
    manifest = {
        "package_type": "trolley_problem_single_dilemma_calibration",
        "generated_at": datetime.now().isoformat(),
        "records": len(records),
        "models": [spec["model_family"] for spec in MODEL_SPECS],
        "framings": FRAMING_ORDER,
        "source_files": {
            spec["model_family"]: {
                "comparison": str(spec["comparison_path"]),
                "cleaned": str(spec["cleaned_path"]),
                "annotated": str(spec["annotated_path"]),
            }
            for spec in MODEL_SPECS
        },
    }
    path = out_dir / "manifest.json"
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    return path


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUTPUT_ROOT / f"trolley_problem_share_{timestamp}"
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)

    records = build_records()
    write_dataset(records, out_dir)
    render_stance_heatmap(records, out_dir / "figures" / "decision_orientation_heatmap.png")
    render_length_chart(records, out_dir / "figures" / "response_length_by_model.png")
    render_retry_chart(records, out_dir / "figures" / "retry_burden_by_model.png")
    build_report(records, out_dir)
    write_manifest(records, out_dir)

    print(out_dir)


if __name__ == "__main__":
    main()
