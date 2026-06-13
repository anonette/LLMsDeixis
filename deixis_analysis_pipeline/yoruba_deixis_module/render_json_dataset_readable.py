#!/usr/bin/env python3
"""Render a UTF-8 JSON dataset into readable HTML and Markdown.

Designed for the Yoruba module datasets so that the outputs can be opened in a
browser or text editor without the encoding damage often introduced by Excel.
"""

from __future__ import annotations

import argparse
import json
import html
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


GROUP_ORDER = ["GPT-4o", "Claude 3.5 Sonnet", "DeepSeek"]
FRAMING_ORDER = [
    "impersonal",
    "second_person",
    "first_person",
    "first_person_plural",
    "reflexive",
    "dialogic",
    "spatial",
    "temporal",
    "cosmological",
]


def load_records(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    if isinstance(payload, list):
        return payload
    raise ValueError("Expected a JSON array or an object with a top-level 'records' list")


def sort_key(record: dict[str, Any]) -> tuple[int, int, str]:
    model = record.get("model_family", "")
    framing = record.get("framing_type", "")
    try:
        model_idx = GROUP_ORDER.index(model)
    except ValueError:
        model_idx = len(GROUP_ORDER)
    try:
        framing_idx = FRAMING_ORDER.index(framing)
    except ValueError:
        framing_idx = len(FRAMING_ORDER)
    return model_idx, framing_idx, framing


def safe(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def model_label(record: dict[str, Any]) -> str:
    family = safe(record.get("model_family"))
    if family:
        return family
    model = safe(record.get("model")).lower()
    if "deepseek" in model:
        return "DeepSeek"
    if "claude" in model:
        return "Claude 3.5 Sonnet"
    if "gpt" in model:
        return "GPT-4o"
    return "Unknown"


def is_control_comparison_record(record: dict[str, Any]) -> bool:
    return "control_response_yo" in record and "constrained_response_yo" in record


def framing_label(record: dict[str, Any]) -> str:
    return safe(record.get("framing_label") or record.get("framing_type"))


def render_html(records: list[dict[str, Any]], input_path: Path, output_path: Path, title: str) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in sorted(records, key=sort_key):
        grouped[model_label(record)].append(record)

    sections: list[str] = []
    for model in GROUP_ORDER + sorted(set(grouped) - set(GROUP_ORDER)):
        if model not in grouped:
            continue
        cards: list[str] = []
        for row in grouped[model]:
            prompt_yo = html.escape(safe(row.get("prompt_yo")))
            if is_control_comparison_record(row):
                control_yo = html.escape(safe(row.get("control_response_yo")))
                control_en = html.escape(safe(row.get("control_response_en_academic")))
                constrained_yo = html.escape(safe(row.get("constrained_response_yo")))
                constrained_en = html.escape(safe(row.get("constrained_response_en_academic")))
                cards.append(
                    f"""
                    <article class="card">
                      <div class="card-head">
                        <h3>{html.escape(framing_label(row))}</h3>
                        <div class="chips">
                          <span class="chip">Control: {html.escape(safe(row.get('control_response_length')))} chars</span>
                          <span class="chip chip-muted">Constrained: {html.escape(safe(row.get('constrained_response_length')))} chars</span>
                        </div>
                      </div>
                      <dl class="meta">
                        <div><dt>Length delta</dt><dd>{html.escape(safe(row.get('length_delta_control_minus_constrained')))}</dd></div>
                        <div><dt>Control session</dt><dd>{html.escape(safe(row.get('control_source_session')))}</dd></div>
                        <div><dt>Constrained session</dt><dd>{html.escape(safe(row.get('constrained_source_session')))}</dd></div>
                        <div><dt>Dilemma</dt><dd>{html.escape(safe(row.get('dilemma_id')))}</dd></div>
                      </dl>
                      <section>
                        <h4>Yoruba Prompt</h4>
                        <p>{prompt_yo}</p>
                      </section>
                      <section>
                        <h4>Control Yoruba</h4>
                        <p>{control_yo}</p>
                      </section>
                      <section>
                        <h4>Constrained Yoruba</h4>
                        <p>{constrained_yo}</p>
                      </section>
                      <section>
                        <h4>Control English Translation</h4>
                        <p>{control_en}</p>
                      </section>
                      <section>
                        <h4>Constrained English Translation</h4>
                        <p>{constrained_en}</p>
                      </section>
                    </article>
                    """
                )
            else:
                response_yo = html.escape(safe(row.get("response_yo")))
                response_en = html.escape(safe(row.get("response_en_academic")))
                baseline_en = html.escape(safe(row.get("baseline_response_en")))
                residual = html.escape(safe(row.get("residual_deictic_note")))
                subtype = html.escape(safe(row.get("impersonal_subtype")))
                cards.append(
                    f"""
                    <article class="card">
                      <div class="card-head">
                        <h3>{html.escape(framing_label(row))}</h3>
                        <div class="chips">
                          <span class="chip">Yoruba: {html.escape(safe(row.get('decision_yoruba')))}</span>
                          <span class="chip chip-muted">English: {html.escape(safe(row.get('decision_english')))}</span>
                        </div>
                      </div>
                      <dl class="meta">
                        <div><dt>Method condition</dt><dd>{html.escape(safe(row.get('methodological_condition')))}</dd></div>
                        <div><dt>Impersonal subtype</dt><dd>{subtype or '&nbsp;'}</dd></div>
                        <div><dt>Retry attempts</dt><dd>{html.escape(safe(row.get('retry_attempts_used')))}</dd></div>
                        <div><dt>Stop artifact</dt><dd>{html.escape(safe(row.get('contains_stop_artifact')))}</dd></div>
                      </dl>
                      <section>
                        <h4>Yoruba Prompt</h4>
                        <p>{prompt_yo}</p>
                      </section>
                      <section>
                        <h4>Yoruba Response</h4>
                        <p>{response_yo}</p>
                      </section>
                      <section>
                        <h4>Academic English Translation</h4>
                        <p>{response_en}</p>
                      </section>
                      <section>
                        <h4>Published English Baseline</h4>
                        <p>{baseline_en}</p>
                      </section>
                      {f'<section><h4>Residual Deictic Note</h4><p>{residual}</p></section>' if residual else ''}
                    </article>
                    """
                )
        sections.append(f"<section class=\"model-block\"><h2>{html.escape(model)}</h2>{''.join(cards)}</section>")

    html_text = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 0;
      background: #f5f4f0;
      color: #181818;
      font: 16px/1.55 Georgia, "Times New Roman", serif;
    }}
    .page {{
      width: min(1200px, calc(100vw - 32px));
      margin: 24px auto;
      background: #fffdfa;
      border: 1px solid #d6d0c7;
      padding: 32px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }}
    h1, h2, h3, h4 {{ line-height: 1.2; }}
    h1 {{ margin: 0 0 8px; font-size: 32px; }}
    h2 {{ margin: 32px 0 14px; padding-top: 10px; border-top: 2px solid #d6d0c7; color: #6a3a10; }}
    h3 {{ margin: 0; font-size: 22px; }}
    h4 {{ margin: 14px 0 6px; font-size: 15px; color: #21546d; }}
    p {{ margin: 0 0 10px; white-space: pre-wrap; }}
    .lede {{ color: #5d5a54; margin-bottom: 18px; }}
    .model-block {{ display: block; }}
    .card {{ border: 1px solid #ddd5ca; background: #fff; padding: 18px; margin: 0 0 18px; }}
    .card-head {{ display: flex; justify-content: space-between; gap: 16px; align-items: start; margin-bottom: 10px; }}
    .chips {{ text-align: right; }}
    .chip {{ display: inline-block; border: 1px solid #c9bba8; border-radius: 999px; padding: 3px 9px; font-size: 12px; margin: 0 0 6px 6px; background: #f8f1e7; }}
    .chip-muted {{ background: #eef3f5; border-color: #bfd0d7; }}
    .meta {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin: 0 0 12px; }}
    .meta dt {{ font-size: 12px; text-transform: uppercase; color: #6b665f; letter-spacing: 0.04em; }}
    .meta dd {{ margin: 2px 0 0; font-size: 14px; }}
    code {{ font-family: Consolas, "Courier New", monospace; }}
    @media (max-width: 900px) {{
      .page {{ padding: 20px; }}
      .card-head {{ display: block; }}
      .chips {{ text-align: left; margin-top: 10px; }}
      .meta {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media print {{
      body {{ background: #fff; }}
      .page {{ width: auto; margin: 0; border: 0; box-shadow: none; }}
      .card {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <h1>{html.escape(title)}</h1>
    <p class="lede">UTF-8-safe readable export generated from <code>{html.escape(str(input_path))}</code>. Open this file in a browser to review Yoruba text without spreadsheet encoding damage.</p>
    {''.join(sections)}
  </main>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(html_text)


def render_markdown(records: list[dict[str, Any]], input_path: Path, output_path: Path, title: str) -> None:
    lines: list[str] = [
        f"# {title}",
        "",
        f"Source JSON: `{input_path}`",
        "",
        "UTF-8-safe readable export. View this file in a UTF-8-aware editor or open the companion HTML in a browser.",
        "",
    ]

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in sorted(records, key=sort_key):
        grouped[model_label(record)].append(record)

    for model in GROUP_ORDER + sorted(set(grouped) - set(GROUP_ORDER)):
        if model not in grouped:
            continue
        lines.extend([f"## {model}", ""])
        for row in grouped[model]:
            if is_control_comparison_record(row):
                lines.extend(
                    [
                        f"### {framing_label(row)}",
                        "",
                        f"- Control length: `{safe(row.get('control_response_length'))}`",
                        f"- Constrained length: `{safe(row.get('constrained_response_length'))}`",
                        f"- Length delta: `{safe(row.get('length_delta_control_minus_constrained'))}`",
                        "",
                        "**Yoruba Prompt**",
                        "",
                        safe(row.get("prompt_yo")),
                        "",
                        "**Control Yoruba**",
                        "",
                        safe(row.get("control_response_yo")),
                        "",
                        "**Constrained Yoruba**",
                        "",
                        safe(row.get("constrained_response_yo")),
                        "",
                        "**Control English Translation**",
                        "",
                        safe(row.get("control_response_en_academic")),
                        "",
                        "**Constrained English Translation**",
                        "",
                        safe(row.get("constrained_response_en_academic")),
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"### {framing_label(row)}",
                        "",
                        f"- Yoruba decision: `{safe(row.get('decision_yoruba'))}`",
                        f"- English decision: `{safe(row.get('decision_english'))}`",
                        f"- Methodological condition: `{safe(row.get('methodological_condition'))}`",
                        f"- Impersonal subtype: `{safe(row.get('impersonal_subtype'))}`",
                        f"- Retry attempts: `{safe(row.get('retry_attempts_used'))}`",
                        "",
                        "**Yoruba Prompt**",
                        "",
                        safe(row.get("prompt_yo")),
                        "",
                        "**Yoruba Response**",
                        "",
                        safe(row.get("response_yo")),
                        "",
                        "**Academic English Translation**",
                        "",
                        safe(row.get("response_en_academic")),
                        "",
                        "**Published English Baseline**",
                        "",
                        safe(row.get("baseline_response_en")),
                        "",
                    ]
                )
                residual = safe(row.get("residual_deictic_note"))
                if residual:
                    lines.extend(["**Residual Deictic Note**", "", residual, ""])

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a UTF-8 JSON dataset into readable HTML and Markdown")
    parser.add_argument("input_json", help="Path to the source JSON dataset")
    parser.add_argument("--title", default=None, help="Document title override")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: next to input JSON)")
    args = parser.parse_args()

    input_path = Path(args.input_json).resolve()
    records = load_records(input_path)

    title = args.title or f"Readable Export: {input_path.stem}"
    output_dir = Path(args.output_dir).resolve() if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = output_dir / f"{input_path.stem}_readable_{stamp}.html"
    md_path = output_dir / f"{input_path.stem}_readable_{stamp}.md"

    render_html(records, input_path, html_path, title)
    render_markdown(records, input_path, md_path, title)

    print(f"HTML: {html_path}")
    print(f"Markdown: {md_path}")


if __name__ == "__main__":
    main()
