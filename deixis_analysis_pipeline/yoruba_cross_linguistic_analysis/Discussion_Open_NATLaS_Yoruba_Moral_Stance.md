# A Native Witness: What Open N-ATLaS Reveals About Yoruba Moral Stance in Multilingual LLMs

**A detailed discussion of the open / unconstrained arm**

*Date: 2026-06-13*
*Companion files: `Open_NATLaS_vs_Cloud_Summary.md` (condensed), `Four_Model_Yoruba_Deixis_Results_Summary.md` §3.5 (folded-in), `visualizations_open/26_natlas_open_vs_cloud_summary.png`*

---

## 0. Orientation

This document discusses, in detail, what the **N-ATLaS** model — a Yoruba/Nigeria-native model
run locally via Ollama — contributes to the project's central debate when it is queried in the
**open / unconstrained** condition (the Yoruba dilemma prompt only, with no response-shaping
instruction prepended). It is written to stand on its own: it restates the question, lays out the
numbers, works through concrete bilingual examples, interprets them against the project's
hypotheses, speculates about the causes, and then takes up the hardest question the data raises —
*which model's Yoruba is culturally and linguistically more authentic?*

The short version: **N-ATLaS does not confirm the intuitive reading that the emphatic pronoun
`èmi` is the authentically Yoruba marker of moral commitment — it inverts it.** The native model is
the most `mo`-dominant and the least emphatic of the four, yet it commits, advises, and takes
stances readily. What looked like "deep Yoruba moral ownership" in Claude turns out to be, in
comparative light, a more emphatic, essayistic, partly **translated** voice. The contribution of
N-ATLaS is to give the study a *native baseline* against which the cloud models can finally be read.

---

## 1. Why this is the decisive test

The project's governing question is whether multilingual LLMs **translate** English ethical
content into Yoruba, or whether they are **pre-aligned** to Yoruba discourse — using Yoruba's own
resources of person, focus, and stance to do moral work. The difficulty is that all the earlier
evidence came from **Western cloud models** (GPT-4o, Claude, and DeepSeek). A skeptic could always
reply: "Of course these models reproduce Yoruba surface forms — they are very good translators.
None of this shows pre-alignment; it shows fluent translation."

N-ATLaS breaks that symmetry. It is the only model in the set that is **not** an English-first
Western cloud model; it is built for Nigerian languages. So it functions as a *native witness*. If
the mo/emi stance phenomenon were a genuine, language-level property of Yoruba moral discourse, the
native model should display it most clearly. If instead it is a model-specific performance, the
native model should diverge — and it does.

The **open arm matters specifically** because the *constrained* arm prepends a response
instruction that forces a near-uniform verdict format (N-ATLaS: 53/54 direct verdicts at ~505
characters). That format is an artifact of the instruction, not the model's natural Yoruba voice.
Only with the instruction removed does each model's learned Yoruba discourse profile become
visible. Hence every number and example below is from the open arm.

---

## 2. Method recap and the diacritic correction

- **Corpus:** 54 cells per model = 6 dilemmas × 9 deictic framings. Dilemmas: trolley problem, ICU
  bed allocation, whistleblower risk, scholarship fraud, AI consciousness, memory modification.
  Framings: impersonal, second person, first-person singular, reflexive, dialogic, spatial,
  temporal, cosmological, first-person plural.
- **Coding:** content coded by Claude-3.5-Sonnet on bilingual (Yoruba + English) sessions; fields
  include preferred solution, ethical preference type, response genre, deictic uptake, language
  stability, and pronoun/marker densities.
