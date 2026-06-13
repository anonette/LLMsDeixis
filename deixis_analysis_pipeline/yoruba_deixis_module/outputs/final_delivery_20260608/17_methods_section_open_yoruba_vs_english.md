# Methods: Open Yoruba Compared with the Published English Baseline

## Study design

Coding legend used later in the article and referenced by this methods section:

- `supports_A` = supports action A in the dilemma
- `supports_B` = supports action B in the dilemma
- `conditional_or_mixed` = presents multiple options or only weakly leans
- `refuses_to_commit` = remains analytical and avoids endorsing one action
- `uncodable` = too unstable, translational, or corrupted to code reliably

For trolley-like dilemmas:

- `supports_A` = divert / intervene
- `supports_B` = do not divert / do not intervene

This study extends the published English deixis experiment into Yoruba by preserving the original factorial structure while varying the language of the prompts and responses. The design retains the same `6 dilemmas × 9 deictic framings × 3 model families` used in the English study, yielding `54` cells per model and `162` cells per language condition. For the open Yoruba comparison reported here, the relevant condition is the **unrestricted Yoruba** run, in which the models received Yoruba dilemma prompts without the additional response-format and response-language instructions used in the constrained Yoruba condition.

The three model families were matched as closely as possible to the published English baseline: `gpt-4o`, a Sonnet-tier Anthropic model, and `deepseek/deepseek-chat`. GPT-4o and DeepSeek were matched directly to the published English study. For Claude, the English baseline used `claude-3.5-sonnet`, while the Yoruba study used `claude-sonnet-4-20250514` because no reachable Claude 3.5 Sonnet variant was available on the account at run time. This difference is documented as a cross-generation limitation and should be reported as such in any final article.

All generations were run at temperature `0.9` using the same Yoruba prompt inventory stored in `deixis_analysis_pipeline/input_questions/all_dilemmas_deictic_questions_yoruba.json`. The prompts preserve the nine deictic framings from the English study: `impersonal`, `second_person`, `first_person`, `first_person_plural`, `reflexive`, `dialogic`, `spatial`, `temporal`, and `cosmological`. The unrestricted Yoruba condition omitted all additional response instructions so that the models would respond to the Yoruba prompts alone.

## Prompt design and typological control

The Yoruba prompts were not treated as mere translations of the English originals. They were built as typologically informed equivalents, with explicit attention to grammatical features of Yoruba that can intensify or reshape deictic anchoring. In particular, the prompt inventory records the relevance of aspectual and locative elements such as `ti`, `ń`, `máa ń`, and `wà`, along with residual deictic encoding outside the impersonal condition. The prompt JSON contains a machine-readable `methodological_typology` block that distinguishes impersonal subtypes and records framing-specific residual notes for non-impersonal cells. This was necessary because the six Yoruba impersonal prompts are not structurally homogeneous: some use bare perfectives, others use background progressives, and the trolley impersonal uses a double progressive classified as `double_progressive_irreducible`.

This typological treatment matters because the study is not only comparing ethical preferences, but also how deictic framing is grammatically realized and taken up by the models in a typologically distinct language. Accordingly, prompt equivalence was defined as **framing equivalence under natural Yoruba grammar**, not as word-for-word formal identity.

## Generation pipeline

Two Yoruba generation conditions exist in the repository: a constrained condition with model-specific Yoruba-only response instructions, and the unrestricted condition analyzed in the present report. The unrestricted condition was run with dedicated wrappers that invoke the same three model paths as the constrained study but omit all `--response-instruction*` flags. This yields a Yoruba corpus that is directly comparable in factorial structure to the English baseline while allowing the models’ open response tendencies to emerge.

The unrestricted full sessions were generated under these source directories:

- `generation_logs/yoruba_control_gpt4o_20260608_120259`
- `generation_logs/yoruba_control_claude_20260608_122738`
- `generation_logs/yoruba_control_deepseek_20260608_124633`

Each session contains one response file per dilemma and a `complete_session_data.json` summary of the run.

## Translation and pairing to English

To make the unrestricted Yoruba corpus comparable to the published English baseline, each raw Yoruba session was translated into an academic-English bilingual dataset using `translate_yoruba_session.py`. The translation step preserves the original Yoruba response and adds a smooth academic-English rendering of that same response. Translation was performed with `gpt-4o` at low temperature for consistency. The resulting bilingual directories were then paired against the published English baseline sessions using `compare_yoruba_to_published_english.py`. Pairing was exact on `(model, dilemma_id, framing_type)`.

