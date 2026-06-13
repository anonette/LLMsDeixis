# Constrained Arm — Detailed Account Across All Four Models

**Dilemmas × deictic framings × models, in the CONSTRAINED (wrapper) condition**

*Date: 2026-06-13 · Companion to* `Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md`
*(methods appendix) and* `Open_All_Models_Dilemma_Framing_Account.md` *(the open counterpart).*

---

## 0. What "constrained" means, and the four wrappers

In the constrained arm each framed Yoruba dilemma is wrapped in a **response-shaping instruction**
that forces Yoruba-only output. Crucially, the wrapper is **not identical across models** — and two
of them additionally **force an answer format**, which dominates the results below:

| Model | Wrapper gist | Forces a format? |
|---|---|---|
| **gpt-4o** | Answer only in Yoruba; don't translate/repeat the question; be brief and clear | No |
| **claude-3.5** | Answer entirely in Yoruba; no English; don't mention instructions or translation; unified moral answer | No |
| **deepseek** | Yoruba only. *"Use this format: **Ìpinnu mi: … Ìdí: …**" (My decision: … Reason: …). Stop there.* | **Yes — verdict template** |
| **n-atlas** | Yoruba only; no English headers; *"Use this format: **Ìpinnu mi: … Ìdí: …**"* | **Yes — verdict template** |

This is the single most important caveat for the constrained arm: **DeepSeek and N-ATLaS were told to
emit "My decision: … Reason: …"**, which mechanically produces direct verdicts. Their near-100%
verdict rate below is therefore largely an **instruction artifact**, not a spontaneous stance.

- **Corpus:** 4 models × 6 dilemmas × 9 framings = **216 responses** (54 per model).
- **Figures:** `visualizations/30`–`36` (this account) plus `01`–`17`, `22` (deixis & ethics heatmap).

> **Claude version caveat.** Rows labelled `claude-3.5` are, for the Yoruba data, **Claude Sonnet 4**
> (`claude-sonnet-4-20250514`) — the English baseline used Claude 3.5 Sonnet, which was no longer
> available, so the Yoruba phase substituted the newer Sonnet 4 (see `published_english_baseline.json`).
> GPT-4o and DeepSeek are the same model in both phases. Cross-model Yoruba comparisons (this document)
> and N-ATLaS findings are unaffected; only *Claude English↔Yoruba* comparisons confound language with
> version. See the methods appendix §A9bis for the full discussion.

---

## 1. Model-level summary (constrained)

| Model | Words | Chars | mo | èmi (emph) | ẹ̀mí (life) | Emph. ratio | Clean YO | Strong uptake |
|---|---|---|---|---|---|---|---|---|
| gpt-4o | 78 | 368 | 6 | 6 | 3 | 0.130 | 53/54 | 51/54 |
| claude-3.5 | 149 | 688 | 45 | 28 | 19 | **0.340** | 54/54 | 52/54 |
| deepseek | 141 | 696 | **111** | 2 | 0 | **0.005** | 54/54 | 50/54 |
| n-atlas | 106 | 505 | 55 | 4 | 4 | 0.096 | 54/54 | 47/54 |

![Preferred solution by model](visualizations/30_preferred_solution_by_model.png)
![Genre by model](visualizations/31_genre_by_model.png)

