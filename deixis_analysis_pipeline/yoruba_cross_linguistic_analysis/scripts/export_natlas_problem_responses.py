#!/usr/bin/env python3
"""Export the problematic open N-ATLaS responses (uncodable, refuse-to-commit,
corrupted/garbled) with full Yoruba + English text, prompt, and coding rationale,
so the failure modes can be inspected by hand.

Writes: yoruba_cross_linguistic_analysis/NATLaS_Open_Problem_Responses.md
"""

from __future__ import annotations

import json
from pathlib import Path

ANALYSIS_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_ROOT = ANALYSIS_ROOT.parent

CODED = (
    PIPELINE_ROOT
    / "CONSOLIDATED_REPORTS/yoruba/natlas/yoruba_open_20260612/coded_content.json"
)
BILINGUAL_DIR = (
    PIPELINE_ROOT
    / "yoruba_deixis_module/outputs/bilingual_sessions"
    / "yoruba_control_natlas_20260612_125008_annotated_20260612_131914_bilingual_20260612_133303"
)
OUT = ANALYSIS_ROOT / "NATLaS_Open_Problem_Responses.md"


def load_bilingual():
    by_cell = {}
    for f in BILINGUAL_DIR.glob("*_bilingual.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        dil = data["dilemma_id"]
        for framing, entry in data.get("responses", {}).items():
            by_cell[(dil, framing)] = entry
    return by_cell


def categories(rec):
    cats = []
    if rec.get("preferred_solution") == "uncodable":
        cats.append("UNCODABLE")
    if rec.get("preferred_solution") == "refuses_to_commit":
        cats.append("REFUSES-TO-COMMIT")
    if rec.get("language_stability") == "corrupted_or_unusable":
        cats.append("CORRUPTED/GARBLED")
    return cats


def main():
    coded = json.loads(CODED.read_text(encoding="utf-8"))["coded_records"]
    bi = load_bilingual()

    buckets = {"UNCODABLE": [], "REFUSES-TO-COMMIT": [], "CORRUPTED/GARBLED": []}
    for rec in coded:
        for c in categories(rec):
            buckets[c].append(rec)

    lines = []
    lines.append("# N-ATLaS (open arm) — problematic responses for inspection")
    lines.append("")
    lines.append(
        "Full text of every open-arm N-ATLaS response flagged as **uncodable**, "
        "**refuses-to-commit**, or **corrupted/garbled**, so the failure modes can be read directly."
    )
    lines.append("")
    lines.append(f"- Source coding: `{CODED.relative_to(PIPELINE_ROOT)}`")
    lines.append(f"- Source text: `{BILINGUAL_DIR.relative_to(PIPELINE_ROOT)}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    for c, recs in buckets.items():
        lines.append(f"| {c} | {len(recs)} |")
    lines.append(
        f"| **distinct cells flagged** | "
        f"{len({(r['dilemma_id'], r['framing_type']) for recs in buckets.values() for r in recs})} |"
    )
    lines.append("")
    lines.append(
        "_Note: a cell can appear in more than one category (e.g. corrupted text is often "
        "also uncodable)._"
    )
    lines.append("")

    for cat, recs in buckets.items():
        lines.append("\n---\n")
        lines.append(f"# {cat}  ({len(recs)})")
        for rec in sorted(recs, key=lambda r: (r["dilemma_id"], r["framing_type"])):
            cell = (rec["dilemma_id"], rec["framing_type"])
            entry = bi.get(cell, {})
            also = [c for c in categories(rec) if c != cat]
            lines.append("")
            lines.append(f"## {rec['dilemma_id']} · {rec['framing_type']}")
            if also:
                lines.append(f"*Also flagged: {', '.join(also)}*")
            lines.append("")
            lines.append(
                f"- **preferred_solution:** {rec.get('preferred_solution')} · "
                f"**language_stability:** {rec.get('language_stability')} · "
                f"**genre:** {rec.get('response_genre')} · "
                f"**uptake:** {rec.get('deictic_uptake_quality')} · "
                f"**ethic:** {rec.get('ethical_preference_type')} · "
                f"**confidence:** {rec.get('confidence')}"
            )
            if rec.get("coding_rationale"):
                lines.append(f"- **coder rationale:** {rec['coding_rationale']}")
            if entry.get("audit_notes"):
                lines.append(f"- **audit notes:** {entry['audit_notes']}")
            if entry.get("normalization_notes"):
                lines.append(f"- **normalization notes:** {entry['normalization_notes']}")
            lines.append("")
            lines.append("**Prompt (YO):**")
            lines.append("")
            lines.append("> " + (entry.get("prompt_yo", "(prompt unavailable)") or "").replace("\n", "\n> "))
            lines.append("")
            lines.append("**Response (Yoruba):**")
            lines.append("")
            ry = (entry.get("response_yo") or "(no Yoruba text found)").strip()
            lines.append("```text")
            lines.append(ry)
            lines.append("```")
            lines.append("")
            lines.append("**Response (English translation):**")
            lines.append("")
            ren = (entry.get("response_en_academic") or "(no translation found)").strip()
            lines.append("> " + ren.replace("\n", "\n> "))
            lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    for c, recs in buckets.items():
        print(f"  {c}: {len(recs)}")


if __name__ == "__main__":
    main()
