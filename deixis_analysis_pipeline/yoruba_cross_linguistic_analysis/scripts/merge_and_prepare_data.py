#!/usr/bin/env python3
"""Merge pronoun counts with coded data and prepare for visualization."""

import json
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import REPO_ROOT, normalize_coded_model  # noqa: E402


def load_data():
    yoruba_pronouns = pd.read_csv(ac.DATA_DIR / "yoruba_pronoun_analysis.csv")

    with open(ac.MERGED_CODING_JSON, "r", encoding="utf-8") as handle:
        yoruba_coded_raw = json.load(handle)

    english_coded_path = REPO_ROOT / "yoruba_deixis_module" / "outputs" / "english_coded_content"
    english_coded_file = english_coded_path / "english_open_comparison_coded_20260608_175242" / "coded_content.csv"
    english_coded = pd.read_csv(english_coded_file) if english_coded_file.exists() else None

    paired_path = REPO_ROOT / "CONSOLIDATED_REPORTS" / "yoruba" / "comparisons" / "openai_claude_20260608"
    paired_file = paired_path / "paired_comparison.csv"
    paired_data = pd.read_csv(paired_file) if paired_file.exists() else None

    return yoruba_pronouns, yoruba_coded_raw, english_coded, paired_data


def process_yoruba_coded(coded_raw):
    records = []
    for item in coded_raw.get("records", []):
        record = {
            "model": normalize_coded_model(item.get("model", "")),
            "dilemma_id": item.get("dilemma_id", ""),
            "framing_type": item.get("framing_type", ""),
            "preferred_solution": item.get("preferred_solution", ""),
            "ethical_preference_type": item.get("ethical_preference_type", ""),
            "response_genre": item.get("response_genre", ""),
            "deictic_uptake_quality": item.get("deictic_uptake_quality", ""),
            "language_stability": item.get("language_stability", ""),
            "contains_framework_labels": item.get("contains_framework_labels", False),
            "contains_translation_behavior": item.get("contains_translation_behavior", False),
            "contains_followup_question": item.get("contains_followup_question", False),
            "evidence_span_yo": str(item.get("evidence_span_yo", ""))[:200],
        }
        records.append(record)
    return pd.DataFrame(records)


def merge_datasets(yoruba_pronouns, yoruba_coded_df):
    return pd.merge(
        yoruba_coded_df,
        yoruba_pronouns,
        on=["model", "dilemma_id", "framing_type"],
        how="left",
    )


def calculate_summary_statistics(merged_df):
    stats = {}
    stats["model"] = merged_df.groupby("model").agg(
        {
            "emphatic_ratio": ["mean", "std"],
            "emphatic_ratio_raw": ["mean", "std"],
            "pronouns_per_100_words": ["mean", "std"],
            "word_count": ["mean", "std"],
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_emi_emphatic_per_100w": "mean",
            "first_singular_emi_life_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
        }
    )
    stats["framing"] = merged_df.groupby(["model", "framing_type"]).agg(
        {
            "emphatic_ratio": "mean",
            "pronouns_per_100_words": "mean",
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
        }
    )
    stats["ethics"] = merged_df.groupby(["model", "ethical_preference_type"]).agg(
        {
            "emphatic_ratio": "mean",
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
        }
    )
    stats["genre"] = merged_df.groupby(["model", "response_genre"]).agg(
        {"emphatic_ratio": "mean", "pronouns_per_100_words": "mean"}
    )
    stats["language"] = merged_df.groupby(["model", "language_stability"]).agg(
        {"pronouns_per_100_words": "mean", "emphatic_ratio": "mean"}
    )
    stats["uptake"] = merged_df.groupby(["model", "deictic_uptake_quality"]).agg(
        {"emphatic_ratio": "mean", "pronouns_per_100_words": "mean"}
    )
    return stats


def main():
    print("Loading data...")
    yoruba_pronouns, yoruba_coded_raw, _english_coded, _paired_data = load_data()

    print("Processing Yoruba coded data...")
    yoruba_coded_df = process_yoruba_coded(yoruba_coded_raw)

    print("Merging datasets...")
    merged_df = merge_datasets(yoruba_pronouns, yoruba_coded_df)

    print("Calculating summary statistics...")
    stats = calculate_summary_statistics(merged_df)

    ac.DATA_DIR.mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv", index=False, encoding="utf-8")

    summary = {
        "generated_at": pd.Timestamp.now().isoformat(),
        "condition": ac.active_condition(),
        "models": sorted(merged_df["model"].unique().tolist()),
        "record_count": len(merged_df),
        "emphatic_ratio_by_model": merged_df.groupby("model")["emphatic_ratio"].mean().to_dict(),
        "emphatic_ratio_raw_by_model": merged_df.groupby("model")["emphatic_ratio_raw"].mean().to_dict()
        if "emphatic_ratio_raw" in merged_df.columns
        else {},
        "mi_per_100w_by_model": merged_df.groupby("model")["first_singular_mi_per_100w"].mean().to_dict()
        if "first_singular_mi_per_100w" in merged_df.columns
        else {},
    }
    with open(ac.DATA_DIR / "summary_statistics.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    for key, frame in stats.items():
        frame.to_csv(ac.DATA_DIR / f"stats_{key}.csv", encoding="utf-8")

    print("\n=== KEY FINDINGS ===")
    print("\nEmphatic Ratio by Model:")
    print(stats["model"]["emphatic_ratio"])

    if "first_singular_mi_per_100w" in merged_df.columns:
        print("\nMi (object/reflexive) per 100 words by Model:")
        print(merged_df.groupby("model")["first_singular_mi_per_100w"].mean())

    print("\nEmphatic Ratio by Framing (top rows):")
    print(stats["framing"]["emphatic_ratio"].reset_index().head(12))

    return merged_df, stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()