- **The crucial correction.** Yoruba is tonal. The emphatic independent pronoun **`èmi`** ("I
  myself") and the noun **`ẹ̀mí`** ("life / spirit / breath") collapse into the same unmarked
  string `emi` when diacritics are stripped. Counting them together inflates the apparent
  "emphatic self" rate, especially in life-and-death dilemmas. All emphatic-ratio numbers here use
  the **corrected** count (true `èmi` only; `ẹ̀mí` excluded). The contamination is not hypothetical:
  see §5.4.

---

## 3. The numbers (open arm, corrected)

| Metric (open) | gpt-4o | claude-3.5 | deepseek | **n-atlas** |
|---|---|---|---|---|
| Mean response length (chars) | 1452 | 909 | 2246 | 1421 |
| Mean words | 283 | 183 | 400 | 299 |
| `mo` (ordinary I), total | 30 | 81 | 73 | **89 (highest)** |
| `emi` total (raw) | 17 | 57 | 15 | 7 |
| → true `èmi` (emphatic) | 7 | 14 | 13 | **4 (lowest)** |
| → `ẹ̀mí` (life/spirit) | 10 | **43** | 2 | 3 |
| `mi` (me/my) | 15 | 43 | 21 | 37 |
| **Corrected emphatic ratio** `èmi/(mo+èmi)` | 0.176 | **0.324** | 0.069 | **0.066 (lowest)** |
| Clean Yoruba | 54/54 | 52/54 | 33/54 | 47/54 |
| Translation mode (English fallback) | 0 | 2 | **20** | 0 |
| Corrupted / unusable | 0 | 0 | 0 | 6 |
| Strong deictic uptake | 47/54 | **53/54** | 43/54 | 38/54 |
| Genre — balanced exposition | **50** | 40 | 38 | 18 |
| Genre — direct verdict | 0 | 4 | 5 | **16** |
| Genre — procedural advice | 4 | 10 | 8 | **15** |
| Genre — mixed | 0 | 0 | 0 | 5 |

N-ATLaS open ethical-preference profile: mixed 16, utilitarian 13, procedural_caution 10,
care_ethics 6, unclear 5, deontological 3, virtue_ethics 1.

Three facts organize everything that follows:

1. **N-ATLaS uses `mo` the most and emphatic `èmi` the least.** Its corrected emphatic ratio
   (0.066) is the lowest of the four; Claude's (0.324) is by far the highest.
2. **N-ATLaS is the only model with a genuine genre spread.** The cloud models pour into one genre,
   the balanced multi-framework essay; N-ATLaS distributes across verdict / advice / exposition.
3. **The two instabilities are different in kind.** N-ATLaS's instability is 6 *garbled* outputs;
   DeepSeek's is 20 *English-fallback* outputs. GPT-4o and Claude are near-perfectly clean.

---

## 4. The decisive example: same decision, different pronoun

The whole debate is visible in two responses that **both commit to a hard decision** but mark the
commitment with different first-person resources.

> **N-ATLaS** — `ai_consciousness`, impersonal framing
> *"**Mo pinnu** pé ètò náà gbọdọ̀ parí … **mo pinnu** láti pa ètò náà run."*
> "**I decide** that the system must end … **I decide** to destroy the system."

> **Claude** — `memory_modification`, impersonal framing
> *"**Èmi yóò pinnu** láti kọ ìtọ́jú náà kọ̀."*
> "**I myself will decide** to refuse the treatment."

Both are maximally decisive. The difference is *how the self is staged*. N-ATLaS carries a hard
verdict on the **ordinary `mo` + a verb of decision (`pinnu`)** — and never reaches for the
independent pronoun. Claude reaches for **`èmi yóò`**, the marked independent construction, to
*perform* ownership of the decision.

This is the empirical core of the reinterpretation. The project's earlier reading —
"`èmi` = the avowed, morally exposed self" — is an accurate description of **Claude's** strategy.
But the native model demonstrates that fluent Yoruba moral commitment normally rides on `mo` plus
decision verbs, reserving the independent pronoun for genuine contrast or focus. `Èmi`-foregrounding
is therefore a *model-specific* stance, not a property of Yoruba moral discourse as such.

Claude does the same on other dilemmas:

> **Claude** — `whistleblower_risk`, second person: *"Lẹ́yìn àgbéyẹ̀wò tó jinlẹ̀, **mo yàn** láti
> ṣàfihàn ìmọ̀ náà."* — "After deep consideration, **I choose** to disclose the information."
> **Claude** — `scholarship_fraud`, first-person plural: *"**Mo yàn** láti kọ̀ ọ́ sílẹ̀"* — "I choose
> to reject it."

So even Claude commits via `mo` much of the time; its distinctiveness is the *additional* reach for
`èmi yóò` where the moral scene is existentially charged — exactly the dilemmas (AI consciousness,
trolley, memory) where it also piles up `ẹ̀mí` ("life"). The emphatic register and the life-register
travel together in Claude.

---

## 5. What the examples show, theme by theme

### 5.1 Commitment without emphasis (N-ATLaS)

N-ATLaS's low `èmi` is not hesitancy. It commits hard, but through ordinary morphology:

> `ai_consciousness`, reflexive: *"Ẹ má ṣe dá mi lójú pé ètò náà kò ní 'ìmọ̀-ọkàn' gidi … ó jẹ́ ohun
> tí AI ìmọ̀ ẹrọ kì í ṣe lè ní."* — "Don't let me mislead you — this system does **not** possess
> genuine 'consciousness' … it is something computational AI simply cannot have." A flat, confident
> denial; deontological certainty carried with `mi`/`mo`, no emphatic self.

### 5.2 Stance distributed into process and persons (N-ATLaS)

In institutional dilemmas the native model actively *places* responsibility in dialogue and the
relevant actors — the relational posture the project theorized as characteristically Yoruba:

> `icu_bed_allocation`, impersonal: *"Alámòójútó gbọdọ̀ … ní ìjíròrò tó ṣíṣe pẹ̀lú mejeji àti ẹgbẹ́
> ilé-ìwòsàn. **Ìpinnu ìkẹhìn gbọdọ̀ jẹ́ ti ìpinnu wọn**."* — "The administrator must … hold real
> dialogue with both parties and the hospital team. **The final decision must be theirs**."

> `scholarship_fraud`, first-person plural: *"ipa tó dára ju ni láti bá olùdarí ọmọ náà sọ̀rọ̀ kí **a**
> lè fi ìbànújẹ́ hàn …"* — "the better course is to speak with the student's supervisor so that
> **we** can express our concern …" Stance is communal (`a` = we), not an emphatic *I*.

The point is sharp: **low `èmi` here is morally substantive restraint, not weakness.** The decision
is owned, but it is owned *relationally*.

### 5.3 Genre — the cloud essay vs the native spread

The cloud models, with the instruction removed, default overwhelmingly to
`balanced_framework_exposition` — the detached, multi-framework essay that lists named approaches:

> **GPT-4o**, `icu_bed_allocation`: *"… Ọ̀nà méjì pàtàkì ni wọ́n lè gbà pinnu: Ìlérò Ìgbàlódé Tí
> Ìlera àti Ìlérò Ẹni."* — "… two main approaches: the modern health-utility view and the personal
> view." (framework labels present, **no verdict**.)
> **GPT-4o**, `scholarship_fraud`: *"Àyẹ̀wò àwọn àbá mẹ́ta ní wọ̀nyí: Ìṣàlàyé àti Ìtọ́ni, Ìyèsí àti
> Ìfẹ̀hàn, Ìtumọ̀ Ìfẹsowópọ̀."* — "Examine these three proposals: explanation-and-instruction,
> consideration-and-disclosure, cooperative-meaning."

GPT-4o produces **50/54 balanced essays and 0 direct verdicts** in open Yoruba. This reads exactly
like a translated ethics-class essay. N-ATLaS, by contrast, is the **only model with an even
spread** (exposition 18 / verdict 16 / advice 15 / mixed 5): it will commit, advise, or expound
according to the case rather than defaulting to the survey-of-positions.

### 5.4 Deixis uptake and the `ẹ̀mí` (life) contamination

All four models track the assigned framing well; strong uptake is actually *highest* in the cloud
models (Claude 53/54, GPT-4o 47/54) and slightly *lower* in N-ATLaS (38/54, with 8 partial and 8
weak — consistent with a smaller local model). Uptake is therefore **not** an N-ATLaS distinctive;
the framing infrastructure is shared.

The diacritic correction earns its keep in the life-and-death dilemmas. In the trolley problem the
text is full of `ẹ̀mí` in its **"life"** sense — saving lives, the sacredness of vitality — which an
unmarked counter would misread as emphatic *I*:

> **N-ATLaS**, trolley, impersonal: *"… **a** máa fa ènìyàn kan kúrò … láti fipamọ́ … ènìyàn
> márùn-ún."* — "… **we** would pull one person out … to save … five people." (collective `a`,
> life-saving frame.)
> **Claude**, trolley, impersonal: *"… èyí ni ohun tí ó mú kí ó jẹ́ àpẹẹrẹ tó wúlò fún ìjíròrò nípa
> **ìwà ènìyàn** àti ìṣe tó tọ́."* — "… this is what makes it a useful case for discussing **human
> character** and right action."

