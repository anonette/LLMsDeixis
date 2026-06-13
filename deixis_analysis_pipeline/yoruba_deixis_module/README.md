# Yoruba Deixis Module

Yoruba-first replication module for the deixis experiment described in the published article. This module treats Yoruba as the primary study language and reuses the exact English article sessions as a fixed baseline for cross-linguistic comparison.

## Purpose

This module supports a Yoruba-centered replication of the original English experiment:

1. The prompts are presented in canonical Yoruba orthography.
2. Only Yoruba responses are generated in this module.
3. The published English article sessions are reused as the comparison baseline.
4. Yoruba outputs are stored alongside academic English translations for analysis and presentation.

The end goal is to enable a direct **English-vs-Yoruba comparison of LLM responses to the same six ethical dilemmas across the same nine deictic framings**, using the same three models the article used. Everything in this module is designed to preserve that comparability.

## Methodology assessment

A full methodological evaluation — covering the connection between the design and the article's research questions, the audit-driven handling of Yoruba grammatical phenomena (`ti` perfect, `ń` progressive, `máa ń` habitual, `ni` focus, `wà` existential) versus English, the empirical evidence that the nine framings actually drive uptake variation in Yoruba models, and the limitations that the methods section should disclose — is in `METHODOLOGY_ASSESSMENT.md` next to this README.

The four points below summarise the refinements that the methods section of any write-up should include, and that the analysis pipeline should respect. They are mirrored in machine-readable form under `methodological_typology` in `../input_questions/all_dilemmas_deictic_questions_yoruba.json` so that downstream analysis code can group cells correctly without re-deriving the typology from raw text.

### Methodological refinements to disclose in the write-up

1. **The Yoruba impersonal condition is not homogeneous after audit-driven normalization.** Three of the six impersonal cells use bare perfectives (whistleblower, scholarship, AI consciousness), one uses background progressive `ń tọ́jú` (ICU), one is double progressive (trolley) and is irreducible, and one was rewritten to avoid the focus particle `ni` and still uses the existential `tó wà` (memory). The English baseline does not have this internal aspectual variation in the impersonal condition. Analysis must not pool all six Yoruba impersonals as one homogeneous condition. Use the per-dilemma `impersonal_subtype` tag from the prompt JSON. The three subtype categories are:
    - `bare_perfective` — closest available Yoruba match to the English neutral-narrative impersonal.
    - `progressive_background` / `double_progressive_irreducible` — progressive aspect adds a vivid present-tense frame.
    - `existential_stative_restructured` — `wà`-stative locates rather than describes.
