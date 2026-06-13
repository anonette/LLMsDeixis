#!/usr/bin/env python3
"""Merge open/unrestricted content coding for all four Yoruba models."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import MODELS, OPEN_CODED_DIRS, normalize_coded_model  # noqa: E402


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    ac.configure("open")
    ac.DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    source_map: dict[str, str] = {}

    for model in MODELS:
        coded_dir = OPEN_CODED_DIRS[model]
        if not coded_dir.exists():
            raise FileNotFoundError(f"Missing open coded dir for {model}: {coded_dir}")
        payload = load_json(coded_dir / "coded_content.json")
        source_map[model] = str(coded_dir)
        for row in payload["coded_records"]:
            item = dict(row)
            item["model"] = normalize_coded_model(item.get("model", model))
            rows.append(item)

    merged = {
        "generated_at": datetime.now().isoformat(),
        "condition": "open",
        "models": MODELS,
        "source_dirs": source_map,
        "records": rows,
    }
    with open(ac.MERGED_CODING_JSON, "w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=2, ensure_ascii=False)

    csv_path = ac.DATA_DIR / "open_four_model_coded_merged.csv"
    if rows:
        with open(csv_path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)

    print("\n=== Open four-model coding merge ===")
    for model in MODELS:
        subset = by_model[model]
        print(f"\n{model}: {len(subset)} records")
        print(f"  preferred_solution: {dict(Counter(r['preferred_solution'] for r in subset))}")
        print(f"  response_genre: {dict(Counter(r['response_genre'] for r in subset))}")
        print(f"  needs_review: {sum(1 for r in subset if r.get('needs_second_coder_review'))}")

    print(f"\nMerged JSON: {ac.MERGED_CODING_JSON}")
    print(f"Merged CSV:  {csv_path}")


if __name__ == "__main__":
    main()
