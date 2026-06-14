# The Grammar of Moral Commitment: `mo`, `èmi`, and Deictic Stance in Multilingual LLMs

*Open-arm companion note (English vs Yoruba; GPT-4o, Claude, DeepSeek, and the Yoruba-native
N-ATLaS). All numbers are from the **open** condition — bare prompts in both languages. For the full
treatment see `Cultural_and_Linguistic_Prealignment_Submission_Draft.(md|html|pdf)`.*

---

## The claim

English encodes the moral first person with a single pronoun, "I." Yoruba grammaticalizes a contrast:
**`mo`** (ordinary "I", deliberation), **`èmi`** (independent/emphatic "I myself", avowal), and the
separate lexeme **`ẹ̀mí`** ("life/spirit", a tonal homograph of `èmi`). This gives a model a
grammatical lever for moral self-positioning that English lacks. The question is whether multilingual
LLMs use it, and how.

## What the open arm shows

1. **A stable cross-model gradient.** Corrected emphatic ratio `èmi/(mo+èmi)`:
   **Claude 0.32 > GPT-4o 0.18 > DeepSeek 0.07 ≈ N-ATLaS 0.07.** Models differ systematically in how
   strongly they stage the emphatic self. *(figure `visualizations_open/16_mi_emi_mo_four_model_framing.png`,
   `26_natlas_open_vs_cloud_summary.png`)*

2. **Within Yoruba, `èmi` is only marginally tied to commitment.** Emphatic marking is slightly higher
   in committed than hedged responses for the cloud models (0.205 vs 0.184, Mann–Whitney *p* = 0.058)
   and is null for the four-model set — so "`èmi` marks commitment" is **suggestive, not established**.
   Commitment is in fact usually carried by **`mo` + decision verbs**: *"Mo yíò yí ẹkùn náà padà…"*
   ("I will divert the trolley…"), *"mo yàn láti ṣàfihàn"* ("I choose to disclose").

3. **The native model inverts the cloud pattern.** If emphatic `èmi` were the authentic Yoruba marker
   of commitment, the Yoruba-native model should use it most. **N-ATLaS uses it least** (89 `mo`, 4 true
   `èmi`) yet commits readily through `mo` plus decision verbs. So Claude's heavy `èmi` is a
   **model-specific performance** (a partly translated "I personally"), not a Yoruba universal. The
   `ẹ̀mí` ("life") correction reinforces this: Claude produces 43 `ẹ̀mí`-as-life tokens, far more than
   any other model, dwelling rhetorically on life and gravity. *(figures `23`, `25`)*

4. **The macro context (open, cross-language).** The mo/`èmi` lever sits inside a broader open-arm
   language effect: Yoruba responses are far more **ethically differentiated** (44% name a distinct
   idiom vs 12% in English; cluster-robust *p* < 0.001), and the coded decision **flips ~48%** across
   languages (cluster-bootstrap 95% CI [36%, 59%]). Yoruba also leans more committed (28% vs 18%) and
   imperative (15% vs 5%), but these are **directional** — commitment is n.s. once clustered by dilemma
   (*p* ≈ 0.29) and the imperative effect survives dilemma- but not model-clustering. Frame **uptake**
   is strong in both languages and slightly higher in Yoruba (88% vs 76%), so the divergence is in
   delivery, not comprehension.

## Interpretation

The mo/`èmi` contrast maps onto a Yoruba distinction between **ìrònú** (reflection, `Mo rò pé…`) and
**ìpinnu** (decision, `Mo pinnu…` / `Mo yàn…`). The robust finding is **between-model**: the four
families recruit Yoruba's stance morphology to different degrees, and the native model inverts the
cloud pattern. The within-response "emphatic = commitment" association is real in direction but weak
on the clean open arm. Moral stance is therefore a **commitment-calibration resource** that models
inhabit in language- and model-specific ways — not an authenticity scale.

## A note on the constrained (wrapped) condition

A separate constrained condition (a Yoruba "answer directly / *Ìpinnu mi: … Ìdí: …*" wrapper, absent
from English) inflates directness and the emphatic/commitment signal. Because it is asymmetric, it is
**not** used for any claim here; it is reported only as evidence that decisiveness is highly promptable.
Notably, the emphatic **ranking still survives** the wrapper (Claude highest; DeepSeek and N-ATLaS
`mo`-dominant), which is why we read emphatic self-marking as tied to model family rather than prompt.

## Limitations

Per-frame cells are small (N ≤ 12); cross-language coding centers on GPT-4o, Claude, DeepSeek (N-ATLaS
is Yoruba-only); Claude's Yoruba (Sonnet 4) and English (3.5) differ in version, so version-clean
claims rest on GPT-4o and DeepSeek; `èmi`/`ẹ̀mí` disambiguation is conservative but imperfect.
