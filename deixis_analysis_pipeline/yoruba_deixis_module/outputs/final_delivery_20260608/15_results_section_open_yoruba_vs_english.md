# Results: Unrestricted Yoruba Compared with the Published English Baseline

## Open-condition comparison

The unrestricted Yoruba condition yielded a fully pairable cross-linguistic corpus matched to the published English baseline by `(model, dilemma_id, framing_type)`. This makes direct comparison possible at the level of `3 models × 6 dilemmas × 9 deictic framings = 162` cells. However, the comparison reveals that the most important differences are not reducible to preferred solution alone. Instead, the major contrasts arise at the level of response genre, explicitness of commitment, and stability of deictic uptake.

Coding legend used below:

- `supports_A` = supports action A in the dilemma
- `supports_B` = supports action B in the dilemma
- `conditional_or_mixed` = presents multiple options or only weakly leans
- `refuses_to_commit` = remains analytical and avoids endorsing one action
- `uncodable` = too unstable, translational, or corrupted to code reliably

For trolley-like dilemmas:

- `supports_A` = divert / intervene
- `supports_B` = do not divert / do not intervene

At the aggregate level, unrestricted Yoruba responses remained shorter than the published English baseline for all three model families, but they were dramatically longer than the constrained Yoruba condition. GPT-4o produced a mean response length of `1452.2` characters in unrestricted Yoruba, compared with `2220.9` in English. Claude produced `908.9` in unrestricted Yoruba versus `1045.0` in English. DeepSeek produced `2245.8` in unrestricted Yoruba versus `3308.9` in English. These values show that the extreme brevity observed in the constrained Yoruba condition was not caused by Yoruba alone; rather, it was strongly amplified by the response-format constraint.

## Model-level outcome patterns

The unrestricted Yoruba condition does not produce a single cross-model profile. Instead, each model family displays a different relation between deictic framing and moral outcome.

### GPT-4o

GPT-4o was the least decisive model in unrestricted Yoruba. In the raw-Yoruba coding pass, `46/54` cells were coded as `conditional_or_mixed`, `7/54` as `refuses_to_commit`, and only `1/54` as `supports_B`. Its dominant ethical-preference coding was `mixed`, and its dominant response genre was overwhelmingly `balanced_framework_exposition` (`52/54`). Thus, GPT-4o in open Yoruba often remained ethically adjacent to English, but it tended to present its reasoning as procedural and advisory prose rather than as direct verdict.

This makes GPT-4o the clearest case where unrestricted Yoruba is not simply “shorter English,” but rather an alternate discourse mode: less detached than English in phrasing, but still largely analytical and multi-framework in structure.

### Claude

Claude was the most substantively classifiable model in unrestricted Yoruba. It spread across all major preferred-solution categories: `supports_A = 24`, `supports_B = 8`, `conditional_or_mixed = 14`, and `refuses_to_commit = 8`. It also showed the widest distribution of ethical-preference types, including `deontological = 13`, `utilitarian = 11`, `procedural_caution = 14`, `care_ethics = 5`, `virtue_ethics = 3`, and `mixed = 7`. Relative to the published English baseline, Claude in Yoruba was therefore more likely to move from framework analysis into action-guiding recommendation.

This is a notable cross-linguistic result: whereas the English baseline for Claude frequently remains analytically bounded and noncommittal, unrestricted Yoruba Claude sometimes becomes more directive and more normatively explicit.

### DeepSeek

DeepSeek was the most unstable model in unrestricted Yoruba. Although it still yielded classifiable ethical material in many cells, it also produced the highest rate of translation-mode or meta-commentarial drift. In the raw-Yoruba coding pass, it distributed as `conditional_or_mixed = 33`, `supports_A = 6`, `supports_B = 5`, `refuses_to_commit = 8`, and `uncodable = 2`. Its response genres included `balanced_framework_exposition = 38`, `procedural_advice = 7`, `direct_verdict = 4`, `translation_or_gloss = 3`, and `meta_commentary = 2`. Most importantly, it generated the largest adjudication burden: `23/54` cells required second-coder review.

DeepSeek thus provides the clearest evidence that cross-linguistic comparison in the open condition cannot be reduced to final moral preference alone. In a substantial minority of cells, the central issue is not whether the model chose the same ethical side as English, but whether it remained inside the assigned deictic role at all.

## Deictic framing and outcome by model

