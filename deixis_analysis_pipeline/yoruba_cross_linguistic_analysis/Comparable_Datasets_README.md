# Comparable English-Yoruba Datasets for OpenAI and Anthropic

> **Extended analysis:** four models, open/constrained arms, and èmi/ẹ̀mí audit → [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md). Full doc map → [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).

This note documents the second-stage comparable datasets created for the OpenAI and Anthropic English-Yoruba comparison.

## Files created

In `data/`:

- `english_openai_anthropic_comparable.csv`
- `yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.json`
- `comparable_dataset_schema.md`

## What these datasets do

These files create a shared comparison layer across English and Yoruba for the two model lines:

- OpenAI / GPT-4o
- Anthropic / Claude

They preserve the existing manually or semi-manually coded fields where available, and add a second-stage enrichment layer so that English and Yoruba can be compared on more similar discourse variables.

## Fields now available for comparison

### Existing core fields

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability` (Yoruba only; `not_applicable` for English)

### Added discourse fields

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- `indexical_coherence_notes`

### Added marker-count fields

- first-person counts
- emphatic first-person count
- first-person plural count
- second-person count
- third-person count
- temporal markers
- spatial markers
- demonstratives
- obligation markers
- advisory formulas
- hedge markers
- universalist markers

### Added density fields

- `pronouns_per_100_words`
- `obligation_density_per_100_words`
- `advisory_density_per_100_words`
- `hedge_density_per_100_words`

## Important caveat

Not all fields have the same evidential status.

### Directly carried over from prior coding

These come directly from existing coding tables:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `contains_framework_labels`
- `contains_followup_question`
- some other binary fields

### Heuristic second-stage fields

These were added algorithmically for comparability and should be treated as **analytic aids**, not final human judgments:

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- marker-count summaries

These are useful for:

- structured comparison
- exploratory tables
- identifying cases for close reading

They should not replace qualitative interpretation where the article makes strong claims.

## Why this matters

The original English side tracked richer discourse variables than the first Yoruba coding pass. These comparable datasets now reduce that asymmetry and make it possible to compare English and Yoruba more directly on:

- ethical content
- moral reasoning type
- rhetorical authority
- stance
- deictic consistency
- pronoun/deixis structure

## Recommended use in the paper

The strongest use is:

1. use the comparable dataset for summary tables and pattern detection
2. use the raw response text and examples for close reading
3. treat the heuristic fields as a second-stage comparison layer rather than as final gold labels

## Rebuilding the datasets

Script:

- `scripts/build_comparable_datasets.py`

Run:

```powershell
python "C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis\scripts\build_comparable_datasets.py"
```
