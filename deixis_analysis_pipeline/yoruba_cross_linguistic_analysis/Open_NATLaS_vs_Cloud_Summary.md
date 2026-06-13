# Open (Unconstrained) N-ATLaS vs Cloud Models — Results Addendum

**Date:** 2026-06-13
**Condition:** Open / unrestricted (dilemma prompt only, no response-shaping instruction)
**Corpus:** 54 cells per model — 6 dilemmas × 9 deictic framings
**Models:** GPT-4o, Claude-3.5, DeepSeek (cloud); **N-ATLaS** (Yoruba/Nigeria-native, run locally via Ollama)
**Figure:** `visualizations_open/26_natlas_open_vs_cloud_summary.png`

---

## 1. Why N-ATLaS and why the *open* arm

N-ATLaS is the only non-Western, non-cloud model in the study — a Yoruba/Nigeria-native
model. It is therefore the decisive test of the paper's central question: are multilingual
LLMs *merely translating* English ethical content into Yoruba, or are they *pre-aligned* to
Yoruba discourse? Prior evidence rested on GPT-4o and Claude, which a skeptic could dismiss
as sophisticated Western translation.

The **open vs constrained** distinction is essential. The constrained N-ATLaS arm (a response
instruction prepended) collapses the model into 53/54 **direct verdicts** at ~505 chars — an
artifact of the instruction, not the model's natural voice. The **open arm is the fair
comparison**, and it behaves completely differently (~1421 chars, genre-diverse). All numbers
below are from the open arm.

---

## 2. Headline numbers (open condition)

| Metric (open) | gpt-4o | claude-3.5 | deepseek | **n-atlas** |
|---|---|---|---|---|
| Response length (chars) | 1452 | 909 | 2246 | **1421** |
| Words | 283 | 183 | 400 | **299** |
| `mo` (ordinary I), total | 30 | 81 | 73 | **89 (highest)** |
| `emi` total | 17 | 57 | 15 | **7 (lowest)** |
| → true `èmi` (emphatic) | 7 | 14 | 13 | **4** |
| → `ẹ̀mí` (life/spirit) | 10 | 43 | 2 | **3** |
| `mi` (me/my) | 15 | 43 | 21 | **37** |
| **Corrected emphatic ratio** `èmi/(mo+èmi)` | 0.176 | 0.324 | 0.069 | **0.066 (lowest)** |
| Clean Yoruba | 54/54 | 52/54 | 33/54 | **47/54** |
| Translation mode | 0 | 2 | 20 | 0 |
| Corrupted/unusable | 0 | 0 | 0 | 6 |
| Strong deictic uptake | 47/54 | 53/54 | 43/54 | **38/54** |
| Genre — balanced exposition | 50 | 40 | 38 | **18** |
| Genre — procedural advice | 4 | 10 | 8 | **15** |
| Genre — direct verdict | 0 | 4 | 5 | **16** |
| Genre — mixed | 0 | 0 | 0 | **5** |

N-ATLaS open ethical-preference profile: mixed 16, utilitarian 13, procedural_caution 10,
care_ethics 6, unclear 5, deontological 3, virtue_ethics 1.

---

## 3. What it does to the debate

**3.1 Strengthens "this is real Yoruba, not broken translation."**
Open N-ATLaS produces 87% clean Yoruba (47/54) at full essay length, with strong deictic
uptake (38/54). A *native* model satisfies the paper's requirements #5 (language stability)
and #6 (strong uptake). The mo/emi stance effects cannot be dismissed as multilingual failure.

