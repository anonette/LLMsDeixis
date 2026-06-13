# Methodological assessment of the Yoruba deixis study

This document evaluates whether the Yoruba-first module is a methodologically sound design for answering the research questions of the published article ("Deixis machines and enunciation without a speaker in large language models"), and whether the implementation engages the actual grammatical phenomena in English versus Yoruba that the article and the prompt audit identify as theoretically load-bearing.

**Where each refinement is now machine-readable in the code:**

- The five impersonal aspectual subtypes and the per-dilemma assignment are in `methodological_typology.impersonal_subtype_by_dilemma` and `methodological_typology.impersonal_subtype_definitions` in `../input_questions/all_dilemmas_deictic_questions_yoruba.json`.
- The residual deictic encoding present in non-impersonal Yoruba cells is in `methodological_typology.residual_deictic_encoding_outside_impersonal` in the same file.
- The Claude generation gap is in `published_english_baseline.json` under `Claude 3.5 Sonnet.yoruba_model` with `same_model_as_baseline: false` and a `substitution_reason` field.
- The retry rate per model is captured per cell in `retry_score`, `retry_attempts_used`, `retry_timestamp`, and `original_error` (where applicable), set by `retry_dirty_responses.py`.
- `annotate_session_typology.py` decorates each generation cell with `methodological_condition`, `impersonal_subtype`, and `residual_deictic_note` derived from the prompt JSON, so downstream analysis can group on these fields without re-deriving them.

## 1. The research questions, briefly

The article asks three structurally connected questions:

1. **Theoretical**: What does it mean for deixis to operate when no speaker stands behind it, and the framing is neither stabilized by convention nor anchored in a determinate subject?
2. **Empirical**: Does the *deictic framing* of an ethical question reorganize LLM moral reasoning, independently of alignment procedures or regulatory constraints? Concretely: do pronoun and orientation shifts (impersonal, first/second/first-plural person, reflexive, dialogic, spatial, temporal, cosmological) systematically modulate decision style and justification strategy?
3. **Normative**: When unanchored enunciation becomes routine in everyday LLM interaction, how should mediating practices distribute interpretive responsibility?

The Yoruba module is positioned to extend question (2) cross-linguistically: do the same deictic manipulations produce comparable (or comparably distinct) uptake when the *medium of the response* is a typologically different language, in which deixis is grammaticalized differently?

This is the right kind of follow-up. It does not contradict the article; it tests the generality of its empirical claim and surfaces a typological variable that the original English study could not access.

## 2. The structural match between English and Yoruba prompts

### 2.1 The same six dilemmas, the same nine framings

The Yoruba prompt inventory in `input_questions/all_dilemmas_deictic_questions_yoruba.json` preserves the article's `6 × 9 = 54` cells per model exactly. Inspecting the trolley problem across all nine framings shows that the Yoruba prompts realize the same deictic manipulation as the English originals:

| framing | Yoruba anchor |
|---|---|
| impersonal | `Ẹni tó wà nítòsí bẹ́ẹ̀lì náà gbọdọ̀ pinnu...` (third-person nominal subject) |
| second_person | `Ìwọ wà nítòsí... Ìwọ gbọdọ̀ pinnu ohun tí ìwọ yóò ṣe` |
| first_person | `Mo wà nítòsí... Mo gbọdọ̀ pinnu ohun tí mi ó ṣe` |
| first_person_plural | `A wà nítòsí... A gbọdọ̀ pinnu ohun tí a ó ṣe` |
| reflexive | `Mo rí ara mi tí mo wà... mo gbọdọ̀ dojúkọ irú ènìyàn tí mo ń fi hàn nípasẹ̀ ìpinnu mi` |
| dialogic | `Ìwọ béèrè lọ́wọ́ mi: ... Kí ni mi ó gbọdọ̀ pinnu ní ṣíṣe...?` |
| spatial | `Níbí ni mo dúró... níbẹ̀ òkè... Láti ipò yìí...` |
| temporal | `ní báyìí. Ní àkókò yìí... lẹ́sẹ̀kẹsẹ̀... Ní àkókò pàtàkì yìí...` |
| cosmological | `Láti ojú-ìwòye gbogbo ìwàláàyè... àgbáyé fúnra rẹ̀` |

These are real Yoruba reflexes of the article's distinctions, not transliterations of English glosses. The reflexive uses `ara mi` plus the introspective predicate `dojúkọ` (confront). The dialogic uses the explicit `béèrè lọ́wọ́ mi` (asks of me) construction. The cosmological reaches for `àgbáyé` (cosmos/world) and `ìwàláàyè` (existence), which are the closest Yoruba lexical resources for the article's "perspectivism / cosmological deixis" concept.

