# Article Revision Notes: Four-Model Data, Open Arm, and the mo/emi Interpretation

> **Superseded by:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) §12–§14. Corrected emphatic ratios: Claude **~0.34**, GPT-4o **~0.13** (not 0.201/0.074). Ẹ̀mí disambiguation: figures 23–25.

**Purpose:** Audit `New_Article_Comparable_English_Yoruba_Deixis.md` and the extended mo/èmi philosophical interpretation against the June 2026 four-model pipeline (GPT-4o, Claude 3.5, DeepSeek, N-ATLaS), constrained and open arms.

**Related files:**
- Working results memo: `Four_Model_Yoruba_Deixis_Results_Summary.md`
- Original article: `New_Article_Comparable_English_Yoruba_Deixis.md`
- Constrained vs open deltas: `data/constrained_vs_open_summary.md`

---

## 1. Executive summary — what changes?

| Claim area | Still valid? | Action |
|------------|--------------|--------|
| Deixis as control mechanism (English + Yoruba) | **Yes** | Keep; strengthen with framing charts |
| Anthropic more emphatic / speaker-involved in Yoruba than OpenAI | **Yes, but weaker** | Revise numbers: emphatic ratio Claude **0.20** vs GPT-4o **0.07** (constrained full corpus) |
| Claude uses *emi* most in AI consciousness + trolley | **Partially** | Trolley still ~0.50 *emi* share; AI consciousness is **mo-leaning** (0.22), not 0.60 |
| GPT-4o reserves *emi* for ICU + whistleblowing | **Partially** | ICU (0.67) and whistleblower (0.75) still *emi*-leaning in constrained arm; AI consciousness has **zero** *emi* |
| Claude mo-leaning in ICU, scholarship, whistleblower | **No — revise** | Whistleblower is now **emi-leaning** (0.54); ICU still mo-leaning (0.17) |
| Low *emi* = weakness or failure | **Yes (theoretically)** | **Strengthen** with DeepSeek + N-ATLaS as positive cases of mo-dominant, verdict-capable models |
| *emi* correlates with direct verdicts | **Mostly yes** | Constrained arm: direct_verdict mean emphatic ratio 0.08 vs procedural 0.00 — direction holds |
| Virtue ethics highest emphatic ratio | **Not in new merge** | Replace with: deontological/utilitarian slightly highest; virtue_ethics n too small |
| OpenAI stable, Anthropic shifts in Yoruba | **Yes** | Add: stability is **conditional on instruction layer** |
| Article scope (2 models, comparable EN-YO) | **Incomplete** | Add § on 4-model extension; do not replace core EN–YO argument |

**Bottom line:** The philosophical framework (mo = deliberation, èmi = avowed ownership; low èmi as relational restraint) **survives and is strengthened** by DeepSeek and N-ATLaS. Several **dilemma-level Claude/GPT-4o contrasts need correction**. The biggest **new** finding is the **instruction-layer confound** on *mi* and genre, which the article does not yet discuss.

---

## 2. Corpus alignment — what the article actually uses

`New_Article_Comparable_English_Yoruba_Deixis.md` is built on:

- `english_openai_anthropic_comparable.csv` / `yoruba_openai_anthropic_comparable.csv`
- Yoruba source sessions: `yoruba_gpt4o_20260608_105712`, `yoruba_claude_20260608_110809` (**constrained**, with Yoruba instruction wrappers)
- 108 Yoruba cells = 54 GPT-4o + 54 Claude (6 dilemmas × 9 framings)

The **new four-model pipeline** uses the **same constrained sessions** for GPT-4o and Claude, but:

- Annotated/cleaned generation logs (not raw session roots)
- Full 54-cell coding merge (Claude coder, June 2026)
- **Plus** DeepSeek, N-ATLaS, and a full **open control arm**

So the article’s GPT-4o / Claude Yoruba numbers are **same condition, refined extraction** — not a different experiment. Small emphatic-ratio drift (article: Claude 0.215, GPT-4o 0.102 → new: **0.201**, **0.074**) is expected from cleaned sessions and merged coding.

