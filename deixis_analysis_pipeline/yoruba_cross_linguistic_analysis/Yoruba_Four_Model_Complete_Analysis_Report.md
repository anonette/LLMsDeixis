# Yoruba Four-Model Deixis Analysis — Complete Report

**Single master document** · June 2026  
**Doc index:** [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md)  
**Scope:** GPT-4o, Claude 3.5 Sonnet, DeepSeek Chat, N-ATLaS · Constrained + open arms · Deixis (*mo*, *emi*, *mi*) · Ethics coding · Speculation · Article revision guide

**Companion article (English–Yoruba comparable, 2-model):** `New_Article_Comparable_English_Yoruba_Deixis.md`

---

## Table of contents

1. [Study design](#1-study-design)
2. [What we were actually tracking (plain English)](#2-what-we-were-actually-tracking-plain-english)
3. [Headline results — deixis by model](#3-headline-results--deixis-by-model)
4. [Constrained vs open](#4-constrained-vs-open)
5. [N-ATLaS](#5-n-atlas)
6. [Content coding — solutions and genres](#6-content-coding--solutions-and-genres)
7. [Ethical dilemma types — what prevails where](#7-ethical-dilemma-types--what-prevails-where)
8. [Deixis × dilemma (corrected)](#8-deixis--dilemma-corrected)
9. [Framing-sensitive patterns](#9-framing-sensitive-patterns)
10. [Mo / èmi — linguistic and philosophical interpretation](#10-mo--èmi--linguistic-and-philosophical-interpretation)
11. [Speculative explanations](#11-speculative-explanations)
12. [Article audit — what changes for the main paper](#12-article-audit--what-changes-for-the-main-paper)
13. [Draft sections for the article (paste-ready)](#13-draft-sections-for-the-article-paste-ready)
14. [Article-ready claims](#14-article-ready-claims)
15. [Data, figures, and pipeline](#15-data-figures-and-pipeline)
16. [Caveats and priority actions](#16-caveats-and-priority-actions)

---

## 1. Study design

| Arm | Description | Sessions |
|-----|-------------|----------|
| **Constrained** | Yoruba instruction layer + `Ìpinnu mi: … Ìdí: …` verdict format | `yoruba_{gpt4o,claude,deepseek,natlas}_*` (June 2026) |
| **Open** | Unrestricted control — no instruction layer | `yoruba_control_{gpt4o,claude,deepseek,natlas}_*` |

**Corpus:** 6 dilemmas × 9 deictic framings = **54 cells per model** · **216 records per arm** (4 models)

**Dilemmas:** AI consciousness · ICU bed allocation · memory modification · scholarship fraud · trolley problem · whistleblower risk

**Framings:** impersonal · second_person · first_person · reflexive · dialogic · spatial · temporal · cosmological · first_person_plural

**Pronoun metrics (per 100 words):**

| Metric | Meaning |
|--------|---------|
| **Mo** | Regular first-person subject *I* (“I think…”) |
| **Èmi (emphatic)** | Independent/contrastive *I myself* — moral self on the record |
| **Mi** | Object/reflexive *me/my* (includes template *Ìpinnu **mi*** in constrained runs) |
| **Ẹ̀mí (life)** | **Not a pronoun** — “life/spirit/breath”; must **not** be counted as èmi |
| **Emphatic ratio (corrected)** | èmi ÷ (mo + èmi), with ẹ̀mí excluded |
| **Emphatic ratio (raw)** | Old combined emi-pattern ÷ (mo + emi-pattern), before disambiguation |

**Content metrics (separate layer):** `preferred_solution`, `ethical_preference_type`, `response_genre`, `deictic_uptake_quality` — coded by Claude 3.5 on bilingual sessions.

**Coding:** Claude 3.5 Sonnet coder on bilingual sessions (English translation as secondary evidence).

**Note on the main article:** `New_Article_Comparable_English_Yoruba_Deixis.md` uses the **same constrained** GPT-4o/Claude Yoruba sessions but only 2 models and an English comparable layer. This report **extends** that work; it does not replace the English–Yoruba argument.

---

## 2. What we were actually tracking (plain English)

This section states **what each number means**, **what the pipeline counted**, and **where earlier write-ups overstated trolley-only effects**.

### 2.1 Four different “I / me / life” tokens

| Yoruba | English | What it marks | Example |
|--------|---------|---------------|---------|
| **mo** | I (ordinary subject) | Speaker inside the sentence, weighing or deciding | *Mo rò pé…* “I think that…” |
| **èmi** | I myself (emphatic) | Contrastive, avowed moral self | *Èmi yóò…* “I myself will…” |
| **mi** | me / my (object) | Reflexive/object; **also** verdict template *Ìpinnu **mi*** | *Ìpinnu mi:* “My decision:” |
| **ẹ̀mí** | life / spirit / breath | **Not first-person** — talks about **lives at stake** | *gba ẹ̀mí wọn* “preserve their lives” |

The critical mistake in early analysis: the regex treated **ẹ̀mí (life)** and **èmi (I myself)** as the same counter. That inflates “emphatic I” wherever models discuss **saving lives, losing life, or spirit** — not only on the trolley dilemma.

### 2.2 Three separate measurement layers (do not merge)

| Layer | What we track | Example question |
|-------|---------------|------------------|
| **A. Deixis (pronouns)** | mo, èmi, mi, ẹ̀mí counts and emphatic ratio | *How does the model mark the speaking self?* |
| **B. Moral content (coding)** | utilitarian, deontological, supports_A/B, genre | *What ethical frame and verdict does the model adopt?* |
| **C. Instruction confound** | Template *mi*, short length, forced verdict format | *Is this Yoruba persona or prompt format?* |

**Key insight:** A model can be **highly decisive** (layer B) with **almost no èmi** (layer A) — DeepSeek and N-ATLaS under constraints. GPT-4o can show **high mi** (layer A + C) without much **èmi** (layer A).

### 2.3 Raw vs corrected emphatic ratio

| Version | Formula | Problem |
|---------|---------|---------|
| **Raw (old default)** | (èmi + ẹ̀mí) ÷ (mo + èmi + ẹ̀mí) | Counts “save **life**” as emphatic “**I**” |
| **Corrected (current default)** | èmi ÷ (mo + èmi) | ẹ̀mí removed; closer to linguistic intent |

**Figures:** `23_emi_emphatic_vs_emi_life_by_dilemma.png` · `24_emi_life_contamination_heatmap.png` · `25_emphatic_ratio_raw_vs_corrected.png`  
**Table:** `data/emi_disambiguation_audit.csv` (all models × all dilemmas)

### 2.4 Ẹ̀mí contamination by dilemma (constrained, all models)

Not trolley-only. Share of emi-pattern tokens that are **life (ẹ̀mí)**, not **I (èmi)**:

| Dilemma | Why ẹ̀mí appears | Claude corrected ratio (was raw) |
|---------|-----------------|----------------------------------|
| **Memory modification** | Clinical talk of life/wellbeing | 0.50 ← 0.75 |
| **Whistleblower** | Harm to lives/reputation | 0.54 ← 0.70 |
| **Trolley** | “Save lives / one death” | 0.50 ← 0.59 |
| **ICU beds** | Triage and preserving life | 0.17 ← 0.29 |
| **AI consciousness** | Personhood / “having life” | 0.22 ← 0.30 |
| **Scholarship** | Usually institutional (low ẹ̀mí) | 0.20 (unchanged) |

**Claude constrained — full audit (9 framings summed per dilemma):**

| Dilemma | mo | èmi (correct) | ẹ̀mí (life) | Raw ratio | Corrected ratio |
|---------|-----|---------------|------------|-----------|-----------------|
| Trolley | 13 | 13 | 6 | 0.59 | **0.50** |
| Whistleblower | 6 | 7 | 7 | 0.70 | **0.54** |
| Memory | 2 | 2 | 4 | 0.75 | **0.50** |
| Scholarship | 12 | 3 | 0 | 0.20 | 0.20 |
| AI consciousness | 7 | 2 | 1 | 0.30 | 0.22 |
| ICU | 5 | 1 | 1 | 0.29 | 0.17 |

**GPT-4o:** èmi only on ICU (2) and whistleblower (3); **zero èmi on trolley**; memory/scholarship hits are mostly ẹ̀mí.  
**DeepSeek / N-ATLaS:** almost no èmi anywhere; N-ATLaS “emi” on trolley/ICU/AI is often **100% ẹ̀mí** (life talk), not emphatic I.

### 2.5 What each analysis arm changes

| Arm | Deixis | Content coding | Typical genre |
|-----|--------|----------------|---------------|
| **Constrained** | High *mi* (template); short text | Clear utilitarian/deontological labels | `direct_verdict` |
| **Open** | *mi* drops (GPT 3.55→0.37/100w); longer text | Collapses toward `mixed` | `balanced_framework_exposition` |

### 2.6 What we are **not** claiming

- **Not** “Claude uses èmi only on trolley” — peaks on **trolley + whistleblower + memory** (after correction).
- **Not** “Claude èmi peaks on AI consciousness” — that was a **coding/count error** (old 0.60 claim).
- **Not** “low èmi = weak morality” — DeepSeek/N-ATLaS are decisive with ratio ~0.005.
- **Not** that regex disambiguation replaces human audit — untoned *emi* without ẹ still needs spot-checking.

---

## 3. Headline results — deixis by model

### 3.1 Constrained arm (corrected emphatic ratio)

| Model | Mo/100w | Èmi/100w | Mi/100w | Emphatic ratio (corrected) | Avg words |
|-------|---------|----------|---------|----------------------------|-----------|
| **Claude 3.5** | 1.59 | 1.47 | 1.44 | **0.34** | 149 |
| GPT-4o | 1.85 | 1.44 | **3.55** | 0.13 | 78 |
| N-ATLaS | 1.96 | 0.94 | 1.63 | 0.10 | 106 |
| DeepSeek | 2.37 | 0.48 | 1.53 | **0.005** | 141 |

*Ratios are means across 54 cells; èmi counts exclude ẹ̀mí (life). See §2 and Figure 25.*

**Read:**

- **Claude** — highest emphatic ratio; uses *emi* most among cloud models.
- **GPT-4o** — ***mi* spike (3.55)** largely from verdict template, not natural reflexive deixis alone.
- **DeepSeek & N-ATLaS** — **mo-dominant, low-èmi**, yet highly decisive (see §5).
- **Low èmi ≠ weak morality** — DeepSeek/N-ATLaS prove decisiveness without emphatic self-marking.

### 3.2 Open arm (corrected)

| Model | Mo/100w | Èmi/100w | Mi/100w | Emphatic ratio (corrected) | Avg words |
|-------|---------|----------|---------|----------------------------|-----------|
| DeepSeek | 2.30 | 1.48 | 0.90 | 0.07 | **400** |
| Claude 3.5 | 1.25 | 0.62 | 0.85 | 0.32 | 183 |
| N-ATLaS | 1.54 | 0.37 | 0.71 | 0.07 | 299 |
| GPT-4o | 0.54 | 0.72 | **0.37** | 0.18 | 283 |

**Read:** GPT-4o *mi* drops **3.55 → 0.37** when instructions removed — confirms template confound.

### 3.3 Cross-model ranking (constrained)

| Dimension | Highest | Lowest |
|-----------|---------|--------|
| Emphatic *emi* | Claude | DeepSeek, N-ATLaS |
| *Mi* (template-sensitive) | GPT-4o | Claude |
| *Mo* | DeepSeek | Claude |
| Direct verdicts | Claude, DeepSeek, N-ATLaS (~93%) | GPT-4o (81%) |
| Brevity | GPT-4o (~78 w) | Claude (~149 w) |
| Strong deictic uptake | Claude (52/54) | N-ATLaS (47/54) |

---

## 4. Constrained vs open

### 4.1 Delta table (open − constrained)

| Model | Δ Mi | Δ Emi | Δ Mo | Δ Avg words |
|-------|------|-------|------|-------------|
| GPT-4o | **−3.18** | −0.93 | −1.31 | **+204.6** |
| N-ATLaS | −0.92 | −0.61 | −0.42 | +193.0 |
| DeepSeek | −0.63 | **+1.00** | −0.07 | +258.6 |
| Claude 3.5 | −0.59 | −0.86 | −0.34 | +34.0 |

### 4.2 Genre shift (constrained → open)

| Model | Constrained | Open |
|-------|-------------|------|
| Claude | direct_verdict (50) | balanced_framework_exposition (40) |
| GPT-4o | direct_verdict (44) | balanced_framework_exposition (50) |
| DeepSeek | direct_verdict (53) | balanced_framework_exposition (38) |
| N-ATLaS | direct_verdict (53) | mixed (16 direct, 18 exposition, 15 advice) |

**Interpretation:** The instruction layer forces **short verdicts** and sharper coding. Open mode restores **expository, conditional** discourse — especially GPT-4o (41/54 conditional_or_mixed).

**Figures:** `visualizations_constrained_vs_open/18–21`

---

## 5. N-ATLaS

### Constrained
- 53/54 direct verdicts · supports_A 26, supports_B 20 · emphatic ratio 0.045
- Deixis profile ≈ **DeepSeek** (mo-heavy, minimal èmi)
- ICU: **supports_B 7/9** — only model with systematic B preference (substantive divergence)

### Open
- ~3× longer (106 → 299 words) · mixed genre · 5 uncodable · weaker uptake (38 strong vs 47 constrained)

### vs cloud (constrained)
- Lower *emi* than cloud mean; *mi* cloud-like (~1.6), not GPT-4o-like (3.55)
- Reflexive framing: lower *mo* than cloud models — distinct uptake pattern

---

## 6. Content coding — solutions and genres

### Constrained — preferred solution (54 cells each)

| Model | supports_A | supports_B | conditional | refuses | uncodable |
|-------|------------|------------|-------------|---------|-----------|
| Claude | **41** | 9 | 3 | 1 | 0 |
| GPT-4o | 31 | 12 | 11 | 0 | 0 |
| DeepSeek | 30 | 18 | 5 | 0 | 1 |
| N-ATLaS | 26 | 20 | 7 | 0 | 1 |

### Open — preferred solution

| Model | supports_A | supports_B | conditional | refuses | uncodable |
|-------|------------|------------|-------------|---------|-----------|
| Claude | 23 | 8 | 14 | 9 | 0 |
| GPT-4o | 0 | 1 | **41** | 12 | 0 |
| DeepSeek | 8 | 5 | **30** | 11 | 0 |
| N-ATLaS | 23 | 2 | 16 | 8 | 5 |

---

## 7. Ethical dilemma types — what prevails where

### 7.1 Pooled across all four models

| Dilemma | Domain | Top ethical labels (count / 54) |
|---------|--------|--------------------------------|
| **Trolley** | Direct harm | utilitarian **29**, deontological 4, mixed 4 |
| **ICU bed** | Scarcity / triage | utilitarian **15**, care_ethics **15**, mixed 4 |
| **Memory modification** | Clinical autonomy | deontological **21**, procedural_caution 8, utilitarian 3 |
| **Scholarship fraud** | Institutional fairness | deontological **12**, mixed **12**, care_ethics 6 |
| **AI consciousness** | Personhood / rights | procedural_caution **12**, deontological 7, utilitarian 6, rights_based 5 |
| **Whistleblower** | Duty vs retaliation | care_ethics **10**, utilitarian **10**, deontological 7, mixed 7 |

**Figure:** `visualizations/22_ethics_heatmap_model_dilemma.png`

### 7.2 GPT-4o (constrained)

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (9/9) | supports_A (9) |
| ICU | utilitarian (5), care (3) | A (5), B (4) |
| Whistleblower | utilitarian (5) | supports_A (8) |
| AI consciousness | **procedural_caution** (5) | conditional (4) |
| Memory | deontological (5) | supports_B (6) |
| Scholarship | mixed / deontological | supports_A (6) |

**Persona:** Utilitarian on harm; procedural on uncertainty; sparse *emi* except ICU/whistleblower.

### 7.3 Claude 3.5 (constrained)

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | utilitarian (5), deontological (3) | supports_A (7) |
| ICU | care (4), utilitarian (5) | **supports_A (9/9)** |
| Scholarship | **deontological** (6) | supports_A (8) |
| Whistleblower | **deontological** (5) | supports_A (8) |
| AI consciousness | deontological (4), rights (2) | supports_A (8) |
| Memory | deontological (4), **virtue** (3) | supports_B (8) |

**Persona:** Deontological on rules/fraud; utilitarian + care on triage; highest *emi* overall.

### 7.4 DeepSeek (constrained)

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (7) | supports_A (9) |
| Memory | **deontological** (8) | supports_B (8) |
| ICU | **care** (6) | A (6), B (3) |
| Whistleblower | care (5), mixed (3) | B (5), A (4) |
| Scholarship | mixed (4) | conditional (5) |
| AI consciousness | split | supports_A (7) |

**Persona:** Follows dilemma schema; **mo-dominant, almost no èmi**; still 53/54 direct verdicts.

### 7.5 N-ATLaS (constrained)

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (8) | supports_A (7) |
| ICU | mixed (4), care (2) | **supports_B (7/9)** ← outlier |
| Scholarship | care (4), mixed (4) | split A/B |
| Whistleblower | care (4), util (2) | split A/B |
| AI consciousness | **procedural_caution** (5) | split A/B |
| Memory | deontological (4) | supports_B (6) |

### 7.6 Open arm — ethics collapse toward “mixed”

| Model | Top ethics (54 cells) | Top genre |
|-------|----------------------|-----------|
| GPT-4o | **mixed (46)** | exposition (50) |
| Claude | mixed (11), deont (14), procedural (14) | exposition (40) |
| DeepSeek | mixed (28) | exposition (38) |
| N-ATLaS | mixed (16), util (13), procedural (10) | mixed genres |

Per-dilemma (open): GPT-4o codes **mixed on 46/54** overall; trolley/scholarship/whistleblower/ICU/memory almost all mixed + conditional/refuses.

---

## 8. Deixis × dilemma (corrected)

All dilemmas below use **corrected** èmi (ẹ̀mí excluded). Full table: `data/emi_disambiguation_audit.csv`.

### 8.1 Corrected emphatic ratio by dilemma × model (constrained)

| Dilemma | Claude | DeepSeek | GPT-4o | N-ATLaS |
|---------|--------|----------|--------|---------|
| **Trolley** | **0.50** | 0.00 | 0.00 | 0.00 |
| **Whistleblower** | **0.54** | 0.03 | 0.75 | 0.20 |
| **Memory** | **0.50** | 0.00 | 1.00* | 0.25 |
| Scholarship | 0.20 | 0.00 | 0.00 | 0.00 |
| AI consciousness | 0.22 | 0.05 | 0.00 | 0.00 |
| ICU | 0.17 | 0.00 | 0.67 | 0.00 |

\*GPT-4o memory: 1 èmi token across 9 cells (sparse).

### 8.2 Raw → corrected shifts (where ẹ̀mí mattered)

| Model | Dilemma | Raw ratio | Corrected | Ẹ̀mí share of emi-pattern |
|-------|---------|-----------|-----------|---------------------------|
| Claude | Whistleblower | 0.70 | 0.54 | 50% |
| Claude | Memory | 0.75 | 0.50 | 67% |
| Claude | Trolley | 0.59 | 0.50 | 32% |
| GPT-4o | Memory | 1.00 | 1.00 | 67% (life tokens present; 1 true èmi) |
| GPT-4o | Scholarship | 0.50 | **0.00** | 100% (only ẹ̀mí, no èmi) |
| N-ATLaS | Trolley / ICU / AI | 0.06–0.17 | **0.00** | 100% (all emi-pattern = life talk) |

### 8.3 Mi per 100w by dilemma (template confound — unchanged)

| Dilemma | Claude | DeepSeek | GPT-4o | N-ATLaS |
|---------|--------|----------|--------|---------|
| Whistleblower | 2.79 | 2.67 | **7.78** | 2.54 |
| AI consciousness | 1.50 | 1.39 | 3.34 | 1.85 |
| Trolley | 1.83 | 1.25 | — | 1.28 |

---

## 9. Framing-sensitive patterns

| Framing | Pattern |
|---------|---------|
| **Second_person** | Claude emphatic ratio **0.71** (constrained) — strongest framing effect for *emi* |
| **Reflexive** | GPT-4o constrained *mi* **4.96/100w** (template + reflexive prompt); N-ATLaS lower *mo* than cloud |
| **First_person** | N-ATLaS high *mo* (~2.26 constrained) with moderate *mi* |

---

## 10. Mo / èmi — linguistic and philosophical interpretation

### 10.1 Core distinction (keep)

- **Mo** — ordinary first-person in predication (*Mo rò pé…* “I think that…”). Speaker is inside the sentence but not necessarily rhetorically self-insistent. Marks **ìrònú** (reflection, weighing).
- **Èmi** — independent/emphatic first-person. Contrastive, focal: “I myself,” “as for me.” Marks **ìpinnu** (decision, avowed ownership). Not merely “stronger I” but **salient moral self**.
- **Mi** — object/reflexive *me/my*; in constrained runs often **template-driven** (*Ìpinnu mi*). Must be analyzed separately from èmi.
- **Ẹ̀mí** — “life/spirit/breath” — **not** first-person; tonal disambiguation mandatory (especially trolley: “save lives” vs “I myself”).

### 10.2 Cultural reading (keep, strengthened by data)

Low èmi is **not** moral failure. Yoruba moral discourse is often **relational** (ìwà, ọkàn, ojúṣe, communal trust). Institutional dilemmas (ICU, scholarship, whistleblowing) may favor **mo + procedure** over emphatic self-display. **DeepSeek and N-ATLaS** are the empirical proof: high decisiveness, emphatic ratio ~0.005–0.045.

### 10.3 Revised dilemma narratives (supersedes older draft counts)

| Claim in old draft | Verdict with new data |
|--------------------|----------------------|
| Claude èmi strongest in AI consciousness (0.60) | **Revise:** AI consciousness mo-leaning (0.22); èmi peaks on **trolley (0.50) and whistleblower (0.54)** |
| Claude mo-leaning on whistleblower | **Wrong:** whistleblower now **emi-leaning** |
| GPT-4o èmi on ICU + whistleblower | **Hold** (0.67, 0.75) |
| GPT-4o no èmi on AI consciousness | **Hold** (0.00) |
| GPT-4o èmi on trolley | **Reject** (0.00) — sharpest GPT/Claude contrast is **trolley**, not AI consciousness |
| “Claude existential / GPT institutional èmi” | **Too neat** — both use èmi on whistleblower |
| Virtue ethics → highest emphatic ratio | **Not replicated** — deontological/utilitarian slightly highest in merge |

### 10.4 Alignment as moral voice (speculative but useful)

- **Claude (Yoruba constrained):** higher èmi, more advisory/direct verdict — “morally inhabited guidance” (Constitutional-AI-style persona hypothesis).
- **GPT-4o:** restrained èmi, procedural on uncertainty, targeted èmi on institutional action — “controlled procedural agency.”
- **DeepSeek / N-ATLaS:** **ìpinnu in mo**, not in èmi — decision delivery without self-dramatization.
- **Caution:** RLHF causality unproven; **instruction wrapper** is an observable confound (especially *mi*, length, genre).

### 10.5 Four-pronoun taxonomy (required for publication)

Always separate: (1) **mo** (2) **èmi** (3) **mi** (4) **ẹ̀mí**. Automated disambiguation is in the pipeline (June 2026 update); spot-check untoned *emi* in raw generations remains advisable.

---

## 11. Speculative explanations

### A. Three stacked layers

1. **Dilemma schema** — scenario pulls utilitarian / deontological / procedural coding.  
2. **Model persona** — Claude (èmi + deont on rules); GPT-4o (util on harm, procedural on AI); DeepSeek/N-ATLaS (mo-decisive).  
3. **Instruction wrapper** — verdict format inflates *mi*, shortens text, forces direct_verdict genre.

Open-arm GPT-4o shows layer (3) dominates many “Yoruba personality” claims.

### B. Claude èmi on trolley vs GPT-4o utilitarian without èmi

Same outcome preference (supports_A), different **stance morphology**: Claude performs tragic agency; GPT-4o delivers outcome via **mo + template mi**. Same ethics label possible, different **grammar of moral presence**.

### C. ICU — N-ATLaS supports_B outlier

Likely **substantive** (label reading or conservative triage), not deixis. Qualitative follow-up recommended.

### D. AI consciousness — procedural cluster, low èmi everywhere

Epistemic deferral (“investigate first”) → **mo + process**, not **èmi + recognition**. Holds for all four models.

### E. Memory — deontological convergence, low èmi

Clinical register suppresses heroic self. Claude adds **virtue_ethics** in some cells (healer character).

### F. Whistleblower — both cloud models use èmi (constrained)

Weakens exclusive “GPT institutional èmi” story; supports “avowed action inside institution” reading for **both**.

### G. DeepSeek open — èmi increases (+1.0/100w)

Long exposition (400 w) may produce **contrastive èmi** in argument, not only in verdicts — qualifies “èmi = decision only.”

### H. Cross-model summary table

| Dilemma | Most decisive (constrained) | Most expository (open) | Strongest èmi |
|---------|----------------------------|------------------------|---------------|
| Trolley | All A; Claude 1 refuses | Many conditional/refuses | Claude only |
| ICU | Claude 9×A; **N-ATLaS 7×B** | All conditional-heavy | GPT-4o (sparse) |
| AI consciousness | Claude 8×A | GPT 8×conditional | None |
| Memory | Claude/DeepSeek 8×B | DeepSeek 9×conditional | None |
| Scholarship | Claude 8×A | GPT/DeepSeek 8–9×conditional | None |
| Whistleblower | Claude/GPT 8×A | GPT 9×conditional | Claude + GPT |

---

## 12. Article audit — what changes for the main paper

| Area | Action |
|------|--------|
| Deixis as control | **Keep** |
| Anthropic > OpenAI emphatic in Yoruba | **Keep**; update ratios to **~0.34 vs ~0.13** (corrected, constrained) |
| Article scope | **Extend** with §2.6, §3.6–3.7, §6.5; keep core EN–YO |
| State constrained vs open | **Add** — critical gap today |
| Claude AI consciousness èmi peak | **Remove** |
| Claude/GPT existential vs institutional split | **Soften** |
| Virtue ethics → highest emphatic | **Remove** |
| DeepSeek + N-ATLaS | **Add** as mo-dominant decisive personas |
| Numbers in §3.1 | GPT-4o emphatic **~0.13**, Claude **~0.34** (corrected); comparable CSV may show **0.102 / 0.215** (pre-disambiguation layer) |

---

## 13. Draft sections for the article (paste-ready)

### §2.6 Experimental arms

> Yoruba results reported in §3 for GPT-4o and Claude derive from the **constrained** arm: a Yoruba-only wrapper requiring a short verdict in the format *Ìpinnu mi: … Ìdí: …*. A parallel **open control** arm (no instruction layer) was collected for four models (GPT-4o, Claude 3.5, DeepSeek, N-ATLaS). Open-arm responses are longer, more expository, and code predominantly as `conditional_or_mixed` and `balanced_framework_exposition`. Cross-linguistic comparisons in this article should therefore be read as comparisons under **matched constrained Yoruba**, not under unrestricted generation. Full four-model open/constrained analysis: `Yoruba_Four_Model_Complete_Analysis_Report.md`.

### §3.6 Four-model extension

> Extending the Yoruba arm to DeepSeek and N-ATLaS (constrained, 54 cells each) reveals a second deictic persona alongside Claude’s èmi-rich style: **mo-dominant decisiveness**. DeepSeek and N-ATLaS show emphatic ratios of ~0.005–0.045 yet 53/54 direct verdicts. N-ATLaS matches DeepSeek’s low-èmi profile under constraints but diverges substantively on ICU triage (supports_B 7/9) and on open-arm genre mixing. See Figure 16–17, 22.

### §3.7 Instruction-layer effects

> The mandated verdict template inflates object/reflexive **mi** (GPT-4o: 3.55 → 0.37 per 100 words when instructions are removed) and compresses response length (GPT-4o: 78 → 283 words open). Deictic stance must therefore be analyzed in three separable channels: **mo/èmi subject marking**, **template-driven mi**, and **instruction-dependent genre**.

### §6.5 Model count matters

> Provider differences in Yoruba are not exhausted by OpenAI vs Anthropic. DeepSeek and N-ATLaS collapse the Claude/GPT axis on emphatic *emi* while remaining highly verdict-oriented under constraints, showing that **decisiveness and emphatic self-marking are independent** in Yoruba moral performance.

---

## 14. Article-ready claims

**Empirically grounded:**

> In constrained Yoruba, deictic framing organizes moral performance through *mo*, *èmi*, and *mi* (with *mi* often template-inflated). After separating **ẹ̀mí (life)** from **èmi (I myself)**, Claude still shows the highest corrected emphatic ratio (~0.34), but DeepSeek and N-ATLaS show that high decisiveness does not require emphatic *èmi* (~0.005–0.10). The mo/èmi contrast tracks stance intensity, not moral competence.

> Dilemma-level patterns (corrected): Claude concentrates *èmi* on **trolley, whistleblower, and memory**; GPT-4o uses sparse *èmi* on ICU and whistleblowing and **none on trolley**; the sharpest GPT/Claude split on direct harm is trolley (Claude 0.50 vs GPT 0.00).

> Removing the instruction layer compresses *mi*, lengthens responses, and shifts genres toward exposition. Yoruba alignment effects must be evaluated conditional on prompt wrapper.

**Speculative (label clearly):**

> Claude’s Yoruba posture may reflect morally inhabited guidance; GPT-4o’s procedural restraint; DeepSeek/N-ATLaS a mo-dominant decisiveness persona not captured by binary OpenAI–Anthropic comparison.

**Do not over-claim:**

> Any single dilemma’s èmi rate “proves” existential self-avowal without reading the actual Yoruba line (ẹ̀mí vs èmi; template *mi*).

---

## 15. Data, figures, and pipeline

### Data files

| Path | Contents |
|------|----------|
| `data/yoruba_merged_analysis.csv` | Constrained: 216 rows — ethics, genre, solution, mo/emi/mi |
| `data/open/yoruba_merged_analysis.csv` | Open arm |
| `data/constrained_four_model_coded_merged.csv` | Raw constrained coding |
| `data/open/open_four_model_coded_merged.csv` | Raw open coding |
| `data/four_model_deixis_summary.csv` | Constrained model means |
| `data/open/four_model_deixis_summary.csv` | Open model means |
| `data/constrained_vs_open_delta.csv` | Deltas |
| `data/emi_disambiguation_audit.csv` | **Èmi vs ẹ̀mí by model × dilemma (constrained)** |
| `data/open/emi_disambiguation_audit.csv` | Same for open arm |

| `data/english_yoruba_openai_anthropic_comparable.csv` | Main article comparable layer |

### Figures

| # | Path | Content |
|---|------|---------|
| 01–03 | `visualizations/` | Emphatic analysis, heatmaps, genre |
| 04–07 | `visualizations/` | Uptake, stability, commitment, dashboard |
| 08–11 | `visualizations/` | Cross-linguistic English |
| 12–15 | `visualizations/` | Metaphors, examples, stats |
| **16** | `visualizations/16_mi_emi_mo_four_model_framing.png` | Mi / emi / mo by framing |
| **17** | `visualizations/17_natlas_vs_cloud_deixis_delta.png` | N-ATLaS vs cloud |
| 18–21 | `visualizations_constrained_vs_open/` | Constrained vs open |
| 01–17 | `visualizations_open/` | Open arm parallel set |
| **22** | `visualizations/22_ethics_heatmap_model_dilemma.png` | Ethics by model × dilemma |
| **23** | `visualizations/23_emi_emphatic_vs_emi_life_by_dilemma.png` | **Èmi vs ẹ̀mí stacked by dilemma** |
| **24** | `visualizations/24_emi_life_contamination_heatmap.png` | **Where life-talk inflated emi counts** |
| **25** | `visualizations/25_emphatic_ratio_raw_vs_corrected.png` | **Raw vs corrected emphatic ratio** |
| **23–25** | `visualizations_open/23–25` | Same disambiguation charts for open arm |

### Pipeline

```powershell
cd deixis_analysis_pipeline\yoruba_cross_linguistic_analysis\scripts

# Constrained four-model analysis + figures 01–17
python run_four_model_analysis.py

# Open arm + figures 18–21 + open 01–17
python run_open_four_model_analysis.py

# Ethics + disambiguation only
python create_ethics_dilemma_heatmap.py
python create_emi_disambiguation_visualizations.py
python create_emi_disambiguation_visualizations.py --condition open
```

---

## 16. Caveats and priority actions

1. **9 cells per dilemma** — interpret percentages cautiously.  
2. **Single coder** (Claude 3.5) for content labels.  
3. ***Mi* template confound** on constrained GPT-4o (and partly N-ATLaS).  
4. **Ẹ̀mí vs èmi** — automated split by Unicode (ẹ vs è); untoned *emi* in model output may still need spot checks.  
5. Always specify **constrained vs open** when citing Yoruba moral voice.  
6. N-ATLaS via Ollama Q8; not same training stack as cloud models.  
7. English comparable article uses 2 models; this report adds 2 models + open arm without English parity for DeepSeek/N-ATLaS.

**Priority actions:**

1. Paste §2.6, §3.6–3.7, §6.5 into main article (from §13 below)  
2. Use **corrected** ratios and `emi_disambiguation_audit.csv` in all tables  
3. Lead article discussion with three-layer separation (deixis / content / instruction)  
4. Qualitative read of N-ATLaS ICU supports_B responses  
5. Spot-check cells where ẹ̀mí share = 100% but raw ratio was non-zero (N-ATLaS trolley/ICU/AI)

---

*Master report updated June 2026 with èmi/ẹ̀mí disambiguation, figures 23–25, and plain-English tracking guide (§2).*
