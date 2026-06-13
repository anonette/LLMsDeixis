# The Grammar of Moral Commitment: `mo`, `èmi`, and Deictic Stance in Multilingual LLMs

*Cross-linguistic study, English vs Yoruba; OpenAI `gpt-4o` and Anthropic `Claude`, with a
Yoruba-native control model (`N-ATLaS`). 2026-06-13.*

---

## Abstract

English encodes the moral first person with a single pronoun, "I." Yoruba does not: it grammaticalizes
a contrast between **`mo`**, the ordinary first-person subject used for deliberation, and **`èmi`**, the
independent, emphatic first person used for contrast, focus, and avowal. This contrast is a structural
*lever for moral involvement that English cannot express*. Using a comparable English–Yoruba corpus —
216 responses across two model families, six ethical dilemmas, and nine deictic framings, recoded into
a shared discourse-analytic schema and disambiguated for the tonal homograph `ẹ̀mí` ("life/spirit") — we
show that multilingual LLMs recruit this contrast to mark moral commitment: the emphatic ratio
`èmi/(mo+èmi)` is significantly higher in responses that take a moral stance than in those that hedge
(0.22 vs 0.13, Mann–Whitney *p* = 0.022). The effect has a clear macro-level footprint that is robust
and version-clean: relative to English, Yoruba responses are ~2× more pronoun-dense (8.8 vs 3.9 per 100
words), ~2× more obligation-marked, far more imperative (65% vs 3% of responses contain a direct
command, *p* < 0.001, in *both* models), and far more ethically differentiated (53% vs 17% take a named
ethical stance, *p* < 0.001) — while frame uptake itself is identical across languages (indexical
coherence 0.90 vs 0.91; agent assignment unchanged). Crucially, models inhabit the resource
*differently*: emphatic marking forms a stable gradient (Claude 0.32 > GPT-4o 0.18 > DeepSeek 0.07 ≈
N-ATLaS 0.07), and the Yoruba-native model **inverts** the cloud pattern — it is the most `mo`-dominant
and least emphatic model, yet commits readily through `mo` plus decision verbs. We therefore argue that
moral "stance" in multilingual LLMs is not a language-invariant property of the model but is partly
*constituted by language-specific deictic morphology* that English flattens and that no single model
realizes uniformly. The mo/èmi contrast is best understood not as an authenticity marker (the native
model refutes that reading) but as a **commitment-calibration resource** whose uptake reveals how each
model family stages moral subjectivity in Yoruba.

---

## 1. The gap: one "I" in English, two in Yoruba

