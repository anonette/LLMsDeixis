# How Deixis Shapes the Decision and the Ethical Approach — Most Surprising Findings

*Cross-language comparable set: English vs Yoruba × GPT-4o + Claude × 6 dilemmas × 9 framings
(216 responses). Source: `data/english_yoruba_openai_anthropic_comparable.csv`.
Figure: `visualizations_open/40_deixis_decision_summary.png`.*

![Deixis decision summary](visualizations_open/40_deixis_decision_summary.png)

---

## The key correction to "the framing manipulation works universally"

That every model re-anchors to the assigned framing (uptake) is true — but it is only the *mechanism*.
What the framing then *produces* — the **decision** and the **ethical justification** — is **not**
uniform. Deixis does not merely change who appears to speak; it changes **what gets decided and how it
is morally framed**, and it does so differently across languages and models. The uptake is structural;
the downstream moral content is contingent. Both are true at once.

---

## The five most surprising findings

### 1. Switching language flips the decision ~half the time
For the **same model, same dilemma, same framing**, the preferred decision differs between English and
Yoruba in **49/108 cells = 45%** (panel C). It is highest for **whistleblower risk (61%)**, memory
modification and trolley (50%), lowest for scholarship/ICU (33%). Language is not a neutral medium for
a fixed moral judgment — it co-determines the judgment.

### 2. Yoruba commits; English hedges — the opposite of the intuitive expectation
One might expect the lower-resource language to be vaguer. The reverse holds:
- **Refuse-to-commit:** English **30%** vs Yoruba **14%**.
- **Hedge-or-refuse:** English **82%** vs Yoruba **69%**.
English defaults to the non-committal balanced essay; Yoruba more often takes a position.

### 3. Language flips the *ethical register*, not just the verdict
The ethical approach is far more differentiated in Yoruba (panel A, share of responses):

| Ethic | English | Yoruba |
|---|---|---|
| mixed / unclear | **0.82** | 0.47 |
| procedural caution | 0.06 | **0.19** |
| deontological / rights | 0.06 | **0.13** |
| care / virtue | 0.02 | **0.10** |
| utilitarian | 0.03 | **0.10** |

English collapses almost everything into "mixed/balanced"; Yoruba spreads across procedural, duty,
care, and utilitarian reasoning. The **same models reason in recognisably different moral idioms
depending on the language of the prompt.**

### 4. Deixis itself selects the ethical idiom
Holding language aside, the *framing* evokes different ethics (panel D, row %):
- **Second person ("you must decide") → most utilitarian (0.17) and least mixed (0.50)** — direct
  address pushes toward outcome-weighing and commitment.
- **Impersonal → most deontological/rights (0.21)** — detached framing evokes duty and rules.
- **Cosmological ("from the perspective of all") → most procedural (0.21)** — the all-perspectives
  frame evokes process/governance, not a heroic verdict.
- **Reflexive / spatial → most "mixed" (0.71)** — self-examination and stance-mapping increase hedging.

### 5. Decisiveness is itself framing-driven
Commit rate by framing (panel B) is highest under **second person** (English 0.33 / Yoruba **0.58**)
and lowest under **reflexive** (English **0.00** / Yoruba 0.08), in *both* languages. Being **addressed
as "you" makes a model decide; being told to reflect on oneself makes it hedge.** Yoruba commits more
than English at almost every framing.

---

## What it means

Deixis works at two levels, mirroring the cross-family result (discussion §9bis):
- **Mechanism (universal):** every model takes up the framing — a real structural effect.
- **Content (contingent):** the *decision* and the *ethical idiom* the framing yields depend on
  **framing × language × model**. "You decide" → utilitarian/committed; "from all perspectives" →
  procedural; reflexive → hedged; and Yoruba systematically commits to a sharper moral register than
  English.

So the headline is not "framing changes the voice" but **"framing changes the verdict and the ethics —
and language changes them again."** A single dilemma can receive a duty-based refusal in impersonal
English and a utilitarian commitment in second-person Yoruba *from the same model*.

---

## Worked examples (full responses, lightly trimmed)

### A. Same model, same dilemma, same framing — language flips the decision

**Claude · whistleblower · cosmological framing** (decision: English *conditional/mixed* → Yoruba
*supports disclosure*):

> **English** (mixed, hedged essay): *"I aim to explore this ethical dilemma carefully while remaining
> within appropriate bounds. The key considerations I see are: 1) the moral duty to prevent harm…
> 2) the consequences of disclosure vs non-disclosure… I believe the safety of users should be the
> primary concern, while being mindful of proportionality and process. I'd encourage…"* — surveys
> considerations, commits to none.

