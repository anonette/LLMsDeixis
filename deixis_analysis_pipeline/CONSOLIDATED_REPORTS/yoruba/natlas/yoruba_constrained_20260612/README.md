# N-ATLaS Yoruba Constrained Condition

Package: `yoruba_constrained_20260612`

## Prompt condition

**Closed / constrained** — same as the main Yoruba cloud-model runs (`yoruba_gpt4o`, `yoruba_claude`, `yoruba_deepseek`).

Each cell used the `n-atlas` entry from `model_response_instructions.json` (Yoruba-only + `Ìpinnu mi: ... Ìdí: ...` format).

This is **not** the unrestricted open control (`yoruba_control_*`), which omits the instruction layer.

## Source sessions

- Generation: `yoruba_natlas_20260612_113301_cleaned_20260612_115016`
- Bilingual: `yoruba_natlas_20260612_113301_cleaned_20260612_115016_annotated_20260612_115016_bilingual_20260612_115513`
- Coding: `yoruba_natlas_20260612_113301_cleaned_20260612_115016_annotated_20260612_115016_bilingual_20260612_115513_coded_20260612_120919`
- English pairing (structural reference only): `gpt-4o_vs_published_english_20260612_115514`

N-ATLaS has no published English baseline. `paired_comparison.json` pairs Yoruba responses with **GPT-4o English** from the article baseline for row alignment only — not same-model replication.