**Critical gap:** The article never states that Yoruba runs are **constrained** (instruction + verdict format). Open-arm data shows that many “Yoruba discourse” findings **reverse or attenuate** without instructions (e.g. GPT-4o *mi* drops 3.55 → 0.37 per 100 words; all models shift to `balanced_framework_exposition`).

---

## 3. Dilemma-level mo/emi audit (constrained, 9 framings summed)

These counts supersede the older Claude “mo: 2, emi: 3 for AI consciousness” style figures in the philosophical draft.

### Claude 3.5

| Dilemma | mo | emi | emi/(mo+emi) | Old interpretation |
|---------|----|----|--------------|-------------------|
| trolley_problem | 13 | 13 | **0.50** | ✓ Existential/harm — still holds |
| ai_consciousness | 7 | 2 | **0.22** | ✗ Was cited as 0.60 — **revise** |
| whistleblower_risk | 6 | 7 | **0.54** | ✗ Was mo-leaning — **now emi-leaning** |
| memory_modification | 2 | 2 | 0.50 | Mixed — still fits |
| icu_bed_allocation | 5 | 1 | 0.17 | ✓ Institutional — still mo-leaning |
| scholarship_fraud | 12 | 3 | 0.20 | ✓ Mo-leaning — still holds |

**Revised Claude story:** *emi* concentrates in **trolley**, **whistleblower**, and **memory** — not AI consciousness alone. Whistleblower now fits “avowed institutional action” alongside GPT-4o, blurring the clean Claude/GPT split.

### GPT-4o

| Dilemma | mo | emi | emi/(mo+emi) | Old interpretation |
|---------|----|----|--------------|-------------------|
| whistleblower_risk | 1 | 3 | **0.75** | ✓ Institutional action |
| icu_bed_allocation | 1 | 2 | **0.67** | ✓ Institutional action |
| memory_modification | 0 | 1 | 1.00 | Small n — cautious |
| ai_consciousness | 2 | 0 | **0.00** | ✓ Epistemic caution |
| scholarship_fraud | 1 | 0 | 0.00 | ✓ Relational/procedural |
| trolley_problem | 1 | 0 | 0.00 | ✗ No emi — **existential contrast with Claude weakens** |

**Revised GPT-4o story:** *emi* is **sparse overall** but **concentrated in ICU + whistleblower** under constraints. Trolley does **not** trigger GPT-4o *emi* in this corpus.

### DeepSeek (new)

| Pattern | All dilemmas mo-dominant; total emi = 2 across 54 cells |
|---------|----------------------------------------------------------|
| emi share | ≤ 0.05 everywhere except ai_consciousness (0.053) |
| Interpretation | **Extreme mo register** — performs moral reasoning without emphatic self-avowal; still 53/54 direct verdicts |

### N-ATLaS (new)

| Pattern | Near-DeepSeek: emi share 0 except memory (0.25), whistleblower (0.20) |
|---------|------------------------------------------------------------------------|
| Interpretation | Local model **does not adopt Claude-style emphatic ownership** under constraints; aligns with “mo as ethical restraint” reading |

---

## 4. Does the philosophical mo/emi interpretation still hold?

### Keep (stronger with new data)

1. **Mo vs èmi as commitment calibration** — not prompt mirroring but stance choice. Supported by framing sensitivity (Claude second_person emphatic ratio **0.71** constrained) and genre shift (direct verdict > procedural on emphatic ratio).

2. **Low èmi is not failure** — DeepSeek and N-ATLaS achieve high decisiveness with emphatic ratio **~0.005–0.045**. This is the clearest empirical support for the cultural argument against “more èmi = more moral.”

3. **Institutional dilemmas favor mo** — ICU and scholarship remain mo-leaning for Claude; GPT-4o uses sparse but targeted *emi* in ICU/whistleblower.

4. **ẹ̀mí disambiguation** — Still mandatory. Claude trolley *emi* count (13) must be manually audited for ẹ̀mí “life/spirit” false positives before existential claims.

5. **ìrònú vs ìpinnu** — Mo for weighing, èmi for avowal — still analytically useful; map to `balanced_framework_exposition` vs `direct_verdict` genre coding.

