#!/usr/bin/env python3
"""Post-process a constrained N-ATLaS Yoruba generation session (same steps as cloud models)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parent
PIPELINE_DIR = MODULE_DIR.parent
GENERATION_SCRIPTS = PIPELINE_DIR / "generation_scripts"
DEFAULT_SESSION = PIPELINE_DIR / "generation_logs" / "yoruba_natlas_20260612_113301"
CONSOLIDATED_ROOT = PIPELINE_DIR / "CONSOLIDATED_REPORTS" / "yoruba" / "natlas"


def run(command: list[str], description: str) -> None:
    print(f"\n[RUN] {description}")
    print("=" * 72)
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(command, cwd=str(REPO_ROOT), capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"{description} failed (exit {result.returncode})")


def retry_short_cells(session_dir: Path, min_length: int = 150) -> Path:
    """Regenerate cells shorter than min_length via remote Ollama."""
    sys.path.insert(0, str(GENERATION_SCRIPTS))
    from generate_responses_natlas import (  # noqa: WPS433
        OllamaClient,
        build_generation_prompt,
        load_all_dilemmas_questions,
    )
    from session_utils import iterate_response_records  # noqa: WPS433

    cfg_path = MODULE_DIR / "model_response_instructions.json"
    with open(cfg_path, "r", encoding="utf-8") as handle:
        instruction = json.load(handle)["model_response_instructions"]["n-atlas"]

    prompt_path = PIPELINE_DIR / "input_questions" / "all_dilemmas_deictic_questions_yoruba.json"
    prompt_lookup = {
        (d["dilemma_id"], framing): data["question"]
        for d in load_all_dilemmas_questions(str(prompt_path))["dilemmas"]
        for framing, data in d["deictic_questions"].items()
    }

    client = OllamaClient(host="http://100.111.129.69:12434", model="n-atlas")
    retried = []
    for record in iterate_response_records(session_dir):
        text = record.get("response") or ""
        if len(text) >= min_length:
            continue
        dilemma_id = record["dilemma_id"]
        framing = record["framing_type"]
        question = prompt_lookup[(dilemma_id, framing)]
        prompt = build_generation_prompt(question, instruction)
        new_text, meta = client.generate(prompt)
        response_file = session_dir / f"{dilemma_id}_responses.json"
        with open(response_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        cell = data["responses"][framing]
        cell["response"] = new_text
        cell["response_length"] = len(new_text)
        cell["retry_reason"] = f"short_response<{min_length}"
        cell["retry_meta"] = meta
        cell["retry_timestamp"] = datetime.now().isoformat()
        with open(response_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
        print(f"  retried {dilemma_id}/{framing}: {len(text)} -> {len(new_text)} chars")
        retried.append((dilemma_id, framing, len(text), len(new_text)))

    if retried:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        cleaned = session_dir.parent / f"{session_dir.name}_cleaned_{ts}"
        shutil.copytree(session_dir, cleaned)
        summary = {"retried_short_cells": retried, "min_length": min_length}
        with open(cleaned / "retry_summary.json", "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)
        return cleaned
    return session_dir


def latest_child(parent: Path, prefix: str) -> Path:
    matches = sorted(
        [p for p in parent.iterdir() if p.is_dir() and p.name.startswith(prefix)],
        key=lambda p: p.name,
    )
    if not matches:
        raise FileNotFoundError(f"No directory matching {prefix} under {parent}")
    return matches[-1]


def find_comparison_dir(bilingual_dir: Path) -> Path | None:
    comparisons_root = MODULE_DIR / "outputs" / "comparisons"
    matches = []
    for candidate in comparisons_root.iterdir():
        if not candidate.is_dir():
            continue
        summary_path = candidate / "comparison_summary.json"
        if not summary_path.exists():
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("yoruba_source_session") == bilingual_dir.name:
            matches.append(candidate)
    if not matches:
        return None
    return sorted(matches, key=lambda p: p.name)[-1]


def package_consolidated(
    session_dir: Path,
    bilingual_dir: Path,
    comparison_dir: Path | None,
    coded_dir: Path,
    package_name: str,
) -> Path:
    target = CONSOLIDATED_ROOT / package_name
    target.mkdir(parents=True, exist_ok=True)
    for name in ("coded_content.json", "coded_content.csv", "coding_summary.json"):
        shutil.copy2(coded_dir / name, target / name)
    if comparison_dir:
        for name in ("paired_comparison.json", "paired_comparison.csv", "comparison_summary.json"):
            src = comparison_dir / name
            if src.exists():
                shutil.copy2(src, target / name)
    condition = "open" if "open" in package_name else "constrained"
    if condition == "open":
        readme = f"""# N-ATLaS Yoruba Open Control Condition

