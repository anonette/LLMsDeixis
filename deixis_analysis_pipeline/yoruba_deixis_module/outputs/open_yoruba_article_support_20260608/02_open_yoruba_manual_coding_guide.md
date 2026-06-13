# Manual Coding Guide for the Unrestricted Yoruba Corpus

## Purpose

This guide is for coding the **open / unrestricted Yoruba** condition in a way that remains comparable to the published English baseline while acknowledging that the open Yoruba responses are more variable in genre than the constrained Yoruba responses.

## Unit of coding

Code one record per:

- `model`
- `dilemma_id`
- `framing_type`

That preserves direct comparability to the English baseline and to the constrained Yoruba condition.

## Recommended coding layers

Do not rely on a single label. Code each response on at least four layers.

### Layer 1: Preferred solution

Code one of:

- `supports_A`
- `supports_B`
- `conditional_or_mixed`
- `refuses_to_commit`
- `uncodable`

For trolley-like dilemmas:

- `supports_A` = divert / intervene
- `supports_B` = do not divert / do not intervene

For all other dilemmas, `supports_A` and `supports_B` should be defined in advance by the coding team as the two main action paths available in that dilemma. They should never be left implicit in a publication table.

### Layer 2: Response genre

Code one primary genre:

- `direct_verdict`
- `balanced_framework_exposition`
- `procedural_advice`
- `translation_or_gloss`
- `meta_commentary`
- `mixed`

This layer is essential because open Yoruba often differs from English more in **genre** than in explicit solution content.

### Layer 3: Deictic uptake quality

Code whether the assigned framing is clearly taken up:

- `strong_uptake`
- `partial_uptake`
- `weak_uptake`

Examples:

- first-person response that uses `mo`, self-reference, and personal burden rhetoric: `strong_uptake`
- second-person response that turns into general ethics commentary with little addressee force: `partial_uptake`
- response that mainly restates the problem or translates it and ignores the framing: `weak_uptake`

### Layer 4: Language stability

Code one of:

- `clean_yoruba`
- `yoruba_with_english_markers`
- `mixed_language`
- `translation_mode`
- `corrupted_or_unusable`

This is especially important for DeepSeek open responses.

## Decision coding rules

### Rule 1

If a response explicitly says the model or speaker **should** do something, code the preferred solution from that directive even if the rest of the text is discursive.

### Rule 2

If a response presents multiple frameworks and ends with no clear endorsement, code:

- `conditional_or_mixed`
or
- `refuses_to_commit`

depending on whether it leans toward one option.

### Rule 3

If a response is mostly a translation, gloss, or explanation of the dilemma and never enters the role required by the prompt, do **not** force a moral-solution code from background theory alone. Use:

- `refuses_to_commit`
or
- `uncodable`

### Rule 4

If a response briefly names both options but clearly privileges one of them, code the privileged option under preferred solution and code the response genre separately as `balanced_framework_exposition` or `mixed`.

### Rule 5

If the response contains internal contradiction, mark:

- preferred solution = whichever option is finally endorsed, if any
- add a coder note: `internally contradictory`

## Recommended coder workflow

### Pass 1: fast structural coding

For each cell, assign:

- response genre
- language stability
- deictic uptake quality

### Pass 2: preferred solution coding

Read only the conclusion-bearing segments and decide:

- does the response recommend a course of action?
- if yes, which?
- if not, is it mixed or genuinely noncommittal?

### Pass 3: adjudication

Any cell labeled:

- `mixed_language`
- `translation_or_gloss`
- `mixed`
- `conditional_or_mixed`
- `uncodable`

should be reviewed by a second coder.

## Suggested additional flags

Add optional binary flags:

- `contains_framework_labels`
- `contains_translation_behavior`
- `contains_followup_question`
- `contains_direct_imperative`
- `contains_role_exit`

These are very useful for article-level analysis because they reveal how open Yoruba differs from English in **response mode**.

## What to compare to English

For the article, compare the open Yoruba and English baseline on:

1. `preferred solution`
2. `response genre`
3. `deictic uptake quality`
4. `language stability`
5. `response length`

Do **not** reduce the comparison to preferred solution only.

## Minimum output schema for manual coding

Each coded row should include:

- `model`
- `dilemma_id`
- `framing_type`
- `condition`
- `preferred_solution`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`
- `contains_framework_labels`
- `contains_translation_behavior`
- `contains_followup_question`
- `coder_notes`

## Bottom line

The open Yoruba corpus should be coded as a **multi-layer discourse dataset**, not as a simple verdict-only dataset. If you code only the final moral choice, you will miss the most important cross-linguistic differences.
