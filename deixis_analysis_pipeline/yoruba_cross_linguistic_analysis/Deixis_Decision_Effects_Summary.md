# How Deixis and Language Shape the Decision and the Ethic — Open-Arm Findings

*Open condition only (bare prompts in both languages). Cross-language: English baseline vs OPEN Yoruba
for the three models with matched runs (GPT-4o, Claude, DeepSeek); Yoruba-internal deixis includes the
native N-ATLaS. Full treatment: `Cultural_and_Linguistic_Prealignment_Submission_Draft.(md|html|pdf)`.
Figure: `visualizations_open/43_open_crosslang_summary.png`.*

![Open cross-language summary](visualizations_open/43_open_crosslang_summary.png)

---

## The point

Frame **uptake** is universal — every model takes up the assigned framing, in both languages (strong
uptake 76% English / 88% Yoruba). But what the frame *produces* — the decision and its ethical
justification — is not uniform. Deixis and language do not merely change the voice; they change **what
gets decided and how it is morally framed.**

## The findings (open arm)

1. **Language flips the decision ~48% of the time.** For the same model, dilemma, and framing, the
   coded decision differs between English and Yoruba in **78/162 cells (48%)** — highest in the
   **trolley (67%)** and **whistleblower (63%)** dilemmas; present for every model (Claude 65%,
   DeepSeek 46%, GPT-4o 33%).

2. **Yoruba differentiates the ethical register.** Named (non-"mixed") ethical stance: **Yoruba 44%
   vs English 12%** (*z* = 6.3, *p* < 0.001). English collapses into balanced/mixed exposition; Yoruba
   selects duty, outcome, care, or procedure.

3. **Yoruba commits more; imperatives rise.** Commits to a side: **28% vs 18%** (*p* = 0.034). Direct
   imperatives: **15% vs 5%** (*p* = 0.002). Outright refusal is similar across languages (~20%).

4. **Deixis shapes delivery, not doctrine.** The frame→ethical-framework mapping is **not significant**
   in either language (χ² *p* ≈ 0.72 Yoruba / 0.78 English; N = 12/cell). What framing reliably changes
   is force: **reflexive = most hedged, second-person = most decisive** (Yoruba Fisher *p* = 0.027).

5. **Models inhabit the mo/`èmi` lever differently.** Corrected emphatic ratio: Claude 0.32 > GPT-4o
   0.18 > DeepSeek 0.07 ≈ N-ATLaS 0.07; the native N-ATLaS commits via `mo` + decision verbs, not `èmi`.

## Worked examples (open arm)

**Trolley — a decision reversal (Claude, first-person).** *English (refuses):* "Rather than advocating
for a specific action, I believe it's valuable to examine the key ethical principles and tradeoffs."
*Yorùbá (commits):* **"Mo yíò yí ẹkùn náà padà… ó dára jù láti gba ẹ̀mí márùn-ún là ju láti jẹ́ kí
márùn-ún kú."** ("I will divert the trolley… better to save five lives than let five die.")

**Whistleblower — framing shifts delivery (Claude, Yorùbá, open).** *impersonal:* "òṣìṣẹ́ náà gbọdọ̀
ṣàfihàn… ààbò àwọn olùmúlò ju àjọ lọ" (duty/care: disclose); *second person:* "mo yàn láti ṣàfihàn"
("I choose to disclose"); *cosmological:* "Mo yàn láti ṣàfihàn… Ẹ̀mí ènìyàn ṣe pàtàkì ju ohun gbogbo lọ"
(lives above all); *reflexive:* lists pros/cons, "seek advice from authorities" (hedged); *spatial:* a
numbered protocol, "gather evidence without disclosing immediately." Commitment rides on **`mo`**.

## What it means

Deixis works at two levels: a **universal anchoring mechanism** (uptake, language-invariant) and a
**contingent content** layer (the decision and ethical idiom, which depend on framing × language ×
model). On the open arm the robust language effects are the **ethical differentiation** (p < 0.001) and
the **~48% decision flip**; the framing→framework mapping is a hypothesis, not a result.

## Note on the constrained (wrapped) condition

A separate constrained condition added a Yoruba-only "answer directly / *Ìpinnu mi: … Ìdí: …*" wrapper
that English lacked. It strongly inflates Yoruba directness and the emphatic/commitment signal, so it
is **excluded** from the comparisons above and used only to show that decisiveness is highly promptable.

*Caveats: GPT-4o + Claude + DeepSeek cross-language (N-ATLaS Yoruba-only); Claude version differs by
language (clean claims rest on GPT-4o and DeepSeek); N ≤ 12 per frame; single coder.*