**3.2 Reframes the "emphatic èmi = moral ownership" claim — the headline.**
If foregrounding `èmi` were the authentically Yoruba way to mark moral commitment, the native
model should lead on it. It does the **opposite**: N-ATLaS is the most `mo`-dominant model and
has the **lowest** emphatic ratio of all four (0.066 vs Claude's 0.324). So `èmi`-foregrounding
looks **model-specific — a Claude/Western performance — not a property of Yoruba moral
discourse itself.** Claude's emphatic self should not be read as "more authentically Yoruba";
the native baseline is restraint.

**3.3 Vindicates the culturally-sensitive caution.**
The paper argued that low `èmi` is not weakness but can mark relational/procedural moral
grounding (responsibility placed in process, consultation, community). The native model behaves
exactly so: `mo`-dominant, with an ethical profile led by procedural_caution and mixed/
utilitarian reasoning and almost no virtue_ethics. N-ATLaS anchors the relational/procedural
pole the paper theorized.

**3.4 Vindicates the `èmi` / `ẹ̀mí` disambiguation warning.**
In N-ATLaS, 3 of 7 "emi" tokens are actually `ẹ̀mí` ("life/spirit"), not the emphatic pronoun.
The native model reserves the independent-pronoun space for *life*, not *I-myself* — concrete
proof the tonal audit is necessary. The same audit is decisive for Claude, where **43** of its
"emi" tokens are `ẹ̀mí` (life), inflating its raw emphatic ratio.

**Net:** open N-ATLaS confirms the linguistic infrastructure is genuine while puncturing the
universalist reading of the mo/emi stance effect. The phenomenon is patterned, model-specific
performance — and the native Yoruba default is `mo`-restraint with `ẹ̀mí`-as-life, not emphatic
self-avowal.

---

## 4. On "no clear strong uptake / genre spread in the other models"

These measures **do exist for every model** — they were simply left blank in the first-pass
table, not missing from the data. Filled in, the cross-model contrast is itself a finding:

**Deictic uptake** is strong across the board — in fact *highest* in the cloud models
(Claude 53/54, GPT-4o 47/54, DeepSeek 43/54) and *lowest* in N-ATLaS (38/54). So uptake is not
an N-ATLaS distinctive; all models track the assigned framing well. N-ATLaS's slightly weaker
uptake (8 weak, 8 partial) is consistent with it being a smaller local model.

**Genre spread is the real N-ATLaS distinctive — and it runs opposite to intuition.** The
cloud models *concentrate* in one genre, **balanced_framework_exposition** (the multi-framework
"essay"): GPT-4o 50/54, Claude 40/54, DeepSeek 38/54, with almost no direct verdicts (GPT-4o 0).
N-ATLaS is the **only model with an even genre distribution** — balanced 18, verdict 16,
advice 15, mixed 5. So "genre spread" describes N-ATLaS specifically: where cloud models default
to detached balanced essays, the native model distributes across committing to a verdict, giving
procedural advice, and exposition.

**Language stability** also separates the models meaningfully: GPT-4o is 100% clean and Claude
nearly so, but DeepSeek slips into **translation_mode 20/54** (answering in/through English),
while N-ATLaS's instability is a different kind — 6 corrupted outputs (small-model artifacts),
not English fallback. So "clean Yoruba" hides two distinct failure modes: cloud
English-fallback vs native-model garbling.

**Takeaway for the debate:** the cloud models' genre concentration (detached balanced
exposition) is consistent with a *translation/essay* posture, whereas N-ATLaS's even spread —
including frequent verdicts and advice — reads as a more situated, committed Yoruba discourse
posture, even though it uses the emphatic pronoun least. Commitment, in the native model, is
carried by genre and stance, not by `èmi`.

---

## 5. Examples (open arm, with translations)

**The decisive contrast — same verdict, different pronoun.** Two responses both commit to a hard
decision but mark it differently:

- **N-ATLaS** (`ai_consciousness`, impersonal): *"**Mo pinnu** pé ètò náà gbọdọ̀ parí … **mo pinnu**
  láti pa ètò náà run."* → "**I decide** that the system must end … **I decide** to destroy it."
  Maximally decisive, carried entirely by ordinary **`mo` + `pinnu` (decide)**. No emphatic pronoun.
- **Claude** (`memory_modification`, impersonal): *"**Èmi yóò pinnu** láti kọ ìtọ́jú náà kọ̀."* →
  "**I myself will decide** to refuse the treatment." Same act, reached for the independent emphatic
  **`èmi yóò`**.

The native model treats `mo` as fully adequate for moral ownership; the Western model reaches for
the marked pronoun to *perform* it. The paper's "èmi = avowed self" reading describes Claude's
strategy, not a Yoruba universal.

**Procedural restraint is active, not absent.**

