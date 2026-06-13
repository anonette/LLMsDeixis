#!/usr/bin/env python3
"""Merge constrained-arm content coding for all four Yoruba models."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analysis_config import (  # noqa: E402
    CODED_DIR,
    CONSTRAINED_BILINGUAL_SESSIONS,
    DATA_DIR,
    MERGED_CODING_JSON,
    MODELS,
    NATLAS_CONSTRAINED_CODED,
    normalize_coded_model,
)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def find_latest_coded_dir(bilingual_dir: Path) -> Path | None:
    prefix = f"{bilingual_dir.name}_coded_"
    matches = sorted(
        [p for p in CODED_DIR.iterdir() if p.is_dir() and p.name.startswith(prefix)],
        key=lambda p: p.name,
    )
    return matches[-1] if matches else None


def ensure_coded(bilingual_dir: Path, model_key: str) -> Path:
    existing = find_latest_coded_dir(bilingual_dir)
    if existing and (existing / "coded_content.json").exists():
        print(f"[skip coding] {model_key}: {existing.name}")
        return existing

    print(f"[coding] {model_key} from {bilingual_dir.name} ...")
    coding_agent = SCRIPT_DIR.parent.parent / "yoruba_deixis_module" / "yoruba_content_coding_agent.py"
    subprocess.run(
        [
            sys.executable,
            str(coding_agent),
            str(bilingual_dir),
            "--coding-model",
            "claude-3.5-sonnet",
            "--output-dir",
            str(CODED_DIR),
        ],
        check=True,
    )
    coded = find_latest_coded_dir(bilingual_dir)
    if coded is None:
        raise FileNotFoundError(f"No coded output found after coding {bilingual_dir}")
    return coded


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    source_map: dict[str, str] = {}

    for model in MODELS:
        if model == "n-atlas":
            coded_dir = NATLAS_CONSTRAINED_CODED
        else:
            bilingual_dir = CONSTRAINED_BILINGUAL_SESSIONS[model]
            if not bilingual_dir.exists():
                raise FileNotFoundError(f"Missing bilingual session: {bilingual_dir}")
            coded_dir = ensure_coded(bilingual_dir, model)

        payload = load_json(coded_dir / "coded_content.json")
        source_map[model] = str(coded_dir)
        for row in payload["coded_records"]:
            item = dict(row)
            item["model"] = normalize_coded_model(item.get("model", model))
            rows.append(item)

    merged = {
        "generated_at": datetime.now().isoformat(),
        "condition": "constrained",
        "models": MODELS,
        "source_dirs": source_map,
        "records": rows,
    }
    with open(MERGED_CODING_JSON, "w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=2, ensure_ascii=False)

    csv_path = DATA_DIR / "constrained_four_model_coded_merged.csv"
    if rows:
        with open(csv_path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)

    print("\n=== Constrained four-model coding merge ===")
    for model in MODELS:
        subset = by_model[model]
        print(f"\n{model}: {len(subset)} records")
        print(f"  preferred_solution: {dict(Counter(r['preferred_solution'] for r in subset))}")
        print(f"  response_genre: {dict(Counter(r['response_genre'] for r in subset))}")
        print(f"  needs_review: {sum(1 for r in subset if r.get('needs_second_coder_review'))}")

    print(f"\nMerged JSON: {MERGED_CODING_JSON}")
    print(f"Merged CSV:  {csv_path}")


if __name__ == "__main__":
    main()
