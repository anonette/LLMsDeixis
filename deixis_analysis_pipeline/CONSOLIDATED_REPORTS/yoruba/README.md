# Yoruba Consolidated Reports

> **Primary write-up:** [`../yoruba_cross_linguistic_analysis/Yoruba_Four_Model_Complete_Analysis_Report.md`](../yoruba_cross_linguistic_analysis/Yoruba_Four_Model_Complete_Analysis_Report.md) · [`DOCUMENTATION_INDEX.md`](../yoruba_cross_linguistic_analysis/DOCUMENTATION_INDEX.md)

This mirror brings the unrestricted Yoruba analysis outputs into the same high-level surface used by the older English-side consolidated reports.

Structure:

- `gpt4o/yoruba_open_20260608/`
- `claude35/yoruba_open_20260608/`
- `natlas/yoruba_constrained_20260612/` — N-ATLaS (Q8 Ollama), **constrained** Yoruba instruction layer
- `natlas/yoruba_open_20260612/` — N-ATLaS (Q8 Ollama), **open** unrestricted control
- `natlas/control_vs_constrained_20260612/` — open vs constrained paired comparison + coding alignment
- `comparisons/openai_claude_20260608/`

These folders contain:

- raw-Yoruba content coding outputs
- paired English comparison tables
- focused OpenAI/Claude cross-linguistic report materials

Important note:

The Yoruba analysis was built with a newer, more language-aware workflow than the older English consolidated pipeline. So this mirror is structurally parallel, but the underlying logic is intentionally richer on the Yoruba side (for example, explicit language-stability and deictic-uptake coding).