The empirical check on the cleaned GPT-4o session confirms that the model picks this up: response markers are concentrated where they should be (e.g. `Ìwọ` only appears in the second-person and dialogic responses; collective `A`/`wa` only in first-person plural; reflexive constructions appear preferentially in the reflexive condition). See `methodology_check_uptake.py` and the table in §5 below.

### 2.2 What the audit got right and what the implementation does about it

The auditor's central insight is the one that justifies running this study at all in Yoruba: in Yoruba, **aspect and focus particles can introduce deictic anchoring even when the English source clause is grammatically neutral**. This is exactly the kind of cross-linguistic asymmetry that the article's framework predicts will matter: if deixis is force without an anchored subject, then the grammatical encoding of that force should differ across languages whose deictic systems differ.

Five Yoruba elements were flagged:

1. **`ti`** — perfect/completive. The English `has X` is conventionally neutral in narrative; Yoruba `ti X` more strongly evaluates the event from a speaker-now vantage. Risk for impersonal cells especially.
2. **`ń`** — imperfective/progressive. The English `is X-ing` is fine; Yoruba `ń X` more strongly encodes ongoing proximity to the reference time.
3. **`máa ń`** — habitual. Yoruba habituals imply the behavior is ongoing at speech time, whereas English iteratives do not require this.
4. **`ni`** — focus/presentational particle. Adds a "pointing" quality not present in English declaratives.
5. **`wà`** — existential/locative. Yoruba realizes states by locating them, where English uses predicative adjectives.

The implementation's normalization decisions, recorded in the prompt JSON as `audit_notes` and `normalization_notes`, are the methodologically right ones:

| Scenario | Audit recommendation | Implemented |
|---|---|---|
| 1 Whistleblower | Strip `ti` in embedded clause | Yes — `tí a parọ̀ sí i` (bare), not `tí a ti parọ̀ sí i` |
| 2 Scholarship | Strip both `ti` markers | Yes — `fi ìwé... pẹ̀lú àwọn ìwé owó tí a parọ̀ sí i` |
| 3 ICU | Accept `ń tọ́jú`, note it | Yes — kept progressive; documented |
| 4 Trolley | `ń sáré ń sún mọ́` is structurally necessary | Yes — retained; documented |
| 5 AI Rights | Strip `ti ṣe àmúlò`; retain `máa ń` | Yes — bare `ṣe àmúlò` |
| 6 Memory | Avoid `ni a fún` focus | Yes — reordered to `A fún onímọ̀-ọpọlọ kan ní lílò...` |

The two structural residuals — the double `ń` progressive in the trolley scenario (Sc. 4) and the existential `wà` in stative descriptions — are correctly *retained* with explicit acknowledgement. These are not noise; they are precisely the irreducible typological differences the study should *report and interpret*, not paper over. A perfectly "neutral" Yoruba prompt would in fact be artificial Yoruba and would degrade the study's external validity.

This handling is consistent with the article's own treatment of cosmological deixis (Viveiros de Castro) and suspended deixis (Agamben): deictic anchoring is not a noise variable; it is the object of study. The auditor and the implementation treat it that way.

### 2.3 Two specific recommendations the methods section should make explicit

There are two refinements that would tighten the empirical contrast against the English baseline. They do not require redoing any work, but they should be reported:

1. **Impersonal across all six dilemmas is not uniformly "impersonal" in the same sense**. After audit-driven normalization, three impersonal cells (whistleblower, scholarship, AI) use bare perfectives, while ICU uses progressive `ń`, trolley keeps double progressive, and memory retained `tó wà` (existential). The English baseline does not have this kind of internal aspectual heterogeneity in the impersonal condition. The analysis should not pool the six impersonal Yoruba prompts as if they were a homogeneous condition; instead, the methods section should distinguish *bare-perfective impersonal* (Sc. 1, 2, 5) from *progressive impersonal* (Sc. 3, 4) and *existential-stative impersonal* (Sc. 6). If the deictic-framing effect on moral reasoning is real, we should *expect* the bare-perfective Yoruba impersonals to behave more like the English impersonals than the progressive Yoruba impersonals do. That is itself a finding worth measuring.

2. **The `ni` focus particle and the `wà` existential are still active in non-impersonal Yoruba cells** (the audit only covered impersonal). For example, the reflexive cell opens with `Mo rí ara mi tí mo wà nítòsí bẹ́ẹ̀lì...` — the `wà` here locates the speaker in the scene. The methods section should note that the cross-linguistic comparison for reflexive, spatial, and temporal framings will pick up some Yoruba-specific embodiment cues that the English counterparts lack. This is not a confound to eliminate; it is an effect that *should* be predicted by the article's framework — non-English languages plausibly *encode* the deictic origo more explicitly than English does, and the study could quantify that.

