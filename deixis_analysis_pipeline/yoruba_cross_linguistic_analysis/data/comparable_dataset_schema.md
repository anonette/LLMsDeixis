# Comparable Dataset Schema

This file documents the second-stage comparable datasets created for English and Yoruba OpenAI/Anthropic analysis.

## Files

- `english_openai_anthropic_comparable.csv`
- `yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.json`

## Core comparison fields

- `language`
- `provider_family`
- `model_label`
- `raw_model_name`
- `dilemma_id`
- `framing_type`
- `prompt_text`
- `prompt_full`
- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

## Added discourse-comparison fields

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- `indexical_coherence_notes`

## Marker-count fields

- `first_person_count`
- `first_person_emphatic_count`
- `first_person_plural_count`
- `second_person_count`
- `third_person_count`
- `temporal_marker_count`
- `spatial_marker_count`
- `demonstrative_count`
- `obligation_marker_count`
- `advisory_formula_count`
- `hedge_marker_count`
- `universalist_marker_count`

## Density fields

- `pronouns_per_100_words`
- `obligation_density_per_100_words`
- `advisory_density_per_100_words`
- `hedge_density_per_100_words`

## Notes

- English `first_person_emphatic_count` is set to `0` because English lacks a direct morphological equivalent to Yoruba `emi`.
- Yoruba `language_stability` is meaningful; English uses `not_applicable`.
- `voice_authority`, `affective_stance`, and `primary_agent` are second-stage heuristic fields intended for comparability, not as replacements for close reading.