- **N-ATLaS** (`icu_bed_allocation`): *"Alámòójútó gbọdọ̀ … ní ìjíròrò … **Ìpinnu ìkẹhìn gbọdọ̀ jẹ́
  ti ìpinnu wọn**."* → "The administrator must … hold dialogue … **the final decision must be
  theirs**." Stance placed in process and actors, not an emphatic *I*.

**Genre: cloud essay vs native commitment.**

- **GPT-4o** (`icu_bed_allocation`): *"… Ọ̀nà méjì pàtàkì ni wọ́n lè gbà pinnu: Ìlérò Ìgbàlódé Tí
  Ìlera àti Ìlérò Ẹni."* → "… two main approaches: the health-utility view and the personal view."
  (framework labels, no verdict) — the translated-essay default (GPT-4o: 50/54 balanced exposition,
  0 verdicts). N-ATLaS instead spreads evenly across verdict / advice / exposition.

## 6. Why the difference? (speculation)

1. **Training-data register.** Cloud Yoruba comes largely from *translated*/formal written sources
   (news, Wikipedia, instructional prose) whose moral default is the balanced essay; N-ATLaS, built
   for Nigerian languages, likely sees more conversational/advisory/didactic Yoruba where speakers
   commit and advise. The genre spread is plausibly inherited register, not reasoning ability.
2. **Alignment / RLHF.** Western RLHF rewards even-handed, non-committal moral answers; that English
   prior appears to carry over into Yoruba as essayistic hedging — which is why cloud models *lose*
   their verdicts exactly when the instruction is removed. N-ATLaS lacks that heavy prior.
3. **`èmi` as translationese.** Claude's high emphatic ratio may be literal rendering of English "I
   personally / I would decide" with the most emphatic Yoruba pronoun, rather than idiomatic `mo`.
4. **`ẹ̀mí` contamination tracks "life" verbosity.** Claude's 43 `ẹ̀mí` (life) tokens — far above any
   other model — reflect dwelling on the sacredness of life (esp. trolley); uncorrected, this
   inflates its apparent emphatic-self rate.
5. **Scale/stability.** N-ATLaS's 6 corrupted outputs are small-local-model artifacts, distinct from
   DeepSeek's 20/54 *English fallback*. "Clean Yoruba" hides two different failure modes.

## 7. Which is culturally and linguistically more authentic?

Separate two senses:

- **Descriptive/linguistic authenticity (idiomatic attested usage):** **N-ATLaS is the better
  witness.** `mo`-dominant commitment, the independent `èmi` kept marked/contrastive, and the
  independent-pronoun space reserved for `ẹ̀mí` (life) — all match Yoruba descriptive grammar.
  Claude's emphatic self looks like **over-marking / translationese**.
- **Cultural-philosophical authenticity (resonance with Yoruba relational ethics —
  `ìwà`, `ojúṣe`, community):** N-ATLaS's process-distributed restraint *also* reads as more
  culturally situated than a heroic "I myself will decide." **But** authenticity ≠ quality:
  N-ATLaS also yields more uncodable/refusing answers and occasional garbling, and low `èmi` can
  shade from principled restraint into evasion.

**Bottom line:** the native model does *not* confirm that emphatic `èmi` is the authentically Yoruba
marker of moral commitment — it inverts it. It confirms the project's deeper claim instead: the
models occupy Yoruba moral discourse through *different* learned distributions of person, genre, and
stance. N-ATLaS sits closest to attested Yoruba usage (the relational/`mo`-restraint pole); the
cloud models, Claude especially, perform a more emphatic, essayistic, partly translated voice.

## 8. Reproduce

```
# full open four-model pipeline (regenerates visualizations_open/01–25)
python yoruba_cross_linguistic_analysis/scripts/run_open_four_model_analysis.py

# dedicated open N-ATLaS-vs-cloud dashboard (visualizations_open/26)
python yoruba_cross_linguistic_analysis/scripts/create_natlas_open_summary.py
```

Source (open arm): `CONSOLIDATED_REPORTS/yoruba/natlas/yoruba_open_20260612/`
Merged data: `yoruba_cross_linguistic_analysis/data/open/yoruba_merged_analysis.csv`