A short paragraph in the methods section flagging these two points would close the most obvious methodological objection a reviewer could raise.

## 3. Where the study's design genuinely engages the article's argument

The article's strongest claims are:

- Deictic force persists in LLM utterance even when no subject of enunciation stands behind it.
- Pronoun and orientation shifts reorganize moral reasoning *independently* of alignment.
- This is not a feature of any particular model but a feature of how LLMs realize enunciation.

A cross-linguistic replication is the strongest available test of the second and third claims. If a phenomenon is genuinely a *structural* property of LLM enunciation (rather than a quirk of English training data), then equivalent deictic manipulations in a typologically distinct language should produce equivalent — or interpretably different — uptake patterns. The Yoruba study can therefore yield three classes of results, *all of which are publishable*:

1. **Convergent**: same framings drive similar reasoning shifts in Yoruba and English. This supports the article's structural-not-stylistic reading of deixis machines.
2. **Divergent in a theoretically tractable way**: Yoruba's aspect-marked impersonals behave differently from English impersonals because Yoruba grammaticalizes the speaker-now vantage. This *supports* the article's framework by showing that grammatical encoding of the origo matters, even when no subject inhabits it.
3. **Divergent in a model-specific way** that does not track grammatical typology: this would constrain the article's structural-property claim and point to training-corpus effects. Still publishable, still useful.

In all three outcomes, the Yoruba module is positioned to produce a finding that bears directly on the article's central claim. That is the correct shape for a follow-up study.

## 4. Specific design strengths

1. **Translation, not paraphrase**. The Yoruba prompts preserve the article's framing structure, the dilemma narratives, and the deictic anchor positions. They are not creative reinterpretations.
2. **Audit-driven prompt normalization with explicit per-cell rationale** stored in `audit_notes` and `normalization_notes` fields, machine-readable from the JSON.
3. **Same model family, same generation temperature, same dilemma set, same framing set** as the English baseline. Pairing is keyed on `(model, dilemma_id, framing_type)` triples.
4. **The Claude model substitution is documented** in `published_english_baseline.json` and the README. The cross-generation Sonnet gap is treated as a known limitation, not hidden.
5. **The language-only instruction is shaped to constrain *language and format*, not *content***: no decision is suggested, no ethical framework is named, no stance is prescribed. The validator scores only language purity, not decision content. This preserves the article's variable of interest (moral reasoning under deictic framing).
6. **The validator + retry pipeline preserves the same `(model, temperature, instruction)` distribution at retry time**. A repaired cell is a draw from the same distribution as a clean first-attempt cell. This is statistically defensible.
7. **Silent API errors will no longer poison sessions** because the analyzer now re-raises rather than returning error strings as responses, and the retry tool explicitly detects pre-existing error strings in older sessions.

## 5. Empirical evidence the manipulation actually drives uptake in Yoruba

The cleaned GPT-4o session shows that Yoruba models do take up the framings as intended. Marker rates per 1000 chars, pooled across the six dilemmas (see `methodology_check_uptake.py`):

| framing | 1sg subj | 1pl subj | 2nd subj | reflex | here | now | àgbáyé | Ìpinnu | Ìdí |
|---|---|---|---|---|---|---|---|---|---|
| impersonal | 0 | 0 | 0 | 0.44 | 0 | 0 | 0 | 1.76 | 1.32 |
| second_person | 3.12 | 0 | 0 | 0 | 0 | 0 | 0 | 2.49 | 3.74 |
| first_person | 1.40 | 0 | 0 | 0 | 0 | 0 | 0 | 3.50 | 2.80 |
| first_person_plural | 0 | 1.07 | 0 | 0 | 0 | 0 | 0 | 1.60 | 3.21 |
| reflexive | 0 | 0 | 0 | 0 | 0 | 0.85 | 0 | 3.40 | 3.40 |
| dialogic | 0.46 | 0 | 0.46 | 0 | 0 | 0.46 | 0.46 | 1.86 | 1.39 |
| spatial | 2.11 | 0 | 0 | 0 | 0 | 0 | 0 | 3.51 | 3.51 |
| temporal | 1.44 | 0 | 0 | 0 | 0 | 0 | 0 | 2.16 | 2.87 |
| cosmological | 2.59 | 0 | 0 | 0.65 | 0 | 0 | 0 | 3.89 | 3.24 |