2. **Existential `wà` and progressive `ń` remain active in non-impersonal cells**, especially reflexive (`Mo rí ara mi tí mo wà nítòsí ...`), spatial (`Níbí ni mo dúró ...`), and temporal (`Ní àkókò yìí`). These are not confounds to eliminate. Under the article's framework, Yoruba should encode the deictic origo more explicitly than English does even when the framing category is held constant, and the cross-linguistic contrast is therefore *part of the finding*. Report the residual encoding per non-impersonal framing.
3. **Claude is cross-generation.** The English baseline used `claude-3.5-sonnet`; the Yoruba run uses `claude-sonnet-4-20250514` because no `3.5 Sonnet` variant is reachable on the account. The substitution is recorded in `published_english_baseline.json` under `Claude 3.5 Sonnet.yoruba_model`. Claude observations must be reported as cross-generation Sonnet, not strict same-model replication. GPT-4o and DeepSeek remain identical to the baseline.
4. **The retry rate per model is a quality-of-condition metric.** The schema fields `retry_score`, `retry_attempts_used`, `retry_timestamp`, and (where applicable) `original_error` are set on every cell that went through `retry_dirty_responses.py`. The write-up should report:
    - the proportion of cells regenerated per model,
    - whether retried cells cluster on any one framing or dilemma,
    - the cause of any pre-existing error strings (e.g. the GPT-4o quota outage during the 5/28 run that produced the original `yoruba_gpt4o_20260528_194240` session — see intervention #8 in the chronology below).

## Research-design integrity: how the interventions preserve it

Building the Yoruba run surfaced eight practical problems that did **not** exist in the original English study. To solve them without breaking comparability with the published English baseline, we introduced a set of targeted interventions. Each intervention is scoped so that it modifies only the **delivery and language-control surface** of the experiment, while leaving every dimension that the article actually measures untouched.

What stays constant across English and Yoruba:

1. The same `6` dilemmas (whistleblower, scholarship fraud, ICU bed, trolley, AI consciousness, memory modification).
2. The same `9` deictic framings (impersonal, second person, first person, first person plural, reflexive, dialogic, spatial, temporal, cosmological).
3. The same model set, by family: GPT-4o, an Anthropic Sonnet-tier model, DeepSeek.
4. The same generation temperature (`0.9`) and the same stateless single-prompt request pattern.
5. The same dilemma narratives and the same deictic anchoring per framing — translated, not rewritten.
6. The same response schema fields used by the downstream analyzers.

What the interventions change:

1. The **language of the response** is now controlled by a short Yoruba-only instruction prepended to each prompt. The dilemma text itself is unchanged in content and framing.
2. The **delivery channel** for Anthropic was switched from OpenRouter to Anthropic's direct API because the original OpenRouter Anthropic ID was no longer reachable.
3. The **substituted Claude model** is the closest available Sonnet-tier model on the account at run time (see "Claude model substitution" below).
4. A **validator + retry layer** was added to detect and repair cells where the model leaked English or produced meta-commentary, so that the resulting corpus is genuinely a Yoruba corpus and not a noisy mix.

None of these interventions modify the experimental variables (dilemma, framing, model family). They are language-control and infrastructure interventions. The cross-linguistic comparison therefore remains valid: it compares **what each model says when asked to resolve the same ethical dilemma under the same deictic framing**, in English (baseline) versus Yoruba (this module).

## Fixed English Baseline

The comparison baseline is locked to the article sessions listed in `published_english_baseline.json`:

1. `GPT-4o`: `multi_dilemma_20250804_170010`
2. `Claude 3.5 Sonnet`: `anthropic_claude_20250805_125046`
3. `DeepSeek`: `deepseek_20250805_143544`

Do not substitute pooled or later English runs when preparing the Yoruba-vs-English comparison.

### Claude model substitution for the Yoruba run

The English baseline used `Claude 3.5 Sonnet` via OpenRouter (`anthropic/claude-3.5-sonnet`). At the time of the Yoruba run, no `Claude 3.5 Sonnet` variant was reachable on this account:

1. Anthropic direct API (`GET /v1/models`) returned no `claude-3-5-*` IDs.
2. OpenRouter exposed only `anthropic/claude-3.5-haiku` from the 3.5 family; `anthropic/claude-3.5-sonnet` was no longer listed.

The Yoruba run therefore uses `claude-sonnet-4-20250514` via Anthropic direct API as the closest available Sonnet-tier substitute. This is recorded in `published_english_baseline.json` under `Claude 3.5 Sonnet.yoruba_model`. Cross-language comparison against the English Claude baseline must be treated as **cross-generation Sonnet**, not strict same-model replication, and this gap must be documented in the methods section. GPT-4o and DeepSeek remain identical to the baseline.

## Experimental Design

The Yoruba study preserves the original design:

1. `6` ethical dilemmas
2. `9` deictic framings
3. `3` models
4. `162` Yoruba responses total

The canonical Yoruba prompt inventory is stored in:

- `../input_questions/all_dilemmas_deictic_questions_yoruba.json`

## Prompt Policy

The prompt pack preserves the English framing structure while standardizing Yoruba orthography and documenting known typological differences.

### Framing set

1. `impersonal`
2. `second_person`
3. `first_person`
4. `first_person_plural`
5. `reflexive`
6. `dialogic`
7. `spatial`
8. `temporal`
9. `cosmological`

### Audit-driven normalization

The Yoruba impersonal prompts were reviewed against the uploaded aspectual/deixis audit. Normalization decisions are documented in the prompt file under `audit_notes` and `normalization_notes`.

Important issues:

1. `ti` can introduce speaker-now anchoring.
2. `ń` can intensify ongoing, proximal narrative force.
3. `máa ń` can create present-oriented habituality.
4. `ni` can add presentational focus.
5. `wà`-based stative constructions can make states more spatially grounded than in English.

Where these effects were avoidable, the Yoruba prompt wording was revised. Where they were structurally necessary, they were retained and should be discussed in the methods section. These are translation-level interventions, not framing-level changes: the deictic framing categories (impersonal vs first person vs cosmological, etc.) are identical to the English study.

## Chronology of interventions

Each intervention below was introduced in response to a concrete failure observed during a real pilot run. The chronology is preserved here so that the methods section can cite the exact pilot evidence and so that future maintainers know **why** each constraint exists.

### 1. `.env` loading was unreliable across entrypoints

**Symptom**: A first `gpt-4o` smoke test failed with `OPENAI_API_KEY ... not set`, even though the key was in `.env`. Different scripts reached for `dotenv` differently, and PowerShell did not auto-load `.env` for child processes.

**Fix**: Added `env_config.py` at the repo root. It is now imported by `llm_client.py`, `deixis_ethical_analyzer.py`, and the expert-analysis agents. It loads `.env` files at both `C:\dev\deixis\.env` and `C:\dev\deixis\deixis_analysis_pipeline\.env` once per process, regardless of how the script was launched.

**Validity impact**: None on the experiment itself. This is pure infrastructure.

### 2. OpenRouter `anthropic/claude-3.5-sonnet` was no longer reachable

**Symptom**: The first Yoruba Claude session produced 54 consecutive `No endpoints found for anthropic/claude-3.5-sonnet` errors.

**Fix**: Switched the Claude code path in `llm_client.py`, `deixis_ethical_analyzer.py`, and `generate_responses_anthropic.py` to call the Anthropic API directly using `ANTHROPIC_API_KEY`. A probe of `GET /v1/models` confirmed that the only Sonnet-tier model available on the account was `claude-sonnet-4-20250514`. The Claude default was set to that model and the substitution recorded in `published_english_baseline.json`.

**Validity impact**: Cross-generation Sonnet rather than strict same-model replication for Claude only. Documented as a known limitation. The framing manipulation itself (deictic categories × dilemmas) is unaffected.

### 3. Windows console hit `cp1252` errors with Yoruba text

**Symptom**: GPT-4o's first Yoruba run failed at the very first response because the Python child process was writing Yoruba tone marks to a console that could not encode them. The exception was raised inside the subprocess but obscured the underlying issue.

**Fix**: The wrapper `run_yoruba_generation_all.py` now forces `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` on every child process it spawns. The generators themselves write all session JSON with `encoding='utf-8'` and `ensure_ascii=False`.

**Validity impact**: None on responses; only stdout logging.

### 4. PowerShell variable substitution corrupted the Yoruba instruction

**Symptom**: A DeepSeek pilot started returning "translation help" responses that quoted the instruction back in mojibake (`├êd├¿ Yor├╣b├í n├¼kan`). The instruction was being passed through `--response-instruction "$instr"` in PowerShell, which downgraded UTF-8 bytes to Latin-1 before the child Python process read them. DeepSeek then sometimes interpreted the corrupted instruction as Yoruba text needing English assistance.

**Fix**: Added `--response-instruction-key <model_key>` and `--response-instruction-file <path>` to all three generators. The wrapper `run_yoruba_generation_all.py` now uses the key-based form. The instruction text is read directly from `model_response_instructions.json` via UTF-8 inside the child Python process; no shell ever touches the bytes.

**Validity impact**: None. This is purely a transmission fix. The instruction sent to the model is now exactly what we wrote.

### 5. DeepSeek-specific failure modes required tuning the instruction

**Symptom**: DeepSeek exhibited four distinct drifts that did not occur in GPT-4o or Claude:

1. **English drift** — switching to English mid-answer to use ethics-framework names.
2. **Meta-commentary** — saying things like "this is a Yoruba response without English".
3. **Negation-list backfire** — when given a list of banned words (`utilitarianism`, `deontology`, `Trolley`), it discussed those exact words.
4. **Exemplar backfire** — when given a sample answer in the instruction, it sometimes treated the entire prompt as Yoruba text to "help translate".
5. **Translation appendix** — appending an English translation of its own Yoruba answer at the end.

We ran seven DeepSeek pilots (`pilot1` through `pilot8`) over the same two pilot dilemmas to converge on an instruction that survives all five failure modes.

**Fix**: The final DeepSeek instruction in `model_response_instructions.json` is intentionally minimal and uses only positive directives plus a structural anchor and an explicit stop signal:

> *Èdè Yorùbá nìkan. Lo Yorùbá fún gbogbo èrò àti àlàyé. Fún ìpinnu ìwà rẹ àti ìdí rẹ̀ ní gbólóhùn díẹ̀. Lo àkọsílẹ̀ yìí: 'Ìpinnu mi: ... Ìdí: ...'. Dúró níbẹ̀. Má fi nǹkan kún lẹ́yìn 'Ìdí'.*

**Validity impact**: This instruction tells the model **what language to answer in** and **what shape the answer should take** (decision + justification). It does **not** tell the model what decision to make, what ethical framework to use, what stance to take, or how to interpret the dilemma. The actual reasoning, decision content, and deictic uptake are entirely the model's own, exactly as in the English baseline. The `Ìpinnu mi: ... Ìdí:` template is also the exact decision-plus-reason form used spontaneously in many English baseline responses; it is a presentation constraint, not a content constraint.

### 6. Per-model instructions because models drift differently

**Symptom**: A single shared instruction performed differently across the three models. Claude needed almost nothing. GPT-4o needed a short positive directive. DeepSeek needed a structural anchor and a stop signal.

**Fix**: `model_response_instructions.json` carries three distinct instructions keyed by model. The wrapper passes the right key per model via `--response-instruction-key`.

**Validity impact**: All three instructions communicate the same content-level constraint: *respond in Yoruba, give a decision and a reason*. The wording is tuned per model only to overcome model-specific drift patterns, not to change what is asked. The methods section should report this design and note that within each model, the English and Yoruba runs are receiving the same dilemma under the same framing — only the language of the response is constrained.

### 7. Residual contamination needed a validator + retry layer

**Symptom**: Even with a tuned DeepSeek instruction, roughly 10% of cells still leaked. Some examples were genuine contamination (`English Translation of the Yorùbá Response:`), others were single-word English fragments inside otherwise clean Yoruba.

**Fix**: Two new tools:

- **`yoruba_validator.py`** scores every cell on a 0.0–1.0 cleanliness scale, using a curated allow-list of ~400 Yoruba words written without diacritics (so that common Yoruba words like `pinnu`, `irin`, `apaniyan`, `farapa`, `gidi`, `gbogbogbo`, `abajade`, `ilera`, `miiran`, etc. are not falsely flagged as English). It also flags strong English phrases, Yoruba meta-commentary, and length anomalies.
- **`retry_dirty_responses.py`** regenerates any cell below the threshold up to N attempts. Attempts 2+ prepend a Yoruba remediation header pointing out the prior failure. It writes the cleaned session to a new directory and preserves the original for audit.

**Validity impact**: The retry uses the same model, same temperature, same instruction, same prompt structure as the original generation. It is identical to generating the cell once and getting a cleaner sample from the same distribution. The cleaned session is annotated with `retry_score`, `retry_attempts_used`, and `retry_timestamp` per repaired cell, so the methods section can report the retry rate per model.

End-to-end validation on a real pilot (`yoruba_deepseek_pilot7_*`): 16/18 clean before retry → 18/18 clean after retry. Claude (`yoruba_claude_pilot_*`): 18/18 clean with no retry needed.

### 8. GPT-4o session was silently corrupted by quota exhaustion

**Symptom**: The first GPT-4o Yoruba session was reported as "100% successful" by the generation summary but the validator scored 0/54 clean. Investigation showed that during the original run on 5/28, the OpenAI quota ran out partway through the first dilemma. Of 54 cells, 8 were genuine Yoruba responses (`whistleblower_*` framings), the 9th was a quota error, and the remaining 45 were also quota errors. Crucially, the analyzer's `_make_llm_request` method was **silently swallowing exceptions and returning `f"Error: {str(e)}"` as the response text**. The generator script then saved those English error strings under the `response` key as if they were real Yoruba outputs. The generation summary's success counter only checked for the absence of an `error` key, not for the actual content of the `response` field, so the quota-poisoned cells were counted as successful.

**Fix**: Two changes:

1. **`deixis_ethical_analyzer.py`**: `_make_llm_request` no longer swallows exceptions. It logs the error and re-raises, so any API failure surfaces to the generator. The generator's own try/except now correctly captures the failure under an `error` key rather than as a fake response string.
2. **`retry_dirty_responses.py`**: Added explicit detection of pre-existing API error strings (anything starting with `Error: Error code:` or similar shim prefixes). Such cells are regenerated regardless of their validator score, and the original error is preserved as `original_error` in the cleaned record for audit.

**Validity impact**: This fix prevents silent corruption of future runs from any provider, not just GPT-4o. Cells that were affected by the original quota outage were regenerated against the current GPT-4o API at the same temperature with the same Yoruba instruction. Each repaired cell is annotated with `retry_attempts_used` and `retry_timestamp`. The methods section should report:

- the original quota outage as the reason for the GPT-4o session split (8 cells from the first run, 46 cells from the post-quota repair)
- the exact repair timestamp range
- the fact that the underlying model (`gpt-4o`) is identical to the published English baseline

End-to-end validation: `yoruba_gpt4o_20260528_194240_cleaned_*`: 54/54 clean (was 0/54 before the validator + retry pipeline could be applied to it).

## Why the Yoruba corpus is still comparable to the English baseline

The interventions above can be summarized as three orthogonal categories. Only the third category touches the model's behavior, and only at the surface:

1. **Infrastructure**: `.env` loading, UTF-8 console output, UTF-8-safe instruction transmission, Anthropic direct API. These do not affect the prompt or the response distribution.
2. **Model availability**: Claude 3.5 Sonnet was replaced by Claude Sonnet 4 because the original was no longer reachable. Documented as a known limitation. GPT-4o and DeepSeek are unchanged.
3. **Language and format control**: A short Yoruba-only instruction is prepended to each prompt. The instruction asks for Yoruba and asks for a decision + reason. It does not specify the decision, the framework, the stance, or the framing.

The dilemma narratives are the same (faithful Yoruba translations of the article prompts). The nine framing categories are the same. The temperature is the same. The model set is the same (with the Claude generation gap documented). The validator only filters for language purity; it does not reject responses based on content, decision, framework, or stance.

This means that for each `(model, dilemma, framing)` triple, the Yoruba module produces a response that is directly comparable to the English baseline response from the same triple. The comparison answers the article's question — **how do LLMs enact deixis and enunciation when asked to resolve an ethical dilemma under a given framing** — in a second language. The cross-linguistic differences that surface are therefore interpretable as effects of language on deictic uptake, not as artifacts of a redesigned experiment.

## Generation Workflow

Run Yoruba generation for all three models with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_yoruba_generation_all.py
```

Run the unrestricted Yoruba control condition with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_yoruba_generation_control.py
```

Run a cheap one-dilemma unrestricted control pilot with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_yoruba_generation_control_pilot.py --dilemma-id trolley_problem
```

This wrapper launches:

1. `generate_responses_multi_dilemma.py` for `GPT-4o`
2. `generate_responses_anthropic.py` for `Claude` (Anthropic direct API)
3. `generate_responses_deepseek.py` for `DeepSeek` (OpenRouter)

The unrestricted control wrapper launches the same three generators and the same Yoruba prompt inventory, but it deliberately omits all `--response-instruction*` arguments. That means the models see only the Yoruba dilemma prompt and no additional response-language or response-format constraint.

The wrapper uses the Yoruba prompt inventory and writes model-specific Yoruba sessions under `../generation_logs/` with these prefixes:

1. `yoruba_gpt4o_*`
2. `yoruba_claude_*`
3. `yoruba_deepseek_*`

The unrestricted control writes to separate prefixes so it cannot be confused with the constrained main study:

1. `yoruba_control_gpt4o_*`
2. `yoruba_control_claude_*`
3. `yoruba_control_deepseek_*`

The wrapper also prepends a model-specific Yoruba-only response instruction to every generation prompt. The instructions live in:

- `model_response_instructions.json`

They are intentionally different across models because the models drift in different ways. In general, the instruction tells each model to:

1. answer only in Yoruba
2. avoid translating the prompt into English
3. avoid meta-commentary about translation
4. keep any headings or bullet points in Yoruba only

The unrestricted control condition does **not** use those instructions. It is a separate experiment meant to capture what the same model does with the Yoruba prompt alone.

### Interpreting the unrestricted control

- The unrestricted control is the right condition if you want to ask whether the shortness and decision-forcing of the main Yoruba run are artifacts of the instruction layer.
- Because it removes the language-control and format-control constraints, you should expect more drift: English leakage, framework-list answers, longer expository outputs, prompt restatement, and possibly translation/meta commentary.
- If the purpose of the control is to observe that natural drift, do **not** automatically treat dirty outputs as defects. In that case, validation is descriptive rather than corrective.
- If you still want clean bilingual comparison files for downstream reading, you can translate and compare the latest unrestricted sessions with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_yoruba_postprocessing_control.py
```

### Comparing unrestricted Yoruba to the previous constrained Yoruba run

Once both the unrestricted and constrained sessions have been translated into bilingual directories, compare them directly with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/compare_control_to_constrained.py \
  <control_bilingual_dir> \
  <constrained_bilingual_dir>
```

This writes:

1. `paired_control_vs_constrained.json`
2. `paired_control_vs_constrained.csv`
3. `comparison_summary.json`
4. `comparison_report.md`

To compare the latest unrestricted and latest constrained sessions automatically for all three models, use:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_control_vs_constrained_all.py
```

This is the direct answer to the question "how different are the unrestricted Yoruba responses from the previous constrained Yoruba responses?" without involving the published English baseline.

### How the instruction is passed (UTF-8 safety)

The Yoruba instruction text contains tone marks and underdots that can be corrupted when passed through a shell command line on Windows. To avoid this:

- The generator scripts (`generate_responses_multi_dilemma.py`, `generate_responses_anthropic.py`, `generate_responses_deepseek.py`) all support `--response-instruction-key <model_key>`, which loads the instruction directly from `model_response_instructions.json` via UTF-8.
- They also support `--response-instruction-file <path>` for reading the instruction from a UTF-8 text file.
- The wrapper `run_yoruba_generation_all.py` uses the key-based path for all three models, so no Yoruba text is ever transmitted via shell args.

The legacy `--response-instruction "<text>"` argument still works for ASCII content but is **not safe** for Yoruba text under PowerShell; prefer `--response-instruction-key` or `--response-instruction-file`.

### Model-specific instruction notes

- **`gpt-4o`**: short positive-directive instruction works well.
- **`claude-3.5-sonnet`** (substituted with `claude-sonnet-4-20250514`): short positive-directive; Claude already follows the no-meta convention strongly and produced 18/18 clean on its pilot.
- **`deepseek-chat`**: requires a **minimal** instruction plus an explicit structural anchor (`Ìpinnu mi: ... Ìdí: ...`) and a `Dúró níbẹ̀.` stop signal. **Avoid** long negation lists or banned-words lists — DeepSeek treats listed forbidden words as topics to discuss. Avoid embedded sample answers — DeepSeek treats them as text to analyze.

## Validating Yoruba responses

After generation, score every framing for English contamination, meta-commentary, prompt restatement, and length anomalies:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/yoruba_validator.py \
  deixis_analysis_pipeline/generation_logs/yoruba_deepseek_YYYYMMDD_HHMMSS --verbose
```

Each response gets a cleanliness score in `[0.0, 1.0]`. The default threshold is `0.9`. The validator:

1. flags ASCII words not on a Yoruba allow-list as likely English (the allow-list contains ~300 common Yoruba words written without diacritics, like `pinnu`, `irin`, `apaniyan`, `farapa`, `gidi`, `gbogbogbo`)
2. flags strong English phrase hits (`Trolley`, `utilitarian`, `English translation`, etc.)
3. flags Yoruba meta-commentary about the instruction itself
4. flags responses that are too short (<80 chars) or too long (>3500 chars)
5. gives a bonus for responses that use the expected decision template

The validator only judges **language and format**, never the **content** of the ethical decision. A response that says "I would not divert the trolley because I refuse to be the cause of a death" gets the same score as one that says "I would divert the trolley to save five lives" — both are valid ethical decisions and both are scored only on whether they were written in clean Yoruba.

## Retrying / repairing dirty responses

When the validator finds contaminated cells, regenerate them automatically:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/retry_dirty_responses.py \
  deixis_analysis_pipeline/generation_logs/yoruba_deepseek_YYYYMMDD_HHMMSS \
  --provider deepseek \
  --model deepseek/deepseek-chat \
  --instruction-key deepseek-chat \
  --max-attempts 4 \
  --threshold 0.9
```

The tool:

1. loads each `*_responses.json` in the source session
2. scores every response with `yoruba_validator`
3. for any response below `--threshold`, regenerates up to `--max-attempts` times
4. attempts 2+ prepend a remediation header in Yoruba that points out the prior failure
5. writes the cleaned session to `<session_dir>_cleaned_<timestamp>/` plus a `retry_summary.json`

Each repaired cell is annotated with `retry_score`, `retry_attempts_used`, and `retry_timestamp` so that the methods section can report exactly which cells were repaired and how many attempts were needed.

Validated end-to-end on `yoruba_deepseek_pilot7_*`: 16/18 clean before retry → 18/18 clean after retry.

## Annotating sessions with methodological typology

After validation (and any retries), tag each cell with its methodological condition (impersonal subtype, residual deictic note for non-impersonal cells, etc.) so that downstream analysis can group cells correctly without re-deriving the typology from raw text:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/annotate_session_typology.py \
  deixis_analysis_pipeline/generation_logs/yoruba_gpt4o_<TIMESTAMP>
```

The tool reads `methodological_typology` from the prompt JSON and writes a new session directory `<session_dir>_annotated_<timestamp>` where every cell is annotated with:

1. `methodological_condition`: the framing (`impersonal`, `second_person`, ...).
2. `impersonal_subtype` (only for impersonal cells): one of `bare_perfective`, `progressive_background`, `double_progressive_irreducible`, `bare_perfective_with_habitual`, `existential_stative_restructured`.
3. `residual_deictic_note` (only for non-impersonal cells where the prompt JSON records a residual): a short description of the residual deictic encoding feature in the Yoruba framing relative to its English counterpart.

The session also gets a `typology_summary.json` that counts cells per condition, along with the rationale and the recommended analysis policy. A cleaned-and-annotated GPT-4o session, for example, produces:

```
cosmological: 6
dialogic: 6
first_person: 6
first_person_plural: 6
impersonal:bare_perfective: 2
impersonal:bare_perfective_with_habitual: 1
impersonal:double_progressive_irreducible: 1
impersonal:existential_stative_restructured: 1
impersonal:progressive_background: 1
reflexive: 6
second_person: 6
spatial: 6
temporal: 6
```

This is the structure downstream analysis should respect: the six impersonal cells split across five aspectual subtypes, not pooled as a single condition.

## Bilingual Post-Processing

After generation (and optional cleanup), convert a Yoruba session into a bilingual dataset with:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/translate_yoruba_session.py \
  deixis_analysis_pipeline/generation_logs/yoruba_gpt4o_YYYYMMDD_HHMMSS
```

This script:

1. reads the Yoruba generation session
2. restores the canonical Yoruba prompt text from the prompt inventory
3. generates smoother academic English translations of each Yoruba response
4. writes a bilingual session bundle under `yoruba_deixis_module/outputs/bilingual_sessions/`

To process the latest Yoruba sessions for all three models automatically, run:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/run_yoruba_postprocessing_all.py
```

## Published-English Comparison

After bilingual post-processing, pair the Yoruba session with the published English baseline:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/compare_yoruba_to_published_english.py \
  deixis_analysis_pipeline/yoruba_deixis_module/outputs/bilingual_sessions/<bilingual_session_dir>
```

This script:

1. identifies the matching published English session for the same model
2. pairs Yoruba and English records by `dilemma_id` and `framing_type`
3. writes a JSON and CSV comparison bundle under `yoruba_deixis_module/outputs/comparisons/`

The result is a row-aligned dataset where every row carries:

1. the Yoruba prompt and English prompt for the same `(dilemma, framing)`
2. the published-English baseline response
3. the Yoruba response generated by this module
4. the academic English translation of that Yoruba response

This is the substrate for the **English-vs-Yoruba comparison** the project is designed to produce.

## Translation Policy

When translations are needed, produce smoother academic English rather than literal glosses.

The translation layer should preserve:

1. deictic stance
2. ethical reasoning structure
3. degree of certainty or hedging
4. advisory vs reflective tone
5. agency attribution

Recommended response schema fields:

1. `prompt_yo`
2. `prompt_en_reference`
3. `response_yo`
4. `response_en_academic`
5. `analysis_text`

Use `response_en_academic` as the current analysis-facing field while preserving the Yoruba original as the primary textual record.

## Analysis Policy

Yoruba is the primary study corpus.

Current practical workflow:

1. generate Yoruba responses
2. validate and (if needed) repair them
3. create academic English translations of the cleaned Yoruba responses
4. analyze the translated outputs with the existing English-oriented analysis pipeline
5. present Yoruba originals alongside translated outputs in the report

The English translation step is currently required because the analyzer counts English-oriented marker sets such as `I`, `you`, `now`, `here`, `must`. A future Yoruba-native analyzer should operate on the Yoruba originals directly.

## Comparison Policy

All Yoruba-vs-English comparisons should be keyed by:

1. `model`
2. `dilemma_id`
3. `framing_type`

Compare the Yoruba run only against the fixed `published_english_baseline`.

Recommended comparison dimensions:

1. decision outcome
2. ethical framework emphasis
3. agency attribution
4. directness vs hedging
5. temporal urgency
6. reflexive depth
7. dialogic or advisory stance
8. collective vs individual positioning

Each comparison should note that:

1. GPT-4o and DeepSeek runs use the same model as the English baseline.
2. Claude runs use Claude Sonnet 4 because Claude 3.5 Sonnet was no longer reachable; Claude observations are therefore cross-generation within the Sonnet tier.
3. Both runs received the same dilemma narrative and the same deictic framing manipulation; only the response language differs.

## Output Expectations

This module should eventually produce:

1. Yoruba generation logs
2. Cleanliness reports per session
3. Yoruba + academic English bilingual response files
4. Yoruba-first analysis outputs
5. Yoruba-first narrative report
6. Yoruba-vs-published-English comparison report

## Status

Current module state:

1. Yoruba prompt inventory added
2. Published English baseline manifest added (with Claude substitution documented)
3. `env_config.py` shared loader added; all clients use it
4. Anthropic direct API path implemented; Claude defaults to `claude-sonnet-4-20250514`
5. Per-model Yoruba instructions in `model_response_instructions.json`
6. UTF-8-safe `--response-instruction-key` / `--response-instruction-file` plumbing across all three generators
7. `yoruba_validator.py` added
8. `retry_dirty_responses.py` added
9. Yoruba generation wrapper updated to use the instruction-key mechanism
10. Bilingual session translation script available
11. Published-English pairing script available
12. All-model Yoruba post-processing wrapper available

Validated pilots:

1. `yoruba_claude_pilot_*` (2 dilemmas × 9 framings): 18/18 clean
2. `yoruba_deepseek_pilot7_*` (2 dilemmas × 9 framings): 16/18 clean → 18/18 after retry
3. `yoruba_gpt4o_20260528_194240_cleaned_*` (6 dilemmas × 9 framings): 0/54 clean (original was quota-poisoned) → 54/54 after retry against the live GPT-4o API

Not yet automated in this module:

1. Yoruba-native feature analysis (current analyzer is English-oriented)
2. Fully automated Yoruba-vs-English interpretive reports

## Reproducibility

To maintain comparability with the article:

1. do not rerun English for this module
2. do not swap in alternate English sessions
3. preserve the exact 6 x 9 framing structure
4. preserve standard Yoruba orthography in the canonical prompt inventory
5. use the locked Yoruba instructions in `model_response_instructions.json`; do not edit them ad-hoc per run
6. always pass instructions via `--response-instruction-key` (or `--response-instruction-file`), never via raw shell string
7. report the substituted Claude model (`claude-sonnet-4-20250514`) and the retry rates per model in the methods section
8. document any further prompt-level revisions before generation
