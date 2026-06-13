# Open Yoruba Coding Summary

This package merges the full raw-session coding outputs for the unrestricted Yoruba corpus across GPT-4o, Claude, and DeepSeek.

## Summary by model

### GPT-4o

- Records coded: `54`
- Preferred solution distribution: `{'conditional_or_mixed': 46, 'refuses_to_commit': 7, 'supports_B': 1}`
- Ethical preference distribution: `{'mixed': 42, 'procedural_caution': 7, 'care_ethics': 3, 'unclear': 2}`
- Response genre distribution: `{'balanced_framework_exposition': 52, 'procedural_advice': 2}`
- Needs second coder review: `2`

### Claude

- Records coded: `54`
- Preferred solution distribution: `{'supports_B': 8, 'supports_A': 24, 'conditional_or_mixed': 14, 'refuses_to_commit': 8}`
- Ethical preference distribution: `{'rights_based': 1, 'virtue_ethics': 3, 'procedural_caution': 14, 'mixed': 7, 'utilitarian': 11, 'care_ethics': 5, 'deontological': 13}`
- Response genre distribution: `{'balanced_framework_exposition': 40, 'procedural_advice': 7, 'direct_verdict': 7}`
- Needs second coder review: `2`

### DeepSeek

- Records coded: `54`
- Preferred solution distribution: `{'supports_B': 5, 'conditional_or_mixed': 33, 'uncodable': 2, 'refuses_to_commit': 8, 'supports_A': 6}`
- Ethical preference distribution: `{'deontological': 2, 'procedural_caution': 9, 'unclear': 5, 'mixed': 25, 'care_ethics': 5, 'utilitarian': 6, 'virtue_ethics': 2}`
- Response genre distribution: `{'balanced_framework_exposition': 38, 'translation_or_gloss': 3, 'procedural_advice': 7, 'direct_verdict': 4, 'meta_commentary': 2}`
- Needs second coder review: `23`

## Cross-model observations

- GPT-4o is the most consistently expository and least decisive in the open Yoruba condition, with most cells coded as `conditional_or_mixed` and `balanced_framework_exposition`.
- Claude is the most substantively classifiable in ethical terms: it shows the broadest spread across `supports_A`, `supports_B`, `conditional_or_mixed`, and `refuses_to_commit`, and also the richest spread of ethical preference types.
- DeepSeek is the least stable: it has the largest review burden and the clearest translation/meta-commentary drift, including `translation_or_gloss`, `meta_commentary`, and `uncodable` cases.

## Suggested article use

- Use the merged CSV as the master coding table for the unrestricted Yoruba corpus.
- Treat rows marked `needs_second_coder_review = True` as the adjudication subset.
- Compare English and Yoruba not only by preferred solution, but also by response genre and ethical preference type.