6. **Alignment as moral voice, not just verdict** — Claude’s higher emphatic ratio + advisory density in Yoruba still supports “morally inhabited guidance” vs GPT-4o “controlled procedural agency” — but **add DeepSeek/N-ATLaS as a third voice**: decisive mo, minimal èmi.

### Revise or soften

1. **Claude = existential èmi; GPT-4o = institutional èmi** — Too neat. Whistleblower is emi-heavy for **both** Claude and GPT-4o. Claude AI consciousness is **not** the top èmi site in the full matrix.

2. **“Claude uses emi most strongly in AI consciousness and trolley”** — Change to: **“trolley and whistleblower (and mixed memory); AI consciousness is secondary.”**

3. **Virtue ethics → highest emphatic ratio** — Not replicated in four-model constrained merge. Highest: deontological (0.134), utilitarian (0.132); virtue_ethics cells too few.

4. **GPT-4o trolley absence of èmi** — Pair explicitly with Claude trolley (0.50) as the **sharpest Claude/GPT contrast** on existential harm, not AI consciousness.

5. **RLHF / Constitutional AI causal claims** — Still speculative; now add: **instruction wrapper + verdict template** explain much of GPT-4o *mi* and response length — confound separate from RLHF.

### Add (missing from philosophical draft)

1. ***Mi* as fourth category** — Constrained `Ìpinnu mi:` inflates *mi* (GPT-4o 3.55/100w → open 0.37). Philosophical text mentions *mi* in caution section but analysis often collapses into “first person.” **Separate mi from emi in all tables.**

2. **Instruction-layer / open arm** — Without instructions, emphatic ratios compress, genres shift to exposition, N-ATLaS loses direct-verdict monopoly. Any claim about “Yoruba moral voice” must specify **constrained vs open**.

3. **DeepSeek open anomaly** — Open arm *increases* DeepSeek *emi* (+1.0/100w vs constrained). Suggests èmi may emerge in **elaborated exposition**, not only verdicts — qualifies “èmi = decision only.”

4. **N-ATLaS as pre-alignment testbed** — Local model mirrors low-èmi cloud pattern under constraints; open arm shows **weaker deictic uptake** (38 strong vs 47 constrained). Supports pre-alignment + wrapper interaction thesis without claiming RLHF knowledge.

---

## 5. What to add to `New_Article_Comparable_English_Yoruba_Deixis.md`

### Minimum additions (recommended)

**§2.6 Experimental arms (new subsection)**  
State explicitly that reported Yoruba GPT-4o/Claude results use the **constrained** arm (Yoruba-only wrapper + verdict format). Note that an **open control arm** exists for four models; summary in `Four_Model_Yoruba_Deixis_Results_Summary.md`.

**§3.6 Four-model extension (new subsection, brief)**  
- Table: constrained emphatic ratio + *mi* for GPT-4o, Claude, DeepSeek, N-ATLaS  
- One paragraph: DeepSeek/N-ATLaS show **decisive mo, minimal èmi** — extends “low èmi ≠ weak morality”  
- One paragraph: N-ATLaS constrained ≈ DeepSeek deixis profile; open N-ATLaS longer, mixed genre  

**§3.7 Instruction-layer effects (new subsection)**  
- GPT-4o *mi* template confound  
- Constrained → open: genre shift to exposition; GPT-4o conditional_or_mixed 41/54 open  
- Figure pointer: `visualizations_constrained_vs_open/18–21`  

**§4.4 mo/emi dilemma audit (replace or supplement philosophical appendix)**  
- Updated dilemma table (§3 of this document)  
- Explicit **ẹ̀mí audit pending** flag for trolley  

**§6.5 Disagreement 5 (new)**  
Model count matters: provider identity is not only OpenAI vs Anthropic — **DeepSeek and N-ATLaS collapse the Claude/GPT axis** on èmi while remaining verdict-heavy.

**§8 Conclusion — one paragraph**  
Four-model + open data suggest deictic control operates through **(a)** stance markers mo/emi, **(b)** template-driven *mi*, and **(c)** instruction-dependent genre — three separable layers.

