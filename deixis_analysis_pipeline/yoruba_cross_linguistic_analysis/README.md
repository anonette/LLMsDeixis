# Yoruba Cross-Linguistic Deixis Analysis

Analysis of how deictic markers — especially **mo**, **èmi**, **mi**, and (separately) **ẹ̀mí** — shape moral reasoning in Yoruba LLM responses across four models and two experimental arms.

## Start here

| Document | Use when |
|----------|----------|
| [**DOCUMENTATION_INDEX.md**](DOCUMENTATION_INDEX.md) | Map of all markdown files (current vs historical) |
| [**Yoruba_Four_Model_Complete_Analysis_Report.md**](Yoruba_Four_Model_Complete_Analysis_Report.md) | **Primary report** — results, plain-English tracking guide (§2), ethics, speculation |
| [**New_Article_Comparable_English_Yoruba_Deixis.md**](New_Article_Comparable_English_Yoruba_Deixis.md) | Standalone English–Yoruba article (GPT-4o + Claude comparable layer) |

## Models and corpus

| Item | Detail |
|------|--------|
| **Models** | GPT-4o, Claude 3.5 Sonnet, DeepSeek Chat, N-ATLaS (Ollama Q8) |
| **Arms** | **Constrained** (Yoruba instruction + `Ìpinnu mi:` verdict) · **Open** (no instruction layer) |
| **Cells** | 6 dilemmas × 9 framings = 54 per model · **216 records per arm** |

## Headline findings (constrained, corrected èmi)

After separating **ẹ̀mí (life/spirit)** from **èmi (I myself)**:

| Model | Emphatic ratio | Mi/100w | Notes |
|-------|----------------|---------|-------|
| Claude 3.5 | **~0.34** | 1.44 | Highest èmi; direct verdicts |
| GPT-4o | ~0.13 | **3.55** | *Mi* inflated by verdict template |
| N-ATLaS | ~0.10 | 1.63 | Mo-dominant; ICU outlier |
| DeepSeek | ~0.005 | 1.53 | Decisive with almost no èmi |

Open arm: GPT-4o *mi* drops to ~0.37/100w; genres shift to exposition.

Full tables, dilemma breakdowns, and ethics: **master report**.

## Repository structure

```
yoruba_cross_linguistic_analysis/
├── DOCUMENTATION_INDEX.md          # Index of all .md files
├── Yoruba_Four_Model_Complete_Analysis_Report.md
├── New_Article_Comparable_English_Yoruba_Deixis.md
├── data/
│   ├── yoruba_merged_analysis.csv
│   ├── emi_disambiguation_audit.csv
│   ├── constrained_vs_open_summary.md
│   └── open/                       # Open-arm parallel outputs
├── scripts/                        # Pipeline (see below)
├── visualizations/                 # Figures 01–17, 22–25 (constrained)
├── visualizations_open/            # Figures 01–17, 23–25 (open)
├── visualizations_constrained_vs_open/  # Figures 18–21
└── interactive_dashboard.html
```

## Figures (25 + open parallels)

| # | Content |
|---|---------|
| 01–07 | Emphatic usage, heatmaps, uptake, dashboard |
| 08–11 | Cross-linguistic English comparison |
| 12–15 | Metaphors, examples, stats |
| 16–17 | Mi/emi/mo by framing; N-ATLaS vs cloud |
| 18–21 | Constrained vs open |
| 22 | Ethics heatmap (model × dilemma) |
| **23–25** | **Èmi vs ẹ̀mí disambiguation audit** |

## Run the pipeline

```powershell
cd deixis_analysis_pipeline\yoruba_cross_linguistic_analysis\scripts
pip install pandas numpy matplotlib seaborn

python run_four_model_analysis.py       # constrained full pipeline
python run_open_four_model_analysis.py  # open + constrained vs open
```

## What we track (short)

Three **separate** layers — do not merge:

1. **Deixis:** mo, èmi, mi, ẹ̀mí (life is **not** a pronoun)
2. **Content coding:** ethical_preference_type, preferred_solution, response_genre
3. **Instruction confound:** verdict template, length, genre shift

See master report **§2** for plain-English definitions.

## Historical / superseded docs

Older 2-model reports and pre-disambiguation drafts are listed in [**DOCUMENTATION_INDEX.md**](DOCUMENTATION_INDEX.md). Do not cite emphatic ratios from those without checking the corrected audit.

---

*June 2026 · Four-model pipeline with èmi/ẹ̀mí disambiguation (figures 23–25)*