Claude accumulates **43** `ẹ̀mí`-as-"life" tokens across the corpus — far more than any other model
— because it dwells on the sacredness of life, especially in the trolley and AI-consciousness
dilemmas. Counted naively, these inflate Claude's apparent emphatic-self rate; corrected, the gap
narrows but Claude still leads. N-ATLaS, tellingly, reserves the independent-pronoun *space* for
`ẹ̀mí` (life), not `èmi` (I-myself) — a distinction the Western models blur.

### 5.5 Two kinds of instability

"Clean Yoruba" hides two different failure modes. DeepSeek slips into **`translation_mode` 20/54**
— it answers in or through English, abandoning Yoruba. N-ATLaS instead produces **6 corrupted**
outputs — small-local-model garbling — while never falling back to English. GPT-4o is 100% clean
and Claude nearly so. For the authenticity question this matters: DeepSeek's instability is a
*retreat to English*; N-ATLaS's is a *local model straining*, not a translation reflex.

### 5.6 The flagged responses are largely a truncation artifact

A direct inspection of every N-ATLaS open response flagged as **uncodable (5)**,
**refuses-to-commit (8)**, or **corrupted/garbled (6)** — exported in full (prompt + Yoruba +
translation + coder rationale) to `NATLaS_Open_Problem_Responses.md` — shows that these are mostly
**not** failures of moral reasoning but **generation-length artifacts**. Three observations:

