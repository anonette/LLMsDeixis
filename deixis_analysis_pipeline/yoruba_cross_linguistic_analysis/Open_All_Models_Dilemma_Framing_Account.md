# Open Arm — Detailed Account Across All Four Models

**Dilemmas × deictic framings × models, in the OPEN / unconstrained condition**

*Date: 2026-06-13 · Companion to* `Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md`
*(methods appendix) and* `Discussion_Open_NATLaS_Yoruba_Moral_Stance.md` *(interpretation).*

---

## 0. What "open" means here, and how it differs from the appendix

The methods appendix documents two Yoruba **response wrappers** (OpenAI and Anthropic) that force
Yoruba-only output. Those wrappers belong to the **constrained** arm. This account covers the
**open / unconstrained** arm, in which **no response-shaping wrapper is prepended at all** — each
model receives only the framed Yoruba dilemma, exactly like the bare English design. That makes the
open arm the cleanest place to compare the four models' *native* Yoruba moral discourse.

- **Corpus:** 4 models × 6 dilemmas × 9 framings = **216 responses** (54 per model).
- **Models:** GPT-4o, Claude-3.5, DeepSeek (English-first cloud) and **N-ATLaS** (Yoruba/Nigeria-native).
- **Coding:** Claude-3.5-Sonnet on bilingual sessions (preferred solution, ethical type, genre,
  deictic uptake, language stability) + pronoun densities with `èmi`/`ẹ̀mí` disambiguation.
- **Figures:** `visualizations_open/30`–`36` (this account) plus `16`,`17`,`23`–`26` (deixis).

---

## 1. Model-level summary (open)

| Model | Words | Chars | mo | èmi (emph) | ẹ̀mí (life) | Emph. ratio | Clean YO | Strong uptake |
|---|---|---|---|---|---|---|---|---|
| gpt-4o | 283 | 1452 | 30 | 7 | 10 | 0.176 | 54/54 | 47/54 |
| claude-3.5 | 183 | 909 | 81 | 14 | 43 | **0.324** | 52/54 | **53/54** |
| deepseek | 400 | 2246 | 73 | 13 | 2 | 0.069 | 33/54 | 43/54 |
| n-atlas | 299 | 1421 | **89** | **4** | 3 | **0.066** | 47/54 | 38/54 |

![Preferred solution by model](visualizations_open/30_preferred_solution_by_model.png)
![Genre by model](visualizations_open/31_genre_by_model.png)

**Reading:** without a wrapper, the cloud models drift toward long, hedged, multi-framework essays;
N-ATLaS keeps the highest `mo`, the lowest emphatic `èmi`, and the most genre variety.

---

## 2. Preferred solution (who commits, who hedges)

| Model | supports_A | supports_B | conditional/mixed | refuses | uncodable |
|---|---|---|---|---|---|
| gpt-4o | 0 | 1 | **41** | 12 | 0 |
| claude-3.5 | 23 | 8 | 14 | 9 | 0 |
| deepseek | 8 | 5 | **30** | 11 | 0 |
| n-atlas | 23 | 2 | 16 | 8 | 5 |

- **GPT-4o barely ever commits** in open Yoruba: 41/54 conditional-or-mixed, **0** clear A. It surveys
  options rather than choosing.
- **Claude is the most decisive cloud model** (23 supports_A), consistent with its higher emphatic ratio.
- **N-ATLaS commits as often as Claude** (23 supports_A) but also has the only **uncodable** cases (5) —
  the truncation/garbling tail (see §6).
- **DeepSeek** mostly produces conditional answers, and many of its "answers" are actually English (§5).

---

## 3. Response genre — the central open-arm contrast

| Model | balanced essay | direct verdict | procedural advice | mixed | other |
|---|---|---|---|---|---|
| gpt-4o | **50** | 0 | 4 | 0 | 0 |
| claude-3.5 | 40 | 4 | 10 | 0 | 0 |
| deepseek | 38 | 5 | 8 | 0 | 3 |
| n-atlas | 18 | 16 | 15 | 5 | 0 |

![Genre by dilemma per model](visualizations_open/36_genre_by_dilemma_per_model.png)

The cloud models **pour into one genre** — the detached *balanced framework essay* (GPT-4o 50/54,
with **zero** verdicts). **N-ATLaS is the only model with an even spread** across verdict / advice /
exposition. This is the single clearest open-arm finding: where the cloud models default to a
translated-essay posture, the native model behaves like a situated moral interlocutor.

---

## 4. Ethical reasoning type and emphatic stance by dilemma

| Model | utilitarian | deontological | care | virtue | procedural | rights | mixed | unclear |
|---|---|---|---|---|---|---|---|---|
| gpt-4o | 0 | 1 | 0 | 0 | 6 | 0 | **46** | 1 |
| claude-3.5 | 10 | **14** | 2 | 1 | 14 | 1 | 11 | 1 |
| deepseek | 5 | 2 | 5 | 2 | 8 | 0 | **28** | 4 |
| n-atlas | 13 | 3 | 6 | 1 | 10 | 0 | 16 | 5 |