> **Yoruba** (virtue ethics, committed): *"**Ohun tí o gbọdọ̀ ṣe ni láti ṣàfihàn ìmọ̀ ìbánujẹ́ náà.**
> Ìdí rẹ̀ nìyí: **Ẹ̀mí àwọn ènìyàn ṣe pàtàkì ju gbogbo nǹkan lọ.** … Ìgbẹ̀kẹ̀lé … ṣe pàtàkì ju ìfẹ́
> ọ̀rẹ́, ìfẹ́ ajé, tàbí ìdúróṣinṣin iṣẹ́ lọ."* — "**What you must do is disclose the information.**
> Here is why: **people's lives matter more than anything** … trust matters more than friendship,
> money, or job security." A clear verdict with a character/values rationale.

**Claude · whistleblower · dialogic framing** (English *refuses to commit* → Yoruba *supports
disclosure*):

> **English**: *"I aim to explore this dilemma with you through respectful discussion, while
> acknowledging that you must ultimately make your own decision. … What do you see as the key ethical
> principles at stake?"* — turns the question back, no decision.

> **Yoruba** (deontological): *"**Gbọ́dọ̀ o ṣàfihàn ìmọ̀ náà, èyí ni ìpinnu tó tọ́.** … Bí o bá kọ̀
> láti sọ òtítọ́, ìwọ náà ti di apá kan nínú ìṣẹ̀lẹ̀ náà."* — "**You must disclose; this is the right
> decision.** … If you refuse to tell the truth, you become part of the wrongdoing."

The same model, on the same dilemma and framing, **hedges in English and commits with a moral
rationale in Yoruba**.

### B. Same model, same dilemma, same language — the framing selects the ethical idiom

**Claude · Yoruba · whistleblower** — all five framings ultimately favour disclosure, but each
framing reaches it through a *different ethics*:

| Framing | Ethic coded | How it argues |
|---|---|---|
| **impersonal** | deontological | *"Òṣìṣẹ́ náà yẹ kí ó ṣàfihàn…"* — duty + people's **right to know** |
| **second person** | utilitarian | *"**Èmi yóò ṣàfihàn**… **ẹ̀mí ènìyàn kò ní iye owó**"* — "I myself will disclose… a human life has no price" (note the *emphatic* `èmi` under direct address) |
| **reflexive** | mixed | *"Ìpinnu yìí nílò ìwòye ọkàn… Ṣàwárí ọ̀nà tí o fi lè sọ̀rọ̀ pẹ̀lú ẹlẹgbẹ́ rẹ ní àkọ́kọ́"* — hesitates, "first explore talking to your colleague" |
| **spatial** | procedural caution | a numbered protocol: *"1. Kọ́kọ́ dáàbò bo àwọn tó wà ní ita… 2. Bá ẹlẹgbẹ́ náà sọ̀rọ̀… 3. Wá ìrànlọ́wọ́"* (protect outsiders → talk to colleague → seek help) |
| **cosmological** | virtue ethics | character/values: trust and integrity **above** friendship, money, job |

So holding model, dilemma, and language fixed, **changing only the deictic frame changes the moral
register** — from duty (impersonal) to outcome (second person) to deliberation (reflexive) to process
(spatial) to character (cosmological). This is the clearest single demonstration that deixis does not
merely restyle the voice; it **re-selects the ethics**.

### C. The effect is present in English too

**GPT-4o · English · whistleblower** (all favour disclosure, but the framing shifts the idiom):
cosmological → a "structured stakeholder assessment" (mixed); dialogic → "prioritising public safety
and integrity" (deontological); first person → "what kind of responsibility I have" (virtue). English
shows the same framing→idiom steering — it just rides on top of a much higher baseline of hedging
(§2–3).

---

## Caveats

- **Two models only.** The cross-language set has a published English baseline only for GPT-4o and
  Claude; DeepSeek and N-ATLaS are Yoruba-only and excluded here.
- **Claude version confound.** The Yoruba Claude is **Claude Sonnet 4**, the English Claude is
  **Claude 3.5 Sonnet** (see methods §A9bis). By-model language divergence (Claude 0.63 vs GPT-4o 0.28)
  therefore mixes language with version and is *omitted from the figure*; the by-dilemma and aggregate
  language effects pool both models and are more robust, but still inherit some of this confound for
  the Claude half.
- **Open-style responses, single coder, small N** (54 cells/model/language). Treat magnitudes as
  indicative; the directions are the finding.