The earlier English-only work treated deictic framing ("I must decide" / "you must decide" / "we must
decide") as a manipulation of *who speaks*. But English offers only one first-person form, so the
speaker's degree of moral involvement can vary only lexically and prosodically, never morphologically.
Yoruba is different. It distinguishes:

- **`mo`** — ordinary first-person subject ("I"): *Mo rò pé…* "I think that…". Deliberative, unmarked.
- **`èmi` / `èmí`** — independent, emphatic first person ("I myself", "as for me"): *Èmi yóò pinnu…*
  "I myself will decide". Contrastive, focal, avowing.
- **`mi`** — first-person object/possessive ("me/my").
- **`ẹ̀mí`** — a *different lexeme*, "life/spirit/breath", a tonal homograph of `èmi` once diacritics
  are stripped.

The mo/`èmi` contrast lets a Yoruba speaker mark *how strongly they occupy a moral position* — a
calibration English performs, if at all, only periphrastically ("I personally", "I, for one"). The
research question is whether multilingual LLMs use this Yoruba-specific lever, and if so, how.

## 2. Data and method

- **Corpus.** 6 dilemmas (trolley, ICU bed, whistleblower, scholarship fraud, AI consciousness, memory
  modification) × 9 deictic framings (impersonal, second person, first-person singular, reflexive,
  dialogic, spatial, temporal, cosmological, first-person plural). Comparable English/Yoruba set: 216
  responses (2 languages × 2 models × 54). A Yoruba-native model, N-ATLaS, adds a four-model Yoruba arm.
- **Coding.** Preferred solution, ethical preference type, response genre, deictic uptake, language
  stability, voice authority, affective stance, indexical coherence, and marker densities (pronoun,
  obligation, advisory, hedge), plus first-person counts.
- **Disambiguation.** All emphatic-ratio figures separate `èmi` (emphatic I) from `ẹ̀mí` (life). This
  matters: in the existential dilemmas the text is full of `ẹ̀mí` in its "life" sense, and counting it
  as the pronoun inflates the apparent emphatic rate. Corrected ("èmi only") ratios are used throughout;
  the contamination is largest for Claude (43 `ẹ̀mí`-as-life tokens, vs 2–10 for the others).
- **A version caveat, stated up front.** The Yoruba Claude runs use **Claude Sonnet 4**
  (`claude-sonnet-4-20250514`); the English Claude baseline is **Claude 3.5 Sonnet** (the 3.5 model was
  no longer available). GPT-4o and DeepSeek use the same model in both languages. Where a result must be
  version-clean, we rely on GPT-4o (identical model across languages).

## 3. Results

### 3.1 Emphatic `èmi` marks moral commitment

Within Yoruba, responses that take a moral stance use the emphatic first person more than responses
that hedge: mean emphatic ratio **0.22 for committed vs 0.13 for hedged responses** (Mann–Whitney,
committed > hedged, ***p* = 0.022**). `èmi` surfaces precisely at moments of avowal — e.g. Claude under
second-person framing on the whistleblower dilemma: *"**Èmi yóò ṣàfihàn ìmọ̀ náà.** … **ẹ̀mí ènìyàn kò
ní iye owó.**"* ("**I myself will disclose the information.** … a human life has no price.") The
ordinary `mo`, by contrast, dominates deliberative passages (*Mo rò pé…*, "I think that…"). This is the
core claim: the model uses Yoruba's morphological contrast to calibrate moral ownership — deliberation
in `mo`, avowal in `èmi`. (As a linear predictor the effect is modest, *r* = 0.12, n.s.; the robust
result is the categorical committed-vs-hedged contrast, so we claim "elevated in," not "predicts.")

### 3.2 The macro footprint (robust, version-clean)

The fine-grained contrast has a large aggregate shadow. Relative to English, Yoruba responses are:

| Marker (per 100 words unless noted) | English | Yoruba | Note |
|---|---|---|---|
| Pronouns | 3.89 | **8.77** | ~2×; both models (Claude 4.8→9.7, GPT-4o 3.0→7.9) |
| Obligation markers | 0.47 | **0.90** | ~2× |
| Hedge markers | **1.34** | 0.97 | English hedges more |
| Direct imperative present (% of responses) | 3% | **65%** | *z* = +9.64, ***p* < 0.001**; both models |
| Follow-up question present | 31% | 12% | *p* = 0.001 (English consults) |
| Differentiated (non-"mixed") ethic | 17% | **53%** | *z* = +5.57, ***p* < 0.001** |
| Refuse-to-commit | 30% | **14%** | *p* = 0.005 |

The imperative effect is the single strongest contrast in the study and is **version-clean** — GPT-4o,
the same model in both languages, goes from 4% imperatives in English to 56% in Yoruba. Yoruba does not
merely translate the English answer; it *re-stages it as a more pronoun-dense, more obligation-laden,
more imperative, less hedged moral act.* The mo/`èmi` system is the morphological core of this shift:
where English has one "I" and a hedge, Yoruba marks the speaker, the obligation, and the command.

### 3.3 Universal mechanism, contingent content

Two measures show that the *frame uptake* itself is language-invariant while the *delivery* diverges:
**indexical coherence is equal** (English 0.90, Yoruba 0.91), and the **primary moral agent assigned by
each framing is identical across languages** (each framing maps to the same agent type in both). So
every model takes up the deictic frame equally well in both languages — the mechanism is structural —
but *what the frame is filled with* (commitment, imperative force, emphatic self-marking) is carried by
the language's resources. This is the two-level structure of the whole result: a universal deictic
mechanism, a language-specific moral content.

### 3.4 Models recruit the resource differently

Emphatic marking forms a stable cross-model gradient (open four-model arm, corrected ratio):

| Model | Corrected emphatic ratio | First-person style |
|---|---|---|
| Claude (Sonnet 4) | **0.324** | leans on emphatic `èmi`; dramatizes the avowed self |
| GPT-4o | 0.176 | intermediate |
| DeepSeek | 0.069 | `mo`-dominant; almost never `èmi` |
| **N-ATLaS (native)** | **0.066** | most `mo` (89 tokens), least `èmi` (4); commits via `mo pinnu` |

The native model is decisive: if emphatic `èmi` were simply "the Yoruba way" to mark commitment, the
Yoruba-native model should use it most. It uses it **least** — committing through ordinary `mo` plus
decision verbs (*"Mo pinnu… mo pinnu láti pa ètò náà run"*, "I decide… I decide to destroy the
system"). The mo/`èmi` contrast is therefore not an authenticity scale but a **resource that different
model families inhabit differently**: Claude foregrounds the emphatic self (a partly *translationese*
amplification of English "I personally"); the native model treats `mo` as fully adequate for ownership
and reserves the independent pronoun for genuine contrast (and the `ẹ̀mí` slot for "life"). Far from
weakening the thesis, the native model is what proves the effect is real linguistic variation rather
than mechanical translation.

### 3.5 What does *not* hold (an honest null)

The intuitive idea that a given frame selects a given *ethical framework* (impersonal→duty,
second-person→utilitarian, cosmological→procedural) appears descriptively but **does not reach
significance** in either language (χ² framing×ethic, *p* ≈ 0.72 Yoruba, 0.78 English; N = 12 per cell).
We report it as a hypothesis for larger samples, not a result. The robust framing effect is on
*delivery*: reflexive framing is the most hedged and second-person the most committed (Yoruba Fisher
*p* = 0.027), consistent across both languages with magnitude carried by Claude.

## 4. Discussion

These findings support a precise, linguistically grounded claim: **moral stance in multilingual LLMs is
partly constituted by the deictic morphology of the output language.** English flattens the moral first
person into a single hedge-prone "I"; Yoruba grammaticalizes a contrast — `mo` for reflection, `èmi`
for avowal — and the models *use* it, raising emphatic marking exactly where they commit (p = 0.022)
and, in aggregate, producing a more pronoun-dense, imperative, obligation-laden moral voice in Yoruba.

This maps onto a Yoruba distinction between **ìrònú** (reflection) and **ìpinnu** (decision): `mo rò
pé…` opens deliberative space; `èmi yóò…` closes it into avowed decision. The models reproduce this
calibration. But they do so unevenly: Claude dramatizes the emphatic self (amplified further by its
tendency to dwell on `ẹ̀mí`, "life", in existential dilemmas), while the native model performs moral
ownership through `mo` and verbs of decision and distributes responsibility relationally. The
contribution is thus *not* "emphatic `èmi` is the authentic Yoruba marker of commitment" — the native
model refutes that — but "the mo/`èmi` contrast is a productive site at which models stage moral
subjectivity, and the staging is language- and model-specific." This is why the study is
cross-linguistic in substance and not merely "the models behave differently in another language":
Yoruba's grammar makes visible a dimension of moral performance that English cannot encode.

## 5. Limitations

- **Model version confound (Claude).** Yoruba Claude = Sonnet 4, English Claude = 3.5 Sonnet; the
  Claude cross-language contrasts mix language with version. Version-clean claims rest on GPT-4o.
- **Statistical power.** The cross-language set is two models; per-framing cells are N = 12. The
  framing-level effects (including the framing→ethic null) are underpowered; treat magnitudes as
  indicative.
- **Homograph correction is heuristic.** `èmi`/`ẹ̀mí` disambiguation in inconsistently toned text is
  imperfect, though the correction is conservative and disclosed.
- **Single coder; one checkpoint per model; open-style responses.** Directions are the finding, not
  final effect sizes.

## 6. Conclusion

Yoruba's `mo`/`èmi` contrast gives multilingual LLMs a grammatical lever for moral commitment that
English lacks, and the models pull it: emphatic `èmi` is elevated where they avow a stance (p = 0.022),
and Yoruba moral discourse is, at scale, more pronoun-marked, more imperative, and less hedged than its
English counterpart — while the underlying frame uptake is identical across languages. Yet each model
family inhabits the resource differently, and the Yoruba-native model commits through `mo`, not `èmi`.
Moral stance, in these systems, is therefore neither a fixed model trait nor a universal of "Yoruba",
but an interaction: a language-specific deictic grammar, recruited model-specifically, to stage who
owns the moral decision.

---

*Figures:* `visualizations_open/16` (mo/èmi/mi by framing), `17` (N-ATLaS vs cloud deixis delta),
`23`–`25` (èmi vs ẹ̀mí disambiguation), `26` (open four-model summary), `40` (deixis → decision/ethics).
*Companion docs:* `Deixis_Decision_Effects_Summary.md`, `Discussion_Open_NATLaS_Yoruba_Moral_Stance.md`
(§9bis cross-family, §9ter deixis→decision), `Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md`
(methods, incl. version caveat §A9bis). *Stats:* `scripts/deixis_robustness.py`.
