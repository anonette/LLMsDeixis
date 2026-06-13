#!/usr/bin/env python3
"""Compare an unrestricted Yoruba bilingual session to a constrained Yoruba bilingual session."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, Any, Tuple

from session_utils import load_json, write_json


def build_lookup(bilingual_dir: Path) -> Tuple[str, str, Dict[Tuple[str, str], Dict[str, Any]]]:
    summary = load_json(bilingual_dir / "bilingual_summary.json")
    lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for file_path in sorted(bilingual_dir.glob("*_bilingual.json")):
        if file_path.name == "bilingual_summary.json":
            continue
        payload = load_json(file_path)
        for framing, record in payload["responses"].items():
            lookup[(payload["dilemma_id"], framing)] = record
    return summary["source_session"], summary["source_model"], lookup


def compare(control_bilingual_dir: Path, constrained_bilingual_dir: Path, output_dir: Path) -> Path:
    control_session, control_model, control_lookup = build_lookup(control_bilingual_dir)
    constrained_session, constrained_model, constrained_lookup = build_lookup(constrained_bilingual_dir)

    if control_model != constrained_model:
        raise ValueError(f"Model mismatch: control={control_model}, constrained={constrained_model}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = output_dir / f"{control_bilingual_dir.name}_vs_{constrained_bilingual_dir.name}_{timestamp}"
    if len(str(target_dir / "comparison_summary.json")) >= 240:
        model_slug = control_model.lower().replace("/", "_").replace(".", "")
        target_dir = output_dir / f"{model_slug}_control_vs_constrained_{timestamp}"
    target_dir.mkdir(parents=True, exist_ok=True)

    paired = []
    for key in sorted(set(control_lookup) & set(constrained_lookup)):
        dilemma_id, framing_type = key
        control = control_lookup[key]
        constrained = constrained_lookup[key]
        paired.append(
            {
                "model": control_model,
                "dilemma_id": dilemma_id,
                "framing_type": framing_type,
                "prompt_yo": control["prompt_yo"],
                "prompt_en_reference": control.get("prompt_en_reference", ""),
                "control_response_yo": control["response_yo"],
                "control_response_en_academic": control["response_en_academic"],
                "constrained_response_yo": constrained["response_yo"],
                "constrained_response_en_academic": constrained["response_en_academic"],
                "control_response_length": len(control["response_yo"]),
                "constrained_response_length": len(constrained["response_yo"]),
                "length_delta_control_minus_constrained": len(control["response_yo"]) - len(constrained["response_yo"]),
                "control_source_session": control_session,
                "constrained_source_session": constrained_session,
            }
        )

    write_json(
        target_dir / "paired_control_vs_constrained.json",
        {
            "model": control_model,
            "control_source_session": control_session,
            "constrained_source_session": constrained_session,
            "paired_records": paired,
            "generated_at": datetime.now().isoformat(),
        },
    )

    with open(target_dir / "paired_control_vs_constrained.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(paired[0].keys()) if paired else [])
        if paired:
            writer.writeheader()
            writer.writerows(paired)

    summary = {
        "model": control_model,
        "control_source_session": control_session,
        "constrained_source_session": constrained_session,
        "paired_records": len(paired),
        "mean_control_length": mean(row["control_response_length"] for row in paired) if paired else 0,
        "mean_constrained_length": mean(row["constrained_response_length"] for row in paired) if paired else 0,
        "mean_length_delta_control_minus_constrained": mean(row["length_delta_control_minus_constrained"] for row in paired) if paired else 0,
        "generated_at": datetime.now().isoformat(),
    }
    write_json(target_dir / "comparison_summary.json", summary)

    lines = [
        f"# Control vs Constrained Yoruba Comparison",
        "",
        f"- Model: `{control_model}`",
        f"- Control session: `{control_session}`",
        f"- Constrained session: `{constrained_session}`",
        f"- Paired records: `{summary['paired_records']}`",
        f"- Mean control response length: `{summary['mean_control_length']:.1f}`",
        f"- Mean constrained response length: `{summary['mean_constrained_length']:.1f}`",
        f"- Mean length delta (control - constrained): `{summary['mean_length_delta_control_minus_constrained']:.1f}`",
        "",
    ]
    for row in paired:
        lines.extend(
            [
                f"## {row['dilemma_id']} / {row['framing_type']}",
                "",
                "**Control Yoruba**",
                "",
                row["control_response_yo"],
                "",
                "**Constrained Yoruba**",
                "",
                row["constrained_response_yo"],
                "",
                "**Control English Translation**",
                "",
                row["control_response_en_academic"],
                "",
                "**Constrained English Translation**",
                "",
                row["constrained_response_en_academic"],
                "",
            ]
        )
    (target_dir / "comparison_report.md").write_text("\n".join(lines), encoding="utf-8")
    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare unrestricted Yoruba responses to constrained Yoruba responses")
    parser.add_argument("control_bilingual_dir", help="Path to unrestricted bilingual session directory")
    parser.add_argument("constrained_bilingual_dir", help="Path to constrained bilingual session directory")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "outputs" / "control_vs_constrained"),
        help="Directory where comparison outputs should be written",
    )
    args = parser.parse_args()

    target_dir = compare(Path(args.control_bilingual_dir), Path(args.constrained_bilingual_dir), Path(args.output_dir))
    print(f"[DONE] Control-vs-constrained comparison written to {target_dir}")


if __name__ == "__main__":
    main()
