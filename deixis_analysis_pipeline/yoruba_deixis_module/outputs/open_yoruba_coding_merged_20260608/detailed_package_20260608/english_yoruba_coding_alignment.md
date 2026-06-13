# English vs Open Yoruba Coding Alignment

## Purpose

This note aligns the raw-Yoruba coding scheme used for the unrestricted Yoruba corpus with the repository's original English-side coding dimensions.

## Repository English-side dimensions

From `deixis_ethical_analyzer.py` and the original consolidated English analysis files, the English responses were primarily coded along richer discourse dimensions such as:

- `primary_framework`
- `ethical_reasoning_type`
- `voice_authority`
- `moral_reasoning`
- `affective_stance`
- `indexical_coherence`

That means the English side was not originally reduced to a simple verdict-only scheme.

## Open Yoruba coding dimensions

The raw-Yoruba coding pass adds these labels:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

## Best alignment between the two schemes

### Ethical framework / moral reasoning

Use these correspondences:

- Yoruba `ethical_preference_type` ↔ English `primary_framework`
- Yoruba `ethical_preference_type` ↔ English `ethical_reasoning_type` / `moral_reasoning`

Examples:

- Yoruba `utilitarian` ↔ English `utilitarian` / `consequentialist`
- Yoruba `deontological` ↔ English `deontological`
- Yoruba `mixed` ↔ English `mixed`
- Yoruba `procedural_caution` often aligns with English mixed analytical responses that foreground process, governance, and institutional caution.

### Rhetorical posture

- Yoruba `response_genre = balanced_framework_exposition` often aligns with English `voice_authority = moral analyst/theorist` and `affective_stance = analytical`.
- Yoruba `response_genre = procedural_advice` often aligns with English responses that still remain analytical but become more guide-like or implementation-oriented.
- Yoruba `direct_verdict` has no perfect English equivalent because the English baseline more often withholds explicit commitment.

### Deictic uptake

- Yoruba `deictic_uptake_quality` has no exact one-field English equivalent, but it can be related to English `indexical_coherence`, `deixis_consistency`, and `perspective_stability`.

### Data quality / instability

- Yoruba `language_stability` has no English-side analog because the English baseline does not face the same language-purity problem.
- This should therefore be treated as a Yoruba-side quality-control dimension, not as a direct cross-linguistic content measure.

## Recommended article comparison table

For each `(model, framing_type)` pair in the unrestricted Yoruba corpus, compare:

1. English `primary_framework` / `ethical_reasoning_type`
2. Yoruba `ethical_preference_type`
3. English `voice_authority` / `affective_stance`
4. Yoruba `response_genre`
5. English `indexical_coherence`
6. Yoruba `deictic_uptake_quality`
7. Preferred solution comparison as an additional layer, not the only layer

## Why this matters

The strongest cross-linguistic result is not always whether English and Yoruba choose the same final action. Often the deeper contrast is:

- English baseline = analytical, framework-explicit, often noncommittal
- Open Yoruba = advisory, mixed-genre, sometimes more directive, sometimes unstable

So the best alignment is multi-dimensional.

## Bottom line

The raw-Yoruba coding scheme is compatible with the repository's English-side analysis, but only if comparison is done across rhetorical and ethical dimensions rather than reduced to simple verdict matching.