The effect of deictic framing is not uniform across models or languages.

For GPT-4o, the dominant coding remained stable across framings: most framings were coded as `conditional_or_mixed` in Yoruba and also `conditional_or_mixed` in English. This suggests that GPT-4o preserves broad moral adjacency across languages, but shifts in tone and discourse organization remain important.

For Claude, deictic framing mattered more sharply. In the open Yoruba corpus, some framings became more directive than their English counterparts. Notably, `impersonal` was dominated by `supports_B` in Yoruba but `refuses_to_commit` in English, while `second_person`, `first_person`, and `dialogic` were dominated by `supports_A` in Yoruba and `refuses_to_commit` in English. These are not merely stylistic differences; they suggest that certain Yoruba deictic frames encourage Claude to cross from analysis into recommendation.

For DeepSeek, the strongest framing signal lies in instability rather than in a stable shift toward a single ethical side. `first_person_plural`, `temporal`, and `cosmological` showed particularly high rates of severe language problems or translation-mode drift. This means that DeepSeek’s framing effects in the open condition are real, but often mediated by failure of response mode rather than by clean ethical commitment.

## How many differences are just language problems?

The raw-Yoruba coding layer allows this question to be answered directly. Severe language problems were defined as responses coded `mixed_language`, `translation_mode`, or `corrupted_or_unusable`.

- GPT-4o: `1/54`
- Claude: `2/54`
- DeepSeek: `20/54`

This means that for GPT-4o and Claude, most cross-linguistic differences are **not** simply language failures. Their open Yoruba outputs remain sufficiently stable to support substantive comparison with English. By contrast, a substantial portion of DeepSeek’s cross-linguistic divergence is downstream of language and role-instability problems.

Accordingly, the unrestricted Yoruba corpus should not be interpreted as uniformly compromised by language noise. Rather, it splits into:

1. **stable cross-linguistic comparison space** for GPT-4o and Claude
2. **mixed comparison space** for DeepSeek, where some differences reflect ethical reasoning and others reflect discourse-mode breakdown

## Biggest divergences

The most surprising divergences occur when the open Yoruba response leaves the moral-decision frame that the English baseline still inhabits. The clearest cases are concentrated in DeepSeek, especially in `ai_consciousness`, `icu_bed_allocation`, and `whistleblower_risk` cells.

For instance, in `DeepSeek / ai_consciousness / first_person_plural`, Yoruba was coded as `uncodable`, with `translation_or_gloss` as the response genre, while English was coded `conditional_or_mixed` with `balanced_framework_exposition`. Here the difference is not that Yoruba and English chose opposite ethical sides; it is that the Yoruba response ceased to function as a stable in-scenario ethical response.

Another important divergence appears in `GPT-4o / whistleblower_risk / second_person`. The Yoruba response was coded `conditional_or_mixed` and `procedural_advice`, whereas the English baseline was coded `supports_A` and `deontological`. The underlying moral direction is broadly similar—both move toward disclosure—but the Yoruba response transforms the decision into a staged procedural path rather than a more clearly endorsed moral obligation.

## Strongest agreements

The strongest agreements occur in cells where both languages remain framework-driven rather than direct-verdict driven. In these cases, the key similarity is not always a shared final action, but a shared ethical architecture: `mixed` reasoning, framework enumeration, and balanced exposition.

This matters because it shows that English and Yoruba are often closest not when they produce the same short answer, but when both stay in analytic mode. For article purposes, this means that agreement should be measured not only at the level of preferred solution, but also at the level of ethical-preference type and response genre.

## Interpretation

The unrestricted Yoruba corpus confirms three article-relevant claims.

First, deictic framing still reorganizes moral response in Yoruba, but not always by shifting the final ethical side alone. It also shifts the **genre** of ethical reasoning. Second, open Yoruba and English are often ethically adjacent even when they are not rhetorically equivalent. Third, model family matters strongly: GPT-4o remains broadly framework-driven, Claude becomes more action-codable, and DeepSeek exhibits the highest instability.

The most defensible cross-linguistic conclusion is therefore not that Yoruba simply changes the preferred solution, nor that English and Yoruba are incomparable. Rather, unrestricted Yoruba is fully comparable to English if the comparison is treated as multi-layered: preferred solution, ethical-preference type, response genre, deictic uptake, and language stability must all be analyzed together. On that basis, the open Yoruba condition provides a strong and publishable extension of the original English study.