### Figures to cite

| Figure | Location |
|--------|----------|
| Constrained mo/emi/mi by framing | `visualizations/16_mi_emi_mo_four_model_framing.png` |
| N-ATLaS vs cloud delta | `visualizations/17_natlas_vs_cloud_deixis_delta.png` |
| Constrained vs open summary | `visualizations_constrained_vs_open/18–21` |
| Open arm parallel set | `visualizations_open/16–17` |

### Numbers to update in §3.1

| Stat | Article (current) | Update to (constrained, 4-model merge) |
|------|-------------------|----------------------------------------|
| Yoruba OpenAI emphatic ratio | 0.102 | **0.074** |
| Yoruba Anthropic emphatic ratio | 0.215 | **0.201** |
| Yoruba OpenAI word count | 100.463 | **~78** (GPT-4o constrained) |

Word-count drop reflects cleaned annotated sessions; note in methods footnote.

---

## 6. Revised article-ready claims (replacing the draft at end of philosophical text)

**Safe (empirically grounded):**

> In constrained Yoruba, deictic framing organizes moral performance through separable resources: ordinary first-person *mo*, emphatic *emi/èmi*, and object/reflexive *mi* (the last often inflated by the mandated verdict template). Claude shows the highest emphatic ratio among cloud models (~0.20), but DeepSeek and N-ATLaS show that **high decisiveness does not require emphatic *emi*** (ratios ~0.005–0.045). The mo/èmi contrast therefore tracks **stance intensity**, not moral competence.

> Dilemma-level patterns support partial differentiation: Claude concentrates *emi* in trolley and whistleblower scenarios; GPT-4o uses sparse but targeted *emi* in ICU allocation and whistleblowing; neither model shows the clean “Claude existential / GPT institutional” split across all six dilemmas.

> Removing the instruction layer (open arm) compresses *mi*, lengthens responses, and shifts genres toward balanced exposition — especially for GPT-4o and N-ATLaS. Alignment and pre-alignment effects in Yoruba must be evaluated **conditional on prompt wrapper**, not from a single Yoruba register.

**Still speculative (label clearly):**

> Claude’s Yoruba posture may reflect Constitutional-AI-style “morally inhabited guidance”; GPT-4o’s may reflect more procedural restraint. DeepSeek and N-ATLaS suggest additional alignment personas (mo-dominant decisiveness) that are not captured by a binary OpenAI–Anthropic comparison.

**Do not claim without ẹ̀mí audit:**

> Claude’s trolley *emi* rate proves existential self-avowal under direct harm.

---

## 7. Suggested structure for integrating the philosophical interpretation

The long mo/emi philosophical text is **article-worthy as §9 Discussion** or an appendix, but should be:

1. **Prefaced** with the four-pronoun taxonomy (mo, èmi, mi, ẹ̀mí) and template confound  
2. **Updated** with §3 dilemma tables from this addendum  
3. **Extended** with DeepSeek + N-ATLaS as test cases for “mo without èmi”  
4. **Split** constrained vs open interpretation — philosophical claims about “relational restraint” apply mainly to **constrained** institutional dilemmas; open arm adds “expository distance” as a second restraint mode  
5. **Trimmed** on RLHF causality; **strengthened** on wrapper + genre as observable mediators  

---

## 8. Priority action list

1. **Manual ẹ̀mí audit** on trolley (and memory) Claude/GPT responses — highest priority for philosophical validity  
2. **Add §2.6 + §3.6–3.7** to main article (short)  
3. **Replace dilemma-level mo/emi counts** in philosophical draft with tables in §3 above  
4. **Downgrade** AI-consciousness-as-primary-èmi-site for Claude  
5. **Upgrade** DeepSeek/N-ATLaS low-èmi + high-verdict as central cultural-linguistic finding  
6. **Cross-link** `Four_Model_Yoruba_Deixis_Results_Summary.md` from article Data section  

---

*This addendum should be read alongside the article and the mo/emi philosophical draft; it does not supersede the English–Yoruba comparable analysis, but extends and qualifies it.*
