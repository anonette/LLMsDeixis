"""Annotate a generation session with the methodological_typology metadata
from the Yoruba prompt JSON.

For each cell (dilemma_id × framing_type), adds:

- `methodological_condition`: the framing as the article reports it
  (impersonal, second_person, ...)
- `impersonal_subtype`: only for impersonal cells; one of
  `bare_perfective`, `progressive_background`,
  `double_progressive_irreducible`, `bare_perfective_with_habitual`,
  `existential_stative_restructured`. Otherwise null.
- `residual_deictic_note`: for non-impersonal cells where the prompt JSON
  records a residual deictic encoding feature; otherwise null.

The annotator writes a new directory next to the source session with the
same response files plus the new fields, and a `typology_summary.json`
counting cells per subtype.

Usage:
    python annotate_session_typology.py <session_dir>
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict


def load_typology() -> dict:
    here = Path(__file__).resolve().parent
    prompt_path = here.parent / "input_questions" / "all_dilemmas_deictic_questions_yoruba.json"
    with open(prompt_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["methodological_typology"]


def detect_schema(data: dict):
    if "responses" in data and isinstance(data["responses"], dict):
        return "nested", data["responses"]
    return "flat", data


def main() -> int:
    parser = argparse.ArgumentParser(description="Annotate a session with methodological typology")
    parser.add_argument("session_dir", help="Path to source session directory")
    args = parser.parse_args()

    session_dir = Path(args.session_dir).resolve()
    if not session_dir.exists():
        print(f"Session not found: {session_dir}")
        return 1

    typology = load_typology()
    impersonal_subtype = typology["impersonal_subtype_by_dilemma"]
    residual_notes = typology["residual_deictic_encoding_outside_impersonal"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = session_dir.parent / f"{session_dir.name}_annotated_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    counts: Dict[str, int] = {}

    for response_file in sorted(session_dir.glob("*_responses.json")):
        dilemma_id = response_file.stem.replace("_responses", "")
        with open(response_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        schema, responses = detect_schema(data)

        for framing, payload in responses.items():
            if not isinstance(payload, dict):
                continue
            payload["methodological_condition"] = framing
            if framing == "impersonal":
                subtype = impersonal_subtype.get(dilemma_id)
                payload["impersonal_subtype"] = subtype
                key = f"impersonal:{subtype}" if subtype else "impersonal:unknown"
                counts[key] = counts.get(key, 0) + 1
            else:
                payload["impersonal_subtype"] = None
                payload["residual_deictic_note"] = residual_notes.get(framing)
                counts[framing] = counts.get(framing, 0) + 1

        out_path = out_dir / response_file.name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    summary = {
        "source_session": session_dir.name,
        "annotated_at": datetime.now().isoformat(),
        "cells_by_condition": counts,
        "impersonal_subtype_by_dilemma": impersonal_subtype,
        "residual_deictic_encoding_outside_impersonal": residual_notes,
        "rationale": typology["rationale"],
        "analysis_recommendations": typology["analysis_recommendations"],
    }
    with open(out_dir / "typology_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Annotated session written to: {out_dir}")
    print(f"Cell counts by condition:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
