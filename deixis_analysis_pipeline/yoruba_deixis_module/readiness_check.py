"""Quick readiness check for the Yoruba deixis module.

Verifies that:
1. Environment variables are loaded.
2. The Yoruba prompt inventory is present and well-formed.
3. Per-model Yoruba instructions exist.
4. The published English baseline manifest is present.
5. All module scripts are on disk.
6. The currently validated clean sessions still validate cleanly.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# bootstrap repo root onto sys.path so we can import env_config + validator
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from env_config import load_project_env  # noqa: E402

load_project_env()

sys.path.insert(0, str(Path(__file__).parent))
from yoruba_validator import score_session, summarize  # noqa: E402


REPO = REPO_ROOT
PIPELINE = REPO / "deixis_analysis_pipeline"
MODULE = PIPELINE / "yoruba_deixis_module"
GEN_LOGS = PIPELINE / "generation_logs"
INPUTS = PIPELINE / "input_questions"


def hr() -> None:
    print("=" * 60)


def section(title: str) -> None:
    print()
    print(title)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    hr()
    print("YORUBA DEIXIS MODULE - READINESS CHECK")
    hr()

    ok = True

    # 1. Environment variables
    section("1. Environment variables:")
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        present = bool(os.getenv(key))
        print(f"   {key}: {'OK' if present else 'MISSING'}")
        ok &= present

    # 2. Yoruba prompt inventory
    section("2. Yoruba prompt inventory:")
    prompt_path = INPUTS / "all_dilemmas_deictic_questions_yoruba.json"
    if not prompt_path.exists():
        print(f"   MISSING: {prompt_path.name}")
        ok = False
    else:
        data = json.loads(prompt_path.read_text(encoding="utf-8"))
        print(f"   File: {prompt_path.name}")
        print(f"   Dilemmas: {len(data['dilemmas'])}")
        for d in data["dilemmas"]:
            framings = list(d["deictic_questions"].keys())
            print(f"     - {d['dilemma_id']}: {len(framings)} framings")
        # methodological_typology block
        typology = data.get("methodological_typology")
        if not typology:
            print("   MISSING: methodological_typology block")
            ok = False
        else:
            subtypes = typology.get("impersonal_subtype_by_dilemma", {})
            residuals = typology.get("residual_deictic_encoding_outside_impersonal", {})
            print(f"   methodological_typology: {len(subtypes)} impersonal subtypes, "
                  f"{len(residuals)} residual-encoding notes")

    # 3. Per-model instructions
    section("3. Per-model Yoruba instructions:")
    instr_path = MODULE / "model_response_instructions.json"
    if not instr_path.exists():
        print(f"   MISSING: {instr_path.name}")
        ok = False
    else:
        cfg = json.loads(instr_path.read_text(encoding="utf-8"))
        for k, v in cfg["model_response_instructions"].items():
            print(f"   {k}: {len(v)} chars")

    # 4. Published English baseline manifest
    section("4. Published English baseline manifest:")
    base_path = MODULE / "published_english_baseline.json"
    if not base_path.exists():
        print(f"   MISSING: {base_path.name}")
        ok = False
    else:
        m = json.loads(base_path.read_text(encoding="utf-8"))
        for model_name, info in m["models"].items():
            tag = "same" if info.get("same_model_as_baseline") else "substitute"
            print(
                f"   {model_name}: english={info['session']} | "
                f"yoruba={info['yoruba_model']} ({tag})"
            )

    # 5. Module scripts on disk
    section("5. Module scripts:")
    scripts = [
        "run_yoruba_generation_all.py",
        "yoruba_validator.py",
        "retry_dirty_responses.py",
        "annotate_session_typology.py",
        "translate_yoruba_session.py",
        "compare_yoruba_to_published_english.py",
        "run_yoruba_postprocessing_all.py",
    ]
    for script in scripts:
        path = MODULE / script
        present = path.exists()
        print(f"   {script}: {'OK' if present else 'MISSING'}")
        ok &= present

    # 6. Previously validated clean sessions
    section("6. Validated clean sessions on disk:")
    sessions = [
        "yoruba_gpt4o_20260528_194240_cleaned_20260529_102820",
        "yoruba_claude_pilot_20260529_083434",
        "yoruba_deepseek_pilot7_20260529_094618_cleaned_20260529_100259",
    ]
    for name in sessions:
        path = GEN_LOGS / name
        if not path.exists():
            print(f"   {name}: NOT FOUND")
            continue
        results = score_session(path)
        summary = summarize(results)
        clean = summary["clean"]
        total = summary["total"]
        status = "OK" if clean == total else f"REGRESSED ({clean}/{total})"
        print(f"   {name}: {clean}/{total} clean ({status})")

    print()
    hr()
    print("READY TO RUN" if ok else "ISSUES DETECTED - see above")
    hr()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
