#!/usr/bin/env python3
"""Pair a bilingual Yoruba session with the published English baseline for the matching model."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

from session_utils import iterate_response_records, load_json, write_json


def build_english_lookup(session_dir: Path) -> Dict[Tuple[str, str], Dict[str, Any]]:
    lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for record in iterate_response_records(session_dir):
        lookup[(record["dilemma_id"], record["framing_type"])] = record
    return lookup


def build_yoruba_lookup(bilingual_dir: Path) -> Tuple[str, Dict[Tuple[str, str], Dict[str, Any]]]:
    summary = load_json(bilingual_dir / "bilingual_summary.json")
    lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for file_path in sorted(bilingual_dir.glob("*_bilingual.json")):
        if file_path.name == "bilingual_summary.json":
            continue
        payload = load_json(file_path)
        for framing, record in payload["responses"].items():
            lookup[(payload["dilemma_id"], framing)] = record
    return summary["source_model"], lookup


def normalize_model_key(model_name: str) -> str:
    model_name = model_name.lower()
    if "deepseek" in model_name:
        return "DeepSeek"
    if "claude" in model_name:
        return "Claude 3.5 Sonnet"
    return "GPT-4o"


def compare(
    bilingual_dir: Path,
    baseline_manifest: Path,
    output_dir: Path,
    baseline_model_key: str | None = None,
) -> Path:
    source_model, yoruba_lookup = build_yoruba_lookup(bilingual_dir)
    baseline_data = load_json(baseline_manifest)
    model_key = baseline_model_key or normalize_model_key(source_model)
    baseline_info = baseline_data["models"][model_key]
    cross_model_note = None
    if baseline_model_key and normalize_model_key(source_model) != baseline_model_key:
        cross_model_note = (
            f"Yoruba source model '{source_model}' has no published English baseline; "
            f"paired against '{baseline_model_key}' English sessions for structural alignment only."
        )
    english_session_dir = baseline_manifest.parent.parent.parent / baseline_info["path"]
    english_lookup = build_english_lookup(english_session_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = output_dir / f"{bilingual_dir.name}_vs_published_english_{timestamp}"
    if len(str(target_dir / "comparison_summary.json")) >= 240:
        model_slug = normalize_model_key(source_model).lower().replace(" ", "_").replace(".", "")
        target_dir = output_dir / f"{model_slug}_vs_published_english_{timestamp}"
    target_dir.mkdir(parents=True, exist_ok=True)

    paired_records: List[Dict[str, Any]] = []
    for key, yoruba_record in sorted(yoruba_lookup.items()):
        dilemma_id, framing_type = key
        english_record = english_lookup.get(key)
        paired_records.append(
            {
                "model": source_model,
                "dilemma_id": dilemma_id,
                "framing_type": framing_type,
                "prompt_yo": yoruba_record["prompt_yo"],
                "prompt_en_reference": yoruba_record.get("prompt_en_reference", ""),
                "response_yo": yoruba_record["response_yo"],
                "response_en_academic": yoruba_record["response_en_academic"],
                "baseline_response_en": english_record["response"] if english_record else "",
                "yoruba_response_length": len(yoruba_record["response_yo"]),
                "yoruba_translation_length": len(yoruba_record["response_en_academic"]),
                "baseline_response_length": len(english_record["response"]) if english_record else 0,
                "published_english_session": baseline_info["session"],
                "yoruba_source_session": bilingual_dir.name,
            }
        )

    write_json(
        target_dir / "paired_comparison.json",
        {
            "yoruba_source_session": bilingual_dir.name,
            "published_english_session": baseline_info["session"],
            "model": source_model,
            "paired_records": paired_records,
            "generated_at": datetime.now().isoformat(),
        },
    )

    with open(target_dir / "paired_comparison.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(paired_records[0].keys()) if paired_records else [])
        if paired_records:
            writer.writeheader()
            writer.writerows(paired_records)

    summary_payload = {
        "yoruba_source_session": bilingual_dir.name,
        "published_english_session": baseline_info["session"],
        "model": source_model,
        "baseline_model_key": model_key,
        "paired_records": len(paired_records),
        "generated_at": datetime.now().isoformat(),
    }
    if cross_model_note:
        summary_payload["cross_model_pairing_note"] = cross_model_note
    write_json(target_dir / "comparison_summary.json", summary_payload)
    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare a bilingual Yoruba session to the published English baseline")
    parser.add_argument("bilingual_dir", help="Path to a bilingual Yoruba session directory")
    parser.add_argument(
        "--baseline-manifest",
        default=str(Path(__file__).resolve().parent / "published_english_baseline.json"),
        help="Path to the published English baseline manifest",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "outputs" / "comparisons"),
        help="Directory where comparison outputs should be written",
    )
    parser.add_argument(
        "--baseline-model-key",
        default=None,
        help="Override baseline model key from published_english_baseline.json (e.g. GPT-4o for n-atlas)",
    )
    args = parser.parse_args()

    target_dir = compare(
        Path(args.bilingual_dir),
        Path(args.baseline_manifest),
        Path(args.output_dir),
        baseline_model_key=args.baseline_model_key,
    )
    print(f"[DONE] Comparison written to {target_dir}")


if __name__ == "__main__":
    main()