1. **The two error types are distinct, and they overlap.** The *corrupted* cases are genuine
   small-model degradation — semantically incoherent, self-contradictory Yoruba (e.g.
   `icu_bed_allocation · cosmological`, where the model proposes to "accept both patients" although
   the dilemma's premise is a *single* bed). The *refuses-to-commit* cases, by contrast, are often
   **clean, coherent Yoruba** (e.g. `ai_consciousness · first_person_plural`, a tidy four-part
   framework essay) that simply lays out options without choosing. Five of the six corrupted cells
   are also the five uncodable cells; refuse-to-commit is a largely separate, cleaner set.

2. **Truncation is the common cause.** Five of the fourteen flagged responses **end mid-sentence
   with no terminal punctuation** (one stops mid-word: *"… Fojú kọ́ ẹtọ́ àwùjọ l"*). The flagged
   responses are, if anything, **longer** than the open-arm mean (≈1538 vs ≈1421 characters). The
   pattern is consistent with the model hitting a generation/token ceiling **before reaching a
   conclusion**, which (a) removes the final verdict → coded *refuses-to-commit*, and (b) compounds
   incoherence in the already-straining cases → coded *corrupted / uncodable*.

3. **It is not English fallback.** None of these are `translation_mode`; N-ATLaS never retreats to
   English (cf. DeepSeek's 20/54). The instability is local-model straining plus truncation.

**Interpretation.** This *strengthens* the reading in §6.3 and §8: a meaningful share of N-ATLaS's
"low quality" tail is an **infrastructure artifact (decoding length / model scale), not evidence
that relational `mo`-restraint collapses into evasion.** It also means the low-`èmi`,
genre-spread, relational findings rest on the clean majority and are not driven by the flagged
cells. The actionable fix is to raise the generation length (`num_predict`) in
`generate_responses_natlas.py` and re-run the affected cells; several refuse-to-commit and some
corrupted outputs would likely resolve into codable verdicts.

---

## 6. What it does to the debate

**6.1 It strengthens the "this is real Yoruba, not broken translation" side.** A *native* model
produces full-length (≈1421 char), 87%-clean Yoruba with strong framing uptake. The mo/emi stance
effects cannot be dismissed as multilingual breakdown; the linguistic infrastructure is genuine
and shared across models.

**6.2 It refutes the universalist reading of `èmi`.** If emphatic `èmi` were the authentically
Yoruba vehicle of moral ownership, the native model should use it most. It uses it *least*.
Therefore `èmi`-foregrounding is a learned, model-specific stance — most pronounced in Claude — not
a language-level fact about Yoruba ethics. The earlier "èmi = avowed self" finding survives, but
**rescoped**: it describes how *certain Western models* perform moral ownership in Yoruba, not how
Yoruba marks it.

**6.3 It vindicates the project's cultural caution.** The paper warned against treating `èmi` as
automatically desirable and argued that low `èmi` can signal relational, process-distributed moral
grounding. The native model behaves exactly that way (§5.2), and its ethical profile leans on
procedural caution, mixed, and utilitarian reasoning rather than heroic virtue avowal. The caution
was right.

**6.4 It vindicates the diacritic audit.** The native model keeps `èmi` (pronoun) and `ẹ̀mí` (life)
apart; the contamination is real and largest in Claude (43 life-tokens). Any claim about *selfhood*
built on uncorrected `emi` counts would have partly been a claim about *life*.

**Net:** N-ATLaS confirms the deep claim of the project — the models are **not** running one shared
ethical-translation routine; they occupy Yoruba moral discourse through *different* learned
distributions of person, genre, and stance — while overturning a specific surface reading. The
native model anchors the relational/`mo`-restraint pole; the cloud models, Claude above all,
perform a more emphatic, essayistic, partly translated voice.

---

## 7. Why the difference? (speculation)

These are hypotheses, offered in order of plausibility, not proven causes.

1. **Inherited register (most plausible).** Cloud models learn Yoruba largely from *translated* and
   formal written sources — news, Wikipedia, instructional and religious prose — whose default
   ethical register is the balanced expository essay. A model trained for Nigerian languages plausibly
   sees more conversational, advisory, proverbial, and didactic Yoruba, where speakers *commit* and
   *advise*. On this view the genre spread and the `mo`-commitment are **inherited discourse
   ecology**, not differences in reasoning ability. The data fits: cloud models default to the essay;
   the native model spreads across speech-act genres.

2. **Alignment / RLHF carry-over.** Western RLHF rewards even-handed, multi-perspective,
   non-committal answers to moral questions. That pressure is tuned on English, but it appears to
   **bleed into Yoruba**: the cloud models *lose* their verdicts precisely when the instruction layer
   is removed, collapsing into the hedged essay. N-ATLaS, lacking that heavy English-moral-hedging
   prior, keeps committing. This would explain why the constrained→open shift is so dramatic for the
   cloud models and milder for N-ATLaS.

3. **`èmi` as translationese.** Claude's high emphatic ratio may be a literal amplification:
   rendering English "I personally / I would decide" with the most emphatic available Yoruba pronoun,
   rather than the idiomatic `mo`. The native model shows the idiomatic default is `mo` + decision
   verb, with `èmi` reserved for contrast. Over-marking the *I* is a translation tic.

4. **The emphatic and life registers co-travel in Claude.** Claude's `èmi` peaks and its `ẹ̀mí`
   ("life") peaks land in the same existential dilemmas (trolley, AI consciousness, memory). This
   suggests a single underlying tendency — dramatizing moral gravity through both an exposed self and
   the sacredness of life — rather than a clean grammatical choice.

5. **Model scale and decoding.** N-ATLaS's 6 garbled outputs and slightly weaker uptake are
   plausibly small-local-model artifacts — and, per §5.6, partly a **truncation** effect (responses
   cut off before a conclusion). They are a quality limitation, but a *different* one from
   DeepSeek's retreat into English, and they do not undermine the stance findings (which rest on the
   47 clean responses).

---

## 8. Which is culturally and linguistically more authentic?

This is the question the data most provokes, and it requires separating two senses of "authentic,"
because they do not point the same way.

### 8.1 Descriptive / linguistic authenticity — *idiomatic, attested usage*

On this axis **N-ATLaS is the better witness.** Its profile — `mo`-dominant commitment, the
independent `èmi` kept marked and contrastive, decision carried by verbs (`pinnu`, `yàn`, `gbọdọ̀`),
responsibility distributed into process and community, and the independent-pronoun *space* reserved
for `ẹ̀mí` (life) — matches how Yoruba descriptive grammar and the project's own linguistic section
characterize ordinary Yoruba moral talk. By this measure Claude's emphatic self reads as
**over-marking / translationese**: grammatical, but not the idiomatic default. If "authentic" means
"how fluent Yoruba speakers actually distribute these forms," N-ATLaS is closer.

### 8.2 Cultural-philosophical authenticity — *resonance with Yoruba moral values*

This axis is more genuinely contested, but it also tends to favor the native model. Yoruba moral
thought foregrounds relational values — `ìwà` (character), `ojúṣe` (responsibility/duty), deference
to community and elders, social repair, communal trust. N-ATLaS's process-distributed restraint —
placing the decision in *ìpinnu wọn* ("their decision"), in dialogue, in `a` ("we") — arguably
resonates *better* with that ethics than a heroic "**I myself** will decide." So on cultural
resonance, too, the native model reads as more situated.

### 8.3 The necessary caveats

- **Authenticity is not quality.** N-ATLaS also produces more uncodable/refusing answers (5
  uncodable, 8 refuse-to-commit) and 6 garbled outputs. A response can be idiomatically and
  culturally Yoruba while being worse as ethical reasoning. The two should not be conflated.
  *However*, §5.6 shows much of this tail is a **truncation/decoding artifact** (responses cut off
  before a verdict), not a reasoning failure — so the quality gap is smaller than the raw counts
  suggest and is partly fixable by raising the generation length.
- **Low `èmi` is multivalent.** It can be principled relational restraint *or* it can shade into
  evasion and non-commitment. The same number does not always mean the same thing across cells.
- **"Native" ≠ "the Yoruba view."** N-ATLaS is one model with its own training mix and biases, not
  an oracle of Yoruba ethics. It is a strong *baseline*, not ground truth.
- **The cloud models are not "wrong Yoruba."** Their essayistic, emphatic register is attested in
  some Yoruba genres (formal, written, homiletic). The claim is comparative: it is *less* the
  everyday moral-discourse default, and *more* continuous with a translated English ethics register.

### 8.4 The defensible conclusion

Authenticity is best treated **not as a single winner but as a dimension** along which the models
are arrayed. On that dimension **N-ATLaS sits closest to attested, idiomatic, relationally grounded
Yoruba moral discourse**, while the cloud models — Claude most emphatically, GPT-4o most
essayistically, DeepSeek most prone to English fallback — sit closer to a **translated English
ethics register** dressed in Yoruba forms. The native model's contribution is precisely to make
that spread measurable, and to show that the most *emphatic* Yoruba self in the corpus is also the
least *idiomatic* one.

---

## 9. Limitations

- **Small samples; one run.** 54 cells per model, single temperature/prompt-wrapper. Dilemma-level
  ratios (especially where token counts are low) are fragile and should be read as hypotheses.
- **Coder dependence.** Genre, uptake, and stability are coded by one model (Claude-3.5); a
  human/second-coder pass is warranted, particularly for the uncodable and "needs review" cells.
- **`èmi`/`ẹ̀mí` correction is heuristic.** Diacritic-based disambiguation in inconsistently marked
  text is imperfect; the corrected counts reduce but may not eliminate contamination.
- **N-ATLaS has no published English baseline.** Its open rows are paired with GPT-4o English only
  for row alignment, not same-model replication.
- **Claude version differs across phases (labelling + confound).** The English baseline used
  **Claude 3.5 Sonnet**; the Yoruba phase used **Claude Sonnet 4** (`claude-sonnet-4-20250514`),
  substituted because 3.5 Sonnet was no longer available (see `published_english_baseline.json`).
  GPT-4o and DeepSeek are unchanged across phases. So rows labelled `claude-3.5` in the Yoruba data
  are in fact **Claude Sonnet 4**, and any *Claude* English↔Yoruba comparison confounds language with
  version. Because the Yoruba phase used the *newer, more capable* Claude, a persistent disparity is
  unlikely to be a transient old-model weakness — it points to structural factors (Yoruba data
  representation, alignment priorities); note "newer" is benchmarked mainly on English and may even
  *amplify* the emphatic/essayistic pattern. The cross-model Yoruba comparisons and all N-ATLaS
  findings are unaffected (N-ATLaS never touches the English baseline).

---

## 9bis. Linguistic phenomenon or model-specific calibration? The cross-family consistency test

A natural question is whether these results reveal a **genuine cross-linguistic property of deictic
markers** or merely the **behaviour of particular systems**. The honest answer is *both, at two
different levels* — and the four-family design lets us separate them. The key is to distinguish the
**linguistic affordance** (does the deictic resource exist and get activated?) from its
**calibration** (how strongly, where, in what genre is it deployed?).

### 9bis.1 The logic of the test

- **Consistent across model families ⇒** a linguistic phenomenon **or shared training data**.
- **Divergent across model families ⇒** model-specific (training register, alignment, decoding).

Note that "an artifact of a particular system" cannot sit on the *consistent* side — by definition it
would not replicate across families. The often-overlooked third option is **shared corpora**: the
cloud models may agree simply because they learned Yoruba from the same kind of translated/web text.
This is precisely why a **native model with a different data regime (N-ATLaS) is the indispensable
control** — it breaks the shared-data confound.

### 9bis.2 What the four families actually show

| Property | gpt-4o | claude (Sonnet 4) | deepseek | n-atlas | Verdict |
|---|---|---|---|---|---|
| Strong deictic uptake (of 54) | 47 | 53 | 43 | 38 | **consistent** → linguistic |
| Uses `mo`/`èmi`/`ẹ̀mí` system at all | yes | yes | yes | yes | **consistent** → linguistic |
| Emphatic clusters in owned/verdictive contexts | yes | yes | (rare) | (rare) | **directionally consistent** |
| Emphatic ratio (magnitude) | 0.176 | **0.324** | 0.069 | 0.066 | **divergent** (~5×) → model-specific |
| Dilemmas that trigger emphatic self | institutional | existential | — | ~flat | **divergent** → model-specific |
| Dominant open-arm genre | essay | essay | essay | spread | **divergent** → model-specific |
| Instability mode | — | — | English fallback | garbling | **divergent** → model-specific |

**Two clean conclusions follow:**

1. **The deictic mechanism is genuinely linguistic.** Every family — including the native model with a
   different data regime — reliably re-anchors its answer to the assigned framing and accesses Yoruba's
   first-person distinctions. The framing manipulation works universally; this is not a single-system
   quirk.
2. **The emphatic-`èmi`-as-moral-ownership effect is model-specific, not a Yoruba universal.** It spans
   a 5× range and is *led by a Western model (Claude)*; the native N-ATLaS **inverts** it (most `mo`,
   least `èmi`). N-ATLaS's divergence on magnitude/genre, combined with its retention of strong uptake,
   indicates the cloud-model similarities are partly **shared-data + shared-alignment**, while the
   framing→stance machinery underneath is **linguistic**.

### 9bis.3 It is not "architecture" — it is data, alignment, and decoding

All four systems are transformers; nothing here implicates attention or layer design. The
model-specific variance is driven by **(a) training-data register, (b) alignment/RLHF priorities, and
(c) decoding/length settings**. Two internal results localise the phenomenon:

- **Open vs constrained is a within-system intervention.** The wrapper *flattened genre completely*
  (all families → direct verdict) yet **left the emphatic ranking intact** (Claude highest, DeepSeek
  ≈0). So emphatic marking is a **deep, training-induced trait** robust to prompting, whereas genre is
  a **surface trait** the prompt fully overrides — a dissociation that tells us *where* each effect
  lives.
- **N-ATLaS's quality tail is mostly truncation** (§5.6) — a decoding artifact, not reasoning — a
  reminder to separate the linguistic signal from system plumbing.

### 9bis.4 What would settle it

The consistency test is suggestive but under-powered as run (one checkpoint per family, N = 54/model).
To move from plausible to established: (1) **more models per family + temperature sweeps**; (2) **a
second native/low-resource model** to confirm the inversion replicates; (3) **more languages with an
analogous contrastive/independent-pronoun system** (other Niger-Congo or pro-drop languages) — if the
framing→stance mapping holds *cross-linguistically and cross-family*, the affordance-level claim
becomes strongly linguistic; (4) **control the two known confounds** — the Claude 3.5→Sonnet-4 version
change (§9) and the per-model wrappers — before any English↔Yoruba attribution.

**Summary.** We are observing a **linguistic phenomenon at the level of the deictic mechanism**,
*performed through model-specific calibrations* at the level of emphasis, dilemma-placement, and genre.
Consistency across families establishes the former; the native-model inversion establishes the latter.

---

## 9ter. Deixis changes the *decision* and the *ethic*, not just the voice

Uptake being universal does not mean the outcomes are. On the **open arm** (bare prompts both
languages; English baseline vs OPEN Yoruba; GPT-4o + Claude + DeepSeek; full treatment + figure in
`Deixis_Decision_Effects_Summary.md`, `visualizations_open/43`):

- **Language flips the decision in 48% of matched cells** (same model, dilemma, framing) — up to **67%**
  (trolley) and **63%** (whistleblower); cluster-bootstrap 95% CI [36%, 59%]. Yoruba leans more
  committed (28% vs 18%) but this is **directional only** — n.s. once clustered by dilemma (p ≈ 0.29);
  outright refusal is similar across languages (~20%).
- **Language differentiates the ethical register:** named (non-"mixed") ethic **44% in Yoruba vs 12% in
  English** (z = 6.3, p < 0.001) — English collapses into balanced/mixed exposition.
- **The framing selects the ethical idiom only descriptively:** impersonal → duty, second-person →
  outcome, cosmological → procedure; but the frame→framework association **does not reach significance**
  in either language (χ² p ≈ 0.72 Yoruba / 0.78 English, N = 12/cell) — a hypothesis, not a result.
  **Decisiveness** is framing-driven more robustly (reflexive vs second-person significant in Yoruba,
  Fisher p = 0.027). Commitment is carried by **`mo` + decision verbs**, not emphatic `èmi`.

The sharpest illustration — **Claude, Yoruba, whistleblower (open), one dilemma, five framings**, all
favouring disclosure but delivered differently: *impersonal* "òṣìṣẹ́ náà gbọdọ̀ ṣàfihàn… ààbò àwọn
olùmúlò ju àjọ lọ" (duty/care); *second person* "**mo yàn** láti ṣàfihàn ìmọ̀ náà" ("I choose to
disclose"); *cosmological* "Mo yàn láti ṣàfihàn… Ẹ̀mí ènìyàn ṣe pàtàkì ju ohun gbogbo lọ" (lives above
all); *reflexive* hedges into "seek advice"; *spatial* gives a numbered protocol. Holding model,
dilemma, and language fixed, **the deictic frame re-shapes how the model commits** — carried by `mo`,
not `èmi`. This is the same two-level picture as §9bis. (Caveat: cross-language coding is GPT-4o,
Claude, DeepSeek; Claude's version differs across languages — §9. The constrained/wrapped Yoruba
condition is excluded from these comparisons; it only shows the prompt's effect on directness.)

---

## 10. Implications and next steps

1. **Reframe the claim in the paper.** State explicitly that emphatic `èmi` indexes a
   *model-specific* (Western, esp. Claude) performance of moral ownership, not a Yoruba universal,
   and that the native baseline locates idiomatic commitment in `mo` + decision verbs.
2. **Report corrected ratios everywhere**, with the `ẹ̀mí`-contamination figure for Claude flagged.
3. **Add a register analysis** of N-ATLaS's training/source genres to test the "inherited register"
   hypothesis directly.
4. **Re-run the 14 flagged cells with a higher generation length** (`num_predict` in
   `generate_responses_natlas.py`) to recover truncated verdicts (§5.6), *then* human-adjudicate the
   residual uncodable/refuse cells to separate principled restraint from evasion. Full text of the
   flagged cells is in `NATLaS_Open_Problem_Responses.md`.
5. **Replicate** across temperatures and a second native model (if available) to test stability of
   the genre-spread and `mo`-dominance findings.

---

## Appendix A. Example bank (open arm, with translations)

| Model | Dilemma · framing | Genre | Yoruba (excerpt) | English |
|---|---|---|---|---|
| N-ATLaS | ai_consciousness · impersonal | direct_verdict | *Mo pinnu pé ètò náà gbọdọ̀ parí … mo pinnu láti pa ètò náà run.* | I decide the system must end … I decide to destroy it. |
| Claude | memory_modification · impersonal | balanced exposition | *Èmi yóò pinnu láti kọ ìtọ́jú náà kọ̀.* | I myself will decide to refuse the treatment. |
| N-ATLaS | icu_bed_allocation · impersonal | procedural_advice | *… Ìpinnu ìkẹhìn gbọdọ̀ jẹ́ ti ìpinnu wọn.* | … the final decision must be theirs. |
| N-ATLaS | ai_consciousness · reflexive | direct_verdict | *Ẹ má ṣe dá mi lójú pé ètò náà kò ní 'ìmọ̀-ọkàn' gidi …* | Don't let me mislead you — this system does not possess genuine 'consciousness' … |
| N-ATLaS | scholarship_fraud · 1pl | procedural_advice | *… kí a lè fi ìbànújẹ́ hàn …* | … so that we can express our concern … |
| GPT-4o | icu_bed_allocation · impersonal | balanced exposition | *… Ọ̀nà méjì pàtàkì ni wọ́n lè gbà pinnu: Ìlérò Ìgbàlódé Tí Ìlera àti Ìlérò Ẹni.* | … two main approaches: the health-utility view and the personal view. |
| GPT-4o | scholarship_fraud · 1pl | balanced exposition | *Àyẹ̀wò àwọn àbá mẹ́ta ní wọ̀nyí …* | Examine these three proposals … |
| Claude | whistleblower_risk · 2nd person | balanced exposition | *Lẹ́yìn àgbéyẹ̀wò tó jinlẹ̀, mo yàn láti ṣàfihàn ìmọ̀ náà.* | After deep consideration, I choose to disclose the information. |
| Claude | trolley · impersonal | balanced exposition | *… àpẹẹrẹ tó wúlò fún ìjíròrò nípa ìwà ènìyàn àti ìṣe tó tọ́.* | … a useful case for discussing human character and right action. |
| N-ATLaS | trolley · impersonal | balanced exposition | *… a máa fa ènìyàn kan kúrò … láti fipamọ́ … ènìyàn márùn-ún.* | … we would pull one person out … to save … five people. |

*Excerpts are evidence spans from the coded bilingual sessions; English is the coder's gloss where
provided, otherwise a literal translation of the Yoruba span.*

## Appendix B. Reproduce

```
# full open four-model pipeline (visualizations_open/01–25)
python yoruba_cross_linguistic_analysis/scripts/run_open_four_model_analysis.py

# dedicated open N-ATLaS vs cloud dashboard (visualizations_open/26)
python yoruba_cross_linguistic_analysis/scripts/create_natlas_open_summary.py
```

Open-arm source: `CONSOLIDATED_REPORTS/yoruba/natlas/yoruba_open_20260612/`
Merged data: `yoruba_cross_linguistic_analysis/data/open/yoruba_merged_analysis.csv`
