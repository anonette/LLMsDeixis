#!/usr/bin/env python3
"""Merge full open Yoruba coding outputs into one article-ready package."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


MODULE = Path(__file__).resolve().parent
CODED = MODULE / "outputs" / "coded_content"
OUT_ROOT = MODULE / "outputs" / "open_yoruba_coding_merged_20260608"

SOURCE_DIRS = [
    CODED / "yoruba_control_gpt4o_20260608_120259_coded_20260608_162937",
    CODED / "yoruba_control_claude_20260608_122738_coded_20260608_162909",
    CODED / "yoruba_control_deepseek_20260608_124633_coded_20260608_164108",
]


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_model(model: str) -> str:
    lowered = model.lower()
    if "deepseek" in lowered:
        return "DeepSeek"
    if "claude" in lowered:
        return "Claude"
    return "GPT-4o"


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for directory in SOURCE_DIRS:
        payload = load_json(directory / "coded_content.json")
        for row in payload["coded_records"]:
            row = dict(row)
            row["model_label"] = normalize_model(row["model"])
            rows.append(row)

    # write merged csv/json
    with open(OUT_ROOT / "open_yoruba_coded_content_merged.json", "w", encoding="utf-8") as handle:
        json.dump({"records": rows, "generated_at": datetime.now().isoformat()}, handle, indent=2, ensure_ascii=False)

    with open(OUT_ROOT / "open_yoruba_coded_content_merged.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model_label"]].append(row)

    lines = []
    lines.append("# Open Yoruba Coding Summary\n")
    lines.append("This package merges the full raw-session coding outputs for the unrestricted Yoruba corpus across GPT-4o, Claude, and DeepSeek.\n")
    lines.append("## Summary by model\n")
    for model in ["GPT-4o", "Claude", "DeepSeek"]:
        subset = by_model[model]
        lines.append(f"### {model}\n")
        lines.append(f"- Records coded: `{len(subset)}`")
        lines.append(f"- Preferred solution distribution: `{dict(Counter(r['preferred_solution'] for r in subset))}`")
        lines.append(f"- Ethical preference distribution: `{dict(Counter(r['ethical_preference_type'] for r in subset))}`")
        lines.append(f"- Response genre distribution: `{dict(Counter(r['response_genre'] for r in subset))}`")
        lines.append(f"- Needs second coder review: `{sum(1 for r in subset if r['needs_second_coder_review'])}`\n")

    lines.append("## Cross-model observations\n")
    lines.append("- GPT-4o is the most consistently expository and least decisive in the open Yoruba condition, with most cells coded as `conditional_or_mixed` and `balanced_framework_exposition`.")
    lines.append("- Claude is the most substantively classifiable in ethical terms: it shows the broadest spread across `supports_A`, `supports_B`, `conditional_or_mixed`, and `refuses_to_commit`, and also the richest spread of ethical preference types.")
    lines.append("- DeepSeek is the least stable: it has the largest review burden and the clearest translation/meta-commentary drift, including `translation_or_gloss`, `meta_commentary`, and `uncodable` cases.\n")

    lines.append("## Suggested article use\n")
    lines.append("- Use the merged CSV as the master coding table for the unrestricted Yoruba corpus.")
    lines.append("- Treat rows marked `needs_second_coder_review = True` as the adjudication subset.")
    lines.append("- Compare English and Yoruba not only by preferred solution, but also by response genre and ethical preference type.\n")

    with open(OUT_ROOT / "open_yoruba_coding_summary.md", "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "source_dirs": [str(path) for path in SOURCE_DIRS],
        "merged_records": len(rows),
    }
    with open(OUT_ROOT / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)

    print(OUT_ROOT)


if __name__ == "__main__":
    main()
