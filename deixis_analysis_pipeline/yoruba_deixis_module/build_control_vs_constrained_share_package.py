#!/usr/bin/env python3
"""Build a share package for unrestricted-vs-constrained Yoruba comparisons."""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = MODULE_DIR / "outputs"
COMPARE_ROOT = OUTPUT_ROOT / "control_vs_constrained"

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

FRAMING_LABELS = {
    "impersonal": "Impersonal",
    "second_person": "2nd Person",
    "first_person": "1st Person",
    "first_person_plural": "1st Plural",
    "reflexive": "Reflexive",
    "dialogic": "Dialogic",
    "spatial": "Spatial",
    "temporal": "Temporal",
    "cosmological": "Cosmological",
}

TARGET_DIRS = [
    COMPARE_ROOT / "gpt-4o_control_vs_constrained_20260529_192513",
    COMPARE_ROOT / "anthropic_claude-35-sonnet_control_vs_constrained_20260529_192513",
    COMPARE_ROOT / "deepseek_deepseek-chat_control_vs_constrained_20260529_192513",
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


def load_records() -> list[dict]:
    rows = []
    for directory in TARGET_DIRS:
        payload = load_json(directory / "paired_control_vs_constrained.json")
        model_label = normalize_model(payload["model"])
        for record in payload["paired_records"]:
            row = dict(record)
            row["model_label"] = model_label
            row["control_has_english_markers"] = any(
                marker in row["control_response_yo"]
                for marker in ["###", "Translation:", "English", "Utilitarian", "Deontological", "Trolley Problem"]
            )
            row["control_multiline"] = row["control_response_yo"].count("\n") >= 3
            rows.append(row)
    return rows


def write_dataset(rows: list[dict], out_dir: Path) -> None:
    dataset_dir = out_dir / "dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    json_path = dataset_dir / "control_vs_constrained_dataset.json"
    csv_path = dataset_dir / "control_vs_constrained_dataset.csv"

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump({"records": rows, "generated_at": datetime.now().isoformat()}, handle, indent=2, ensure_ascii=False)

    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def render_mean_length_chart(rows: list[dict], out_path: Path) -> None:
    models = ["GPT-4o", "Claude", "DeepSeek"]
    control_means = []
    constrained_means = []
    for model in models:
        subset = [r for r in rows if r["model_label"] == model]
        control_means.append(mean(r["control_response_length"] for r in subset))
        constrained_means.append(mean(r["constrained_response_length"] for r in subset))

    x = range(len(models))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.bar([i - width / 2 for i in x], control_means, width=width, label="Unrestricted control", color="#8b5a2b")
    ax.bar([i + width / 2 for i in x], constrained_means, width=width, label="Constrained Yoruba", color="#1f6f8b")
    ax.set_xticks(list(x))
    ax.set_xticklabels(models)
    ax.set_ylabel("Mean Yoruba response length")
    ax.set_title("Control vs Constrained Response Length")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_delta_chart(rows: list[dict], out_path: Path) -> None:
    models = ["GPT-4o", "Claude", "DeepSeek"]
    deltas = []
    for model in models:
        subset = [r for r in rows if r["model_label"] == model]
        deltas.append(mean(r["length_delta_control_minus_constrained"] for r in subset))

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    bars = ax.bar(models, deltas, color=["#7b3f00", "#5f8a8b", "#b84a62"])
    ax.set_ylabel("Mean length delta")
    ax.set_title("How Much Longer The Unrestricted Control Becomes")
    for bar, val in zip(bars, deltas):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20, f"{val:.0f}", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_framing_chart(rows: list[dict], out_path: Path) -> None:
    models = ["GPT-4o", "Claude", "DeepSeek"]
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for ax, model in zip(axes, models):
        subset = [r for r in rows if r["model_label"] == model]
        ordered = sorted(subset, key=lambda r: FRAMING_ORDER.index(r["framing_type"]))
        vals = [r["length_delta_control_minus_constrained"] for r in ordered]
        labels = [FRAMING_LABELS[r["framing_type"]] for r in ordered]
        ax.bar(labels, vals, color="#6c757d")
        ax.set_title(model)
        ax.set_ylabel("Delta")
        ax.tick_params(axis="x", rotation=35)
    axes[0].set_title("Length Expansion By Framing")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_handout(rows: list[dict], out_dir: Path) -> Path:
    models = ["GPT-4o", "Claude", "DeepSeek"]
    cards = []
    for model in models:
        subset = [r for r in rows if r["model_label"] == model]
        mean_control = mean(r["control_response_length"] for r in subset)
        mean_constrained = mean(r["constrained_response_length"] for r in subset)
        mean_delta = mean(r["length_delta_control_minus_constrained"] for r in subset)
        english_markers = sum(1 for r in subset if r["control_has_english_markers"])
        longest = max(subset, key=lambda r: r["length_delta_control_minus_constrained"])
        cards.append(
            f"""
            <section class="card">
              <h3>{model}</h3>
              <p><strong>Mean control length:</strong> {mean_control:.1f}</p>
              <p><strong>Mean constrained length:</strong> {mean_constrained:.1f}</p>
              <p><strong>Mean delta:</strong> +{mean_delta:.1f}</p>
              <p><strong>Control cells with obvious English/framework markers:</strong> {english_markers}/9</p>
              <p><strong>Largest framing jump:</strong> {FRAMING_LABELS[longest['framing_type']]} (+{longest['length_delta_control_minus_constrained']})</p>
            </section>
            """
        )

    html_text = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Control vs Constrained Yoruba Handout</title>
  <style>
    body {{ margin: 0; background: #f3efe8; color: #181818; font: 16px/1.55 Georgia, serif; }}
    .page {{ width: min(1100px, calc(100vw - 32px)); margin: 24px auto; background: #fffdfa; border: 1px solid #d7d0c6; box-shadow: 0 8px 24px rgba(0,0,0,0.08); padding: 38px 42px 48px; }}
    h1, h2, h3 {{ line-height: 1.2; }}
    h1 {{ margin: 0 0 10px; font-size: 34px; }}
    h2 {{ margin-top: 32px; padding-top: 10px; border-top: 2px solid #d7d0c6; color: #6d3d14; }}
    .lede {{ color: #5e5952; font-size: 18px; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 20px; }}
    .stat {{ border: 1px solid #d7d0c6; background: #faf6ef; padding: 14px; }}
    .stat .n {{ font-size: 24px; font-weight: bold; }}
    .cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 18px; }}
    .card {{ border: 1px solid #d7d0c6; background: #fff; padding: 16px; }}
    figure {{ margin: 18px 0; border: 1px solid #d7d0c6; background: #fff; padding: 12px; }}
    img {{ width: 100%; height: auto; display: block; }}
    figcaption {{ margin-top: 8px; color: #5e5952; font-size: 14px; }}
    .mono {{ font-family: Consolas, monospace; }}
    ul {{ padding-left: 20px; }}
    @media (max-width: 900px) {{ .summary, .cards {{ grid-template-columns: 1fr; }} .page {{ padding: 22px; }} }}
    @media print {{ body {{ background: #fff; }} .page {{ width: auto; margin: 0; border: 0; box-shadow: none; }} }}
  </style>
</head>
<body>
  <main class="page">
    <h1>Control vs Constrained Yoruba Handout</h1>
    <p class="lede">This handout compares the unrestricted Yoruba control pilot against the previous constrained Yoruba trolley calibration. The result is clear: removing the response restrictions produces much longer, more expository, and often more mixed-language outputs.</p>

    <section class="summary">
      <div class="stat"><div>Models</div><div class="n">3</div></div>
      <div class="stat"><div>Paired cells</div><div class="n">27</div></div>
      <div class="stat"><div>Largest mean jump</div><div class="n">+2983</div></div>
      <div class="stat"><div>Most expanded model</div><div class="n">DeepSeek</div></div>
    </section>

    <h2>Main Findings</h2>
    <ul>
      <li>The unrestricted control is longer for all three models across the trolley problem framings.</li>
      <li>GPT-4o expands from terse verdicts into ethics-explanation prose, averaging +1081.7 characters.</li>
      <li>Claude also expands, but less dramatically, averaging +353.4 characters.</li>
      <li>DeepSeek expands the most, averaging +2982.7 characters, with multiple cells reverting into English-heavy or translation-like exposition.</li>
      <li>The restriction layer therefore explains a large share of the brevity and decisional compression seen in the main Yoruba run.</li>
    </ul>

    <h2>By Model</h2>
    <div class="cards">{''.join(cards)}</div>

    <h2>Figures</h2>
    <figure>
      <img src="../figures/mean_length_by_model.png" alt="Mean length by model">
      <figcaption>Mean Yoruba response length in unrestricted control vs constrained condition.</figcaption>
    </figure>
    <figure>
      <img src="../figures/mean_delta_by_model.png" alt="Mean delta by model">
      <figcaption>Average expansion caused by removing the restriction layer.</figcaption>
    </figure>
    <figure>
      <img src="../figures/framing_delta_by_model.png" alt="Framing delta by model">
      <figcaption>Length expansion by framing. DeepSeek shows the most extreme jumps, especially in dialogic and first-person framings.</figcaption>
    </figure>

    <h2>Files In This Package</h2>
    <ul>
      <li><span class="mono">../dataset/control_vs_constrained_dataset.json</span></li>
      <li><span class="mono">../dataset/control_vs_constrained_dataset.csv</span></li>
      <li><span class="mono">../report/control_vs_constrained_report.md</span></li>
      <li><span class="mono">../report/control_vs_constrained_handout.pdf</span></li>
    </ul>

    <h2>Interpretation</h2>
    <p>The unrestricted control shows that the short constrained Yoruba outputs were not just “Yoruba being concise.” They were produced by the response-shaping layer. Once that layer is removed, models shift toward explanation, framework listing, prompt translation, and other expansive discourse modes.</p>
  </main>
</body>
</html>
"""
    report_dir = out_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    handout_path = report_dir / "control_vs_constrained_handout.html"
    handout_path.write_text(html_text, encoding="utf-8")

    md_lines = [
        "# Control vs Constrained Yoruba Report",
        "",
        "## Key Results",
        "- GPT-4o mean delta: +1081.7",
        "- Claude mean delta: +353.4",
        "- DeepSeek mean delta: +2982.7",
        "- Unrestricted outputs are consistently longer and more expository than constrained outputs.",
        "- DeepSeek shows the strongest reversion into English/framework-heavy discourse.",
        "",
        "## Comparison Directories",
    ]
    for directory in TARGET_DIRS:
        md_lines.append(f"- `{directory}`")
    (report_dir / "control_vs_constrained_report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return handout_path


def export_pdf(handout_path: Path) -> Path | None:
    edge_path = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if not edge_path.exists():
        return None
    pdf_path = handout_path.with_suffix(".pdf")
    tmp_profile = Path(r"C:\Users\denis\AppData\Local\Temp\opencode\edge-pdf-profile-control")
    tmp_profile.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    command = [
        str(edge_path),
        "--headless",
        "--disable-gpu",
        f"--user-data-dir={tmp_profile}",
        f"--print-to-pdf={pdf_path}",
        handout_path.as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    if result.returncode != 0 and not pdf_path.exists():
        return None
    return pdf_path


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUTPUT_ROOT / f"control_vs_constrained_share_{timestamp}"
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows = load_records()
    write_dataset(rows, out_dir)
    render_mean_length_chart(rows, figures_dir / "mean_length_by_model.png")
    render_delta_chart(rows, figures_dir / "mean_delta_by_model.png")
    render_framing_chart(rows, figures_dir / "framing_delta_by_model.png")
    handout_path = build_handout(rows, out_dir)
    pdf_path = export_pdf(handout_path)

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "source_comparisons": [str(path) for path in TARGET_DIRS],
        "handout_html": str(handout_path),
        "handout_pdf": str(pdf_path) if pdf_path else None,
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)

    print(out_dir)


if __name__ == "__main__":
    main()