Package: `{package_name}`

## Prompt condition

**Open / unrestricted** — same as `yoruba_control_gpt4o`, `yoruba_control_claude`, `yoruba_control_deepseek`.

Each cell used the Yoruba dilemma prompt only. No response-shaping instruction was prepended.

## Source sessions

- Generation: `{session_dir.name}`
- Bilingual: `{bilingual_dir.name}`
- Coding: `{coded_dir.name}`
"""
    else:
        readme = f"""# N-ATLaS Yoruba Constrained Condition

Package: `{package_name}`

## Prompt condition

**Closed / constrained** — same as the main Yoruba cloud-model runs (`yoruba_gpt4o`, `yoruba_claude`, `yoruba_deepseek`).

Each cell used the `n-atlas` entry from `model_response_instructions.json` (Yoruba-only + `Ìpinnu mi: ... Ìdí: ...` format).

This is **not** the unrestricted open control (`yoruba_control_*`), which omits the instruction layer.

## Source sessions

- Generation: `{session_dir.name}`
- Bilingual: `{bilingual_dir.name}`
- Coding: `{coded_dir.name}`
"""
    if comparison_dir:
        readme += f"- English pairing (structural reference only): `{comparison_dir.name}`\n"
        readme += "\nN-ATLaS has no published English baseline. `paired_comparison.json` pairs Yoruba responses with **GPT-4o English** from the article baseline for row alignment only — not same-model replication.\n"
    (target / "README.md").write_text(readme, encoding="utf-8")
    return target


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Post-process N-ATLaS Yoruba session")
    parser.add_argument("session_dir", nargs="?", default=str(DEFAULT_SESSION))
    parser.add_argument("--skip-retry", action="store_true")
    parser.add_argument("--skip-translate", action="store_true")
    parser.add_argument("--skip-compare", action="store_true")
    parser.add_argument("--skip-code", action="store_true")
    parser.add_argument(
        "--open-control",
        action="store_true",
        help="Package as unrestricted open Yoruba control (skip retry; open README text)",
    )
    parser.add_argument(
        "--translation-model",
        default="claude-3.5-sonnet",
        help="Model for academic English translation",
    )
    parser.add_argument(
        "--coding-model",
        default="claude-3.5-sonnet",
        help="Model for content coding",
    )
    parser.add_argument("--skip-annotate", action="store_true")
    args = parser.parse_args()

    session_dir = Path(args.session_dir)
    if not session_dir.is_absolute():
        session_dir = REPO_ROOT / session_dir

    if not args.skip_retry and not args.open_control:
        session_dir = retry_short_cells(session_dir)

    if not args.skip_annotate:
        run(
            [sys.executable, str(MODULE_DIR / "annotate_session_typology.py"), str(session_dir)],
            f"Annotate typology: {session_dir.name}",
        )
        annotated_dir = latest_child(session_dir.parent, f"{session_dir.name}_annotated_")
    else:
        annotated_dir = session_dir

    bilingual_dir = None
    if not args.skip_translate:
        run(
            [
                sys.executable,
                str(MODULE_DIR / "translate_yoruba_session.py"),
                str(annotated_dir),
                "--translation-model",
                args.translation_model,
            ],
            f"Translate: {annotated_dir.name}",
        )
        bilingual_dir = latest_child(MODULE_DIR / "outputs" / "bilingual_sessions", f"{annotated_dir.name}_bilingual_")

    comparison_dir = None
    if bilingual_dir and not args.skip_compare:
        run(
            [
                sys.executable,
                str(MODULE_DIR / "compare_yoruba_to_published_english.py"),
                str(bilingual_dir),
                "--baseline-model-key",
                "GPT-4o",
            ],
            f"Pair with published English (GPT-4o reference): {bilingual_dir.name}",
        )
        comparison_dir = find_comparison_dir(bilingual_dir)

    coded_dir = None
    if bilingual_dir and not args.skip_code:
        run(
            [
                sys.executable,
                str(MODULE_DIR / "yoruba_content_coding_agent.py"),
                str(bilingual_dir),
                "--coding-model",
                args.coding_model,
            ],
            f"Content coding: {bilingual_dir.name}",
        )
        coded_dir = latest_child(MODULE_DIR / "outputs" / "coded_content", f"{bilingual_dir.name}_coded_")

    if coded_dir and bilingual_dir:
        package = package_consolidated(
            session_dir,
            bilingual_dir,
            comparison_dir,
            coded_dir,
            f"yoruba_{'open' if args.open_control else 'constrained'}_{datetime.now().strftime('%Y%m%d')}",
        )
        print(f"\n[DONE] Consolidated package: {package}")

    print("\n[DONE] N-ATLaS post-processing complete.")


if __name__ == "__main__":
    main()
