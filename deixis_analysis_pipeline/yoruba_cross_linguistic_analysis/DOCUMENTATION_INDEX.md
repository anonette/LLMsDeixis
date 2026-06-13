# Yoruba Cross-Linguistic Analysis — Documentation Index

**Last updated:** June 2026  
**Start here:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) — single master report (4 models, constrained + open, èmi/ẹ̀mí disambiguation, ethics, figures 01–25).

---

## Tier 1 — Current (use these)

| Document | Purpose | Status |
|----------|---------|--------|
| [**Yoruba_Four_Model_Complete_Analysis_Report.md**](Yoruba_Four_Model_Complete_Analysis_Report.md) | Full empirical + interpretive report; §2 plain-English tracking guide | **Primary** |
| [**New_Article_Comparable_English_Yoruba_Deixis.md**](New_Article_Comparable_English_Yoruba_Deixis.md) | Standalone EN–YO article (GPT-4o + Claude, comparable layer) | **Current** — see §2.6–2.7 for four-model extension |
| [**Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md**](Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md) | Appendix: dilemmas, framings, prompt differences | **Current** |
| [**Comparable_Datasets_README.md**](Comparable_Datasets_README.md) | Schema for EN–YO comparable CSVs | **Current** |
| [**Comparable_Dataset_Results_Chapter.md**](Comparable_Dataset_Results_Chapter.md) | Results chapter draft from comparable layer | **Current** (2-model stats) |
| [**English_Tracking_vs_Yoruba_OpenAI_Anthropic.md**](English_Tracking_vs_Yoruba_OpenAI_Anthropic.md) | What English tracked vs what Yoruba can match | **Current** |
| [**Why_Not_All_English_Dimensions_Were_Tracked_in_Yoruba.md**](Why_Not_All_English_Dimensions_Were_Tracked_in_Yoruba.md) | Methodological rationale for coding scope | **Current** |
| [**README.md**](README.md) | Repo entry point, pipeline commands | **Updated** |

### Generated data summaries (auto-written by scripts)

| Path | Contents |
|------|----------|
| `data/constrained_vs_open_summary.md` | Four-model constrained vs open deltas |
| `data/emi_disambiguation_audit.csv` | Èmi vs ẹ̀mí by model × dilemma (constrained) |
| `data/open/emi_disambiguation_audit.csv` | Same for open arm |
| `data/example_highlights.md` | Notable response examples (constrained) |
| `data/open/example_highlights.md` | Notable examples (open) |
| `data/comparable_dataset_schema.md` | Field definitions for comparable CSVs |

---

## Tier 2 — Superseded (kept for history; do not cite as primary)

These files redirect to the master report. Numbers may be **pre–ẹ̀mí disambiguation** or **pre–four-model**.

| Document | Superseded by |
|----------|----------------|
| [Four_Model_Yoruba_Deixis_Results_Summary.md](Four_Model_Yoruba_Deixis_Results_Summary.md) | Master report §3–§8 |
| [Article_Addendum_Four_Model_Revision_Notes.md](Article_Addendum_Four_Model_Revision_Notes.md) | Master report §12–§14 |
| [Dilemma_Ethics_Model_Patterns_and_Speculation.md](Dilemma_Ethics_Model_Patterns_and_Speculation.md) | Master report §7, §11 |
| [Yoruba_Deixis_Analysis_Report.md](Yoruba_Deixis_Analysis_Report.md) | Master report + New Article |

---

## Tier 3 — Historical papers (2-model, pre-disambiguation)

Early drafts of the “cultural pre-alignment” argument. **Virtue-ethics → highest emphatic ratio** and **0.21 / 0.10 emphatic ratios** appear here but are **revised** in the master report (corrected Claude ~0.34; ẹ̀mí separated from èmi).

| Document | Notes |
|----------|-------|
| Cultural_and_Linguistic_Prealignment_Paper.md | Full draft |
| Cultural_and_Linguistic_Prealignment_Paper_Journal_Style.md | Journal formatting |
| Cultural_and_Linguistic_Prealignment_Paper_Empirical_Linguistics.md | Empirical focus |
| Cultural_and_Linguistic_Prealignment_Paper_Humanities_Theory.md | Theory focus |
| Cultural_and_Linguistic_Prealignment_Submission_Draft.md | Submission version |

**Do not merge blindly into the New Article** without checking master report §10.3 (revised dilemma narratives).

---

## Figures and interactive

| Location | Figures |
|----------|---------|
| `visualizations/` | 01–17 constrained; **22–25** ethics + èmi/ẹ̀mí audit |
| `visualizations_open/` | 01–17 open; **23–25** disambiguation |
| `visualizations_constrained_vs_open/` | 18–21 arm comparison |
| `interactive_dashboard.html` | Legacy 2-model dashboard |

---

## Pipeline (reproduce everything)

```powershell
cd deixis_analysis_pipeline\yoruba_cross_linguistic_analysis\scripts

python run_four_model_analysis.py      # constrained: coding merge → viz 01–17, 22–25
python run_open_four_model_analysis.py # open + constrained vs open 18–21
```

Individual scripts: see master report §15.

---

## Related outside this folder

| Path | Role |
|------|------|
| `CONSOLIDATED_REPORTS/yoruba/` | Mirrored coding outputs + OpenAI/Claude comparison bundle |
| `CONSOLIDATED_REPORTS/INDEX.md` | English-side consolidated reports index |
| `yoruba_deixis_module/` | Generation, bilingual, coding pipeline scripts |

---

## Quick “which doc for which question?”

| Question | Read |
|----------|------|
| What do mo / èmi / mi / ẹ̀mí mean? | Master report **§2** |
| Four models + open vs constrained? | Master report **§1, §3–§5** |
| Ethics by dilemma and model? | Master report **§7**; figure **22** |
| Was “emi” counting life by mistake? | Master report **§2.3–2.4**; figures **23–25**; `emi_disambiguation_audit.csv` |
| English–Yoruba comparable article? | **New_Article_Comparable_English_Yoruba_Deixis.md** |
| What to change in the article? | Master report **§12–§14** |
| Old 2-model narrative / pre-alignment? | Tier 3 papers (historical) |