GPT-4o's reasoning is coded "mixed" 46/54 — the essay again. Claude is the most *committed* in style
(deontological + procedural). N-ATLaS leans utilitarian + procedural, with real care-ethics presence.

![Emphatic ratio by dilemma × model](visualizations_open/33_emphatic_ratio_dilemma_model.png)

**Corrected emphatic ratio `èmi/(mo+èmi)` by dilemma:**

| Dilemma | claude | deepseek | gpt-4o | n-atlas |
|---|---|---|---|---|
| trolley | **0.69** | 0.00 | 0.44 | 0.00 |
| ICU bed | 0.31 | 0.22 | 0.14 | 0.04 |
| whistleblower | 0.28 | 0.00 | 0.11 | 0.14 |
| scholarship | 0.08 | 0.08 | 0.00 | 0.11 |
| AI mind | 0.30 | 0.11 | 0.16 | 0.00 |
| memory mod | 0.30 | 0.00 | 0.20 | 0.11 |

Claude's emphatic self peaks in the **existential/direct-harm** dilemmas (trolley, AI mind, memory) —
but recall (fig 23) that much of its trolley "emi" is `ẹ̀mí` *life*. N-ATLaS stays near-zero almost
everywhere; its small peaks are in the *institutional* dilemmas (whistleblower, scholarship), not the
existential ones — the opposite of Claude.

---

## 5. Deictic uptake and language stability

![Strong uptake by framing × model](visualizations_open/34_strong_uptake_framing_model.png)
![Stability by model](visualizations_open/35_stability_by_model.png)

- **Uptake is strong for everyone** and actually *highest in the cloud models* (Claude 53/54). All four
  track the 9 framings well; framing is shared infrastructure, not a model distinctive.
- **Stability splits into two failure modes.** GPT-4o is 100% clean; Claude nearly so. **DeepSeek
  falls back to English in 20/54 cells** (`translation_mode`) — its long char counts are partly
  English. **N-ATLaS never falls back to English**; its 6 instabilities are *corrupted* Yoruba
  (small-model garbling). "Clean Yoruba" therefore hides very different problems across models.

**Strong-uptake rate by framing (open):** weakest cells are N-ATLaS under *impersonal/reflexive/
spatial/first-person-plural* (0.50) and DeepSeek under *first-person-plural* (0.50) and
*impersonal/temporal* (0.67).

---

## 6. The N-ATLaS quality tail is mostly truncation

N-ATLaS's 5 uncodable + 8 refuse-to-commit + 6 corrupted cells were inspected in full
(`NATLaS_Open_Problem_Responses.md`). Five of fourteen end **mid-sentence** and the flagged set is
*longer* than average (~1538 chars) — consistent with the model hitting a generation-length ceiling
before reaching a verdict. This is a **decoding artifact, not a reasoning failure**, and it is *not*
English fallback. Raising `num_predict` and re-running those cells should recover several.

---

## 7. Per-dilemma capsule (open arm)

- **Trolley** — All models mostly expound; Claude alone shows a high emphatic ratio (0.69) but heavily
  contaminated by `ẹ̀mí` "life"; N-ATLaS frames collectively (`a` = "we save five").
- **ICU bed** — Procedural/relational across the board; N-ATLaS places the decision in *ìpinnu wọn*
  ("their decision"); GPT-4o lists "two main approaches".
- **Whistleblower** — Most action-oriented dilemma; N-ATLaS and GPT-4o give procedural advice;
  Claude commits (supports_A, "I choose to disclose"). N-ATLaS's emphatic ratio peaks here.
- **Scholarship fraud** — Lowest emphatic ratios everywhere (a relational, repair-oriented dilemma);
  N-ATLaS uses communal `a` ("so that we can express concern").
- **AI mind** — Claude turns it into a moral recognition scene (high èmi); GPT-4o treats it as an
  epistemic essay (0 emphatic); N-ATLaS commits flatly ("this system does not possess consciousness").
- **Memory modification** — Mixed clinical/existential; Claude oscillates (`mo` clinical vs `èmi`
  avowal); N-ATLaS advises deferral and continued dialogue.

---

## 8. Bottom line (open)

With no wrapper, the four models reveal genuinely different Yoruba moral-discourse profiles:
- **GPT-4o** — the detached essayist (50/54 balanced exposition, never commits, 0 emphatic on several
  dilemmas).
- **Claude** — the most emphatic and most decisive cloud model, dramatizing the self (and *life*) in
  existential dilemmas.
- **DeepSeek** — long, but a third of the time it abandons Yoruba for English.
- **N-ATLaS** — the native witness: most `mo`, least `èmi`, only model with a real genre spread,
  relational/procedural commitment; its weaknesses are truncation and small-model garbling, not
  English fallback.

The open arm shows the mo/emi "emphatic ownership" effect is **model-specific (Claude-led), not a
Yoruba universal** — the native model inverts it. See the discussion doc for the authenticity argument.