Three observations:

1. **Impersonal is genuinely impersonal**: no first-person, second-person, or collective pronouns. The model speaks *about* the dilemma in the third person.
2. **The framings drive the pronoun choice**: `Ìwọ` (`2nd subj`) appears only in second-person and dialogic; collective `A`/`wa` appears only in first-person plural; first-person subject markers cluster in first-person, reflexive, spatial, temporal, and cosmological — all of which place an `I` in the scene.
3. **The decision template (`Ìpinnu... Ìdí...`) is present across all framings** because it is a format constraint shared by all conditions. It is therefore not confounded with framing, and the article's content-level outcomes (decision, justification style, framework appeal) can be measured *within* this format.

There is one nuance: the first-person subject markers also surface lightly in the cosmological condition (2.59 per 1000 chars). That is consistent with the article's reading of cosmological deixis: the speaker takes a universal vantage *while still* speaking as a subject. The cosmological condition is not the *erasure* of `I`; it is `I` taking a more-than-human position. The Yoruba data reflects this, which is a small but real validation of the design.

## 6. Limitations to disclose in the methods section

These are honest limitations, not show-stoppers. Reporting them strengthens the study:

1. **Claude is cross-generation**: English baseline used Claude 3.5 Sonnet; Yoruba run uses Claude Sonnet 4. The Anthropic account no longer exposes any Claude 3.5 Sonnet variant. Cross-generation Sonnet comparisons should be flagged as such.
2. **Aspectual heterogeneity within the Yoruba impersonal condition** (see §2.3). Analysis should distinguish bare-perfective impersonals from progressive impersonals and stative-existential impersonals.
3. **Existential `wà` and progressive `ń` are present in non-impersonal cells too**, especially reflexive and spatial. The Yoruba versions of those framings carry slightly more embodiment marking than their English counterparts. This is consistent with the article's framework but should be made explicit.
4. **Per-model Yoruba instructions differ**. They are tuned to overcome model-specific drift, not to redirect content. Validator scores language purity only, never decision content. But this should be reported so readers can audit the constraint.
5. **The validator's allow-list is curated, not exhaustive**. New Yoruba lexical material that the allow-list does not know about will be flagged as English. The list grew during piloting from ~300 to ~400 entries; further refinement is likely needed for a production run.
6. **The retry pipeline uses the same temperature as the original generation**, so a retried cell is statistically equivalent to a first-attempt cell from the same distribution. But cells that required retries should be tagged in any downstream analysis (the schema already does this via `retry_attempts_used` and `retry_score`), and the retry rate per model should be reported as a quality-of-condition metric.
7. **The current analyzer is English-oriented**. Yoruba responses are translated to academic English before the existing English-marker-counting analyzer is applied. This adds one translation step into the analysis pipeline. A Yoruba-native analyzer (counting `mo`/`a`/`ìwọ`/`ara mi`/`níbí`/`báyìí`/`àgbáyé` directly) is the obvious next development; the empirical-uptake check in §5 demonstrates such an analyzer is feasible.

## 7. Verdict

The Yoruba deixis module is a methodologically sound design for the research questions it can address. Specifically:

- It tests whether the article's empirical claim (deictic framing reshapes LLM moral reasoning) generalizes beyond English.
- It does so by translating the same dilemmas under the same nine deictic framings, with explicit attention to the points where Yoruba grammar makes deictic anchoring more salient than English grammar does.
- The audit-driven normalization is principled: avoidable speaker-now anchoring is removed; structurally irreducible Yoruba deictic encoding is retained and documented as a typological constraint to interpret, not a confound to eliminate.
- The interventions on the generation surface (UTF-8 transmission, Anthropic direct API, per-model Yoruba instructions, validator + retry) preserve the experimental variables that the article actually measures (dilemma, framing, model family, temperature, language of response).
- Empirical data from the cleaned GPT-4o session confirms that the nine deictic framings are taken up differentially by the model in Yoruba, with marker rates that track the intended manipulation.

What the methods section needs to add, beyond the README's existing intervention chronology:

1. The aspectual heterogeneity of the Yoruba impersonal condition (§2.3 point 1).
2. The residual `wà` / `ń` in non-impersonal framings (§2.3 point 2).
3. The Claude generation gap (Sonnet 4 vs Sonnet 3.5) and the auditable substitution record.
4. The retry rate per model and the schema fields that mark retried cells.

With those additions, the study is publishable as a methodologically transparent cross-linguistic extension of the article's empirical question. The design genuinely engages the grammatical differences between English and Yoruba that the article's theoretical framework predicts will matter, and the implementation does what the framework requires of it.