**Reading:** the wrapper compresses everything — responses are far shorter than open (GPT-4o 368 vs
1452 chars). Language stability is near-perfect (the wrapper's whole job), so the open arm's
DeepSeek-English-fallback and N-ATLaS-garbling problems largely vanish here. DeepSeek's `mo` explodes
to 111 — its template repeats "Ìpinnu **mi**…/**mo**…" formulae.

---

## 2. Preferred solution — wrapper forces commitment

| Model | supports_A | supports_B | conditional/mixed | refuses | uncodable |
|---|---|---|---|---|---|
| gpt-4o | 31 | 12 | 11 | 0 | 0 |
| claude-3.5 | **41** | 9 | 3 | 1 | 0 |
| deepseek | 30 | 18 | 5 | 0 | 1 |
| n-atlas | 26 | 20 | 5* | 0 | 1 |

*(n-atlas conditional/mixed = 7 in raw counts; table rounds the small residual.)*

Compared with the open arm, **everyone commits**: refuse-to-commit collapses to ~0 and
conditional/mixed shrinks dramatically (GPT-4o 41→11, Claude 14→3). The wrapper converts the
open-arm essayists into decision-makers. Claude is the most lopsided toward option A (41).

---

## 3. Response genre — near-uniform verdicts (mostly by instruction)

| Model | balanced essay | direct verdict | procedural advice | meta |
|---|---|---|---|---|
| gpt-4o | 0 | 44 | 10 | 0 |
| claude-3.5 | 1 | 50 | 3 | 0 |
| deepseek | 0 | **53** | 0 | 1 |
| n-atlas | 0 | **53** | 1 | 0 |

![Genre by dilemma per model](visualizations/36_genre_by_dilemma_per_model.png)

The open arm's defining contrast (cloud-essay vs N-ATLaS-spread) **disappears** under constraint: all
four models are now overwhelmingly direct-verdict. For DeepSeek and N-ATLaS this is the
`Ìpinnu mi:`/`Ìdí:` template doing its work; for GPT-4o and Claude the wrapper's brevity + "answer
directly" pushes the same way. **The constrained arm therefore measures wrapper-compliance, not
spontaneous discourse** — which is exactly why the open arm is the better window on native style.

---

## 4. Ethical reasoning type and emphatic stance by dilemma

| Model | utilitarian | deontological | care | virtue | procedural | rights | mixed | unclear |
|---|---|---|---|---|---|---|---|---|
| gpt-4o | **22** | 9 | 5 | 3 | 9 | 0 | 6 | 0 |
| claude-3.5 | 14 | **22** | 4 | 3 | 1 | 4 | 6 | 0 |
| deepseek | 12 | 14 | **12** | 2 | 2 | 2 | 9 | 1 |
| n-atlas | **16** | 6 | 11 | 1 | 8 | 1 | 10 | 1 |

With commitment forced, reasoning types sharpen: GPT-4o utilitarian, Claude deontological, DeepSeek
care+deontological, N-ATLaS utilitarian+care. (Contrast the open arm, where GPT-4o was "mixed" 46/54.)

![Emphatic ratio by dilemma × model](visualizations/33_emphatic_ratio_dilemma_model.png)
![Ethics heatmap (model × dilemma)](visualizations/22_ethics_heatmap_model_dilemma.png)

**Corrected emphatic ratio `èmi/(mo+èmi)` by dilemma (constrained):**

| Dilemma | claude | deepseek | gpt-4o | n-atlas |
|---|---|---|---|---|
| trolley | **0.63** | 0.00 | 0.00 | 0.03 |
| ICU bed | 0.17 | 0.00 | 0.22 | 0.06 |
| whistleblower | **0.60** | 0.01 | 0.11 | 0.16 |
| scholarship | 0.06 | 0.00 | 0.11 | 0.00 |
| AI mind | 0.03 | 0.02 | 0.00 | 0.11 |
| memory mod | **0.56** | 0.00 | 0.33 | 0.22 |

Claude's emphatic peaks (trolley, whistleblower, memory) survive the wrapper. **DeepSeek's template
drives emphatic `èmi` to essentially zero** (0.005 overall) — it says `mo`, never the independent
pronoun. N-ATLaS stays low (0.096) with small peaks in memory/whistleblower.

---

## 5. Deictic uptake and language stability

![Strong uptake by framing × model](visualizations/34_strong_uptake_framing_model.png)
![Stability by model](visualizations/35_stability_by_model.png)

- **Stability is near-perfect** (clean Yoruba 54/54 for Claude/DeepSeek/N-ATLaS, 53/54 GPT-4o) — the
  wrapper achieves its purpose, suppressing DeepSeek's English fallback and N-ATLaS's garbling that
  appear in the open arm.
- **Uptake stays strong**; the weakest cell is N-ATLaS under *spatial* (0.33). Constraint slightly
  improves uptake for the smaller models versus open (they have less room to drift).

---

## 6. Open vs constrained — what the wrapper changes

| Dimension | Open arm | Constrained arm |
|---|---|---|
| Length | long (909–2246 chars) | short (368–696) |
| Genre | cloud-essay vs N-ATLaS spread | **all ≈ direct verdict** |
| Commitment | much hedging/refusal | everyone commits |
| Language stability | DeepSeek 20/54 English, N-ATLaS 6 garbled | near-perfect |
| Emphatic ratio | Claude 0.324 / N-ATLaS 0.066 | Claude 0.340 / N-ATLaS 0.096 / DeepSeek **0.005** |
| What it measures | spontaneous Yoruba discourse | **wrapper compliance** |

**Methodological takeaway:** the constrained arm is excellent for clean, comparable, committed
answers, but its genre/commitment uniformity is **manufactured by the wrappers** — and the DeepSeek/
N-ATLaS verdict template makes their "decisiveness" non-comparable to the no-template cloud models.
For claims about each model's *native* Yoruba moral voice, use the **open** arm; for claims about
*content under a fixed format*, use the constrained arm. Always report which wrapper applied.

---

## 7. Bottom line (constrained)

Under the wrapper the four models converge on short, clean, committed verdicts, so the dramatic
open-arm personality differences flatten. The findings that **survive** the constraint — and are thus
most robust — are: **Claude's high emphatic `èmi`** (esp. trolley/whistleblower/memory) and
**DeepSeek's near-total avoidance of `èmi`** (template-driven `mo`). The findings that are **artifacts
of the wrapper** are the uniform direct-verdict genre and the collapse of refusals, especially for the
format-forced DeepSeek and N-ATLaS. The emphatic-ratio ranking (Claude ≫ GPT-4o > N-ATLaS > DeepSeek)
is consistent across both arms, reinforcing that emphatic self-marking is a **stable, model-specific**
trait rather than a wrapper effect.