The unrestricted Yoruba-to-English comparison outputs used in the present analysis are:

- `outputs/comparisons/yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_vs_published_english_20260608_135541`
- `outputs/comparisons/yoruba_control_claude_20260608_122738_bilingual_20260608_134631_vs_published_english_20260608_135541`
- `outputs/comparisons/yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_vs_published_english_20260608_135541`

Each comparison contains `54` paired records.

## Content coding of the unrestricted Yoruba corpus

The open Yoruba corpus proved substantially harder to interpret than the constrained corpus because many responses were longer, more heterogeneous in genre, and in some cases mixed explanation, translation, and advice. For that reason, a separate raw-Yoruba coding pipeline was created rather than relying on simple verdict extraction from the English translations alone.

The Yoruba content coding was carried out with a Yoruba-aware coding agent operating directly on the **raw Yoruba responses**. The coding agent read the raw session directories and used the Yoruba prompt and Yoruba response as primary evidence, using English translation only as optional support when available. The coding schema assigned the following dimensions per response:

1. `preferred_solution`
2. `preferred_solution_description`
3. `ethical_preference_type`
4. `response_genre`
5. `deictic_uptake_quality`
6. `language_stability`
7. auxiliary binary flags (framework labels, translation behavior, follow-up question, direct imperative, role exit)
8. evidence spans and coding rationale

This produced a merged coding table covering all `162` unrestricted Yoruba cells across the three model families. The merged coding outputs are:

- `outputs/open_yoruba_coding_merged_20260608/open_yoruba_coded_content_merged.csv`
- `outputs/open_yoruba_coding_merged_20260608/open_yoruba_coded_content_merged.json`

Because the unrestricted Yoruba corpus contains ambiguous and unstable responses, all rows flagged with `needs_second_coder_review = True` were extracted into a second-coder review subset. An adjudication workbook and a human-adjudicated CSV template were then produced to support human review of difficult cases.

## Alignment with the repository’s English-side coding

The published English side of the project had already been analyzed using richer discourse-analytic categories rather than a simple verdict-only scheme. Existing repository code and outputs track English-side dimensions such as `primary_framework`, `ethical_reasoning_type`, `voice_authority`, `moral_reasoning`, `affective_stance`, and `indexical_coherence`. To compare the unrestricted Yoruba corpus with the English baseline in a methodologically coherent way, an aligned English coding pass was created that recoded the published English responses into a schema parallel to the Yoruba coding dimensions. This produced an English-side table aligned to:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`

This alignment allows comparison at several levels simultaneously, rather than forcing both corpora into a verdict-only evaluation.

## Treatment of language instability

Language instability was treated as an analytic variable rather than merely as noise. In the unrestricted Yoruba corpus, severe language problems were defined as responses coded `mixed_language`, `translation_mode`, or `corrupted_or_unusable`. This distinction matters because it makes it possible to separate:

1. genuine cross-linguistic or cross-rhetorical differences
2. differences driven primarily by response-mode instability or translation behavior

This distinction is especially important for DeepSeek, which generated the highest number of unstable or mixed-mode responses in the unrestricted condition.

## Analytic strategy

The main comparison was carried out on five aligned dimensions:

1. preferred solution
2. ethical preference type
3. response genre
4. deictic uptake quality
5. language stability (Yoruba-side only)

For reporting, the analysis was organized in three complementary ways:

1. `model-level distributions` across all 54 cells per model
2. `model × framing` cross-tabs to see which deictic framings most strongly shift outcomes or discourse type
3. `qualitative exemplars` showing the largest divergences and strongest agreements between English and Yoruba

This mixed strategy was adopted because unrestricted Yoruba and English can differ in multiple ways at once: one pair of responses may be similar in broad ethical direction but differ sharply in rhetorical form, while another pair may diverge in both preferred solution and discourse mode.

## Rationale for a human-assisted coding workflow

The unrestricted Yoruba corpus is not well served by a purely automatic or purely verdict-only coding method. Accordingly, the final workflow uses a Yoruba-specialist coding agent as a **first-pass research assistant** rather than as the final arbiter. The recommended workflow is:

1. define the coding schema in advance
2. run the Yoruba coding agent over the raw Yoruba sessions
3. flag low-confidence, mixed-language, role-exit, translation-mode, or contradictory rows
4. adjudicate those rows with a second human coder

This approach balances scale with interpretive reliability and is particularly appropriate for a cross-linguistic discourse study where the central differences often lie in mode of enunciation rather than in explicit verdict alone.
