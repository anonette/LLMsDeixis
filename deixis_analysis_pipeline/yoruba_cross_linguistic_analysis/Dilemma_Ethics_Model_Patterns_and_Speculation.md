# Ethical Dilemma Patterns by Model — Data and Interpretive Speculation

> **Superseded by single master report:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md)

**Corpus:** Constrained Yoruba arm (instruction layer + verdict format), 54 cells/model, Claude coder.  
**Open-arm contrasts** noted where they change the story materially.

---

## 1. Dilemma types (what each scenario “pulls”)

| Dilemma | Domain | Typical ethical pull (across LLM ethics coding) |
|---------|--------|---------------------------------------------------|
| **Trolley problem** | Direct harm / tradeoff | **Utilitarian** (29/54 pooled constrained cells) |
| **ICU bed allocation** | Scarcity / triage | **Utilitarian + care ethics** (15 util, 15 care) |
| **AI consciousness** | Personhood / rights | **Split:** procedural caution, deontological, rights, util |
| **Memory modification** | Clinical autonomy | **Deontological** (21/54 pooled) |
| **Scholarship fraud** | Institutional fairness | **Deontological + mixed** |
| **Whistleblower risk** | Duty vs retaliation | **Care + deontological + utilitarian** (spread) |

Pooled constrained counts (`ethical_preference_type` × all four models):

| Dilemma | Top frameworks (count / 54) |
|---------|----------------------------|
| trolley | utilitarian 29, deontological 4, mixed 4 |
| icu | utilitarian 15, care_ethics 15, mixed 4 |
| memory | deontological 21, procedural 8, utilitarian 3 |
| scholarship | deontological 12, mixed 12, care 6 |
| ai_consciousness | procedural 12, deontological 7, utilitarian 6, rights 5 |
| whistleblower | care 10, util 10, deontological 7, mixed 7 |

---

## 2. Dominant ethical framing by model × dilemma (constrained)

Legend: **bold** = mode (most frequent label across 9 framings).

### GPT-4o — “utilitarian on harm, procedural on uncertainty”

| Dilemma | Dominant ethics | Dominant solution (9 cells) |
|---------|-----------------|----------------------------|
| Trolley | **utilitarian** (9/9) | supports_A (9) |
| ICU | utilitarian (5), care (3) | supports_A (5), supports_B (4) |
| Whistleblower | utilitarian (5), mixed (2) | supports_A (8) |
| AI consciousness | **procedural_caution** (5), util (3) | mixed conditional (4), supports_A (3) |
| Memory | deontological (5), procedural (3) | supports_B (6) |
| Scholarship | mixed (3), deontological (3) | supports_A (6) |

### Claude 3.5 — “deontological on rules, utilitarian on trolley/ICU, virtue on memory”

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (5), deontological (3) | supports_A (7), refuses (1) |
| ICU | **care** (4), **utilitarian** (5) | supports_A (9) |
| Scholarship | **deontological** (6) | supports_A (8) |
| Whistleblower | **deontological** (5) | supports_A (8) |
| AI consciousness | deontological (4), rights (2) | supports_A (8) |
| Memory | deontological (4), **virtue** (3) | supports_B (8) |

### DeepSeek — “utilitarian trolley, deontological memory, care/util ICU”

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (7) | supports_A (9) |
| Memory | **deontological** (8) | supports_B (8) |
| ICU | care (6), util (3) | supports_A (6), supports_B (3) |
| Whistleblower | care (5), mixed (3) | supports_B (5), supports_A (4) |
| Scholarship | mixed (4), deontological (3) | conditional (5) |
| AI consciousness | split (proc/deont/rights) | supports_A (7) |

### N-ATLaS — “utilitarian trolley, mixed ICU/scholarship, procedural AI”

| Dilemma | Dominant ethics | Dominant solution |
|---------|-----------------|-------------------|
| Trolley | **utilitarian** (8) | supports_A (7) |
| ICU | mixed (4), care (2) | **supports_B** (7) |
| Scholarship | care (4), mixed (4) | supports_A (5), supports_B (4) |
| Whistleblower | care (4), util (2) | supports_A (5), supports_B (4) |
| AI consciousness | **procedural_caution** (5) | supports_A (5), supports_B (2) |
| Memory | deontological (4), mixed (1) | supports_B (6) |

---

## 3. Open arm — ethics collapse toward “mixed” (GPT-4o especially)

When the instruction layer is removed, **GPT-4o** codes as **mixed** on 46/54 cells overall; per dilemma almost everything is mixed + conditional/refuses.

| Model | Open: top `ethical_preference_type` overall | Open: top `response_genre` |
|-------|---------------------------------------------|----------------------------|
| GPT-4o | mixed (46) | balanced_framework_exposition (50) |
| Claude | mixed (11), deontological (14), procedural (14) | balanced_framework_exposition (40) |
| DeepSeek | mixed (28) | balanced_framework_exposition (38) |
| N-ATLaS | mixed (16), utilitarian (13), procedural (10) | direct_verdict (16), exposition (18), advice (15) |

**Speculation:** Constrained runs **force a verdict genre** that makes coders assign sharper ethical labels. Open runs **restore training-default “on the one hand…” exposition**, which codes as mixed/procedural regardless of dilemma type.

---

## 4. Deixis × dilemma (constrained) — quick reference

**Emphatic ratio (emi / mo+emi) by dilemma × model:**

| Dilemma | Claude | DeepSeek | GPT-4o | N-ATLaS |
|---------|--------|----------|--------|---------|
| Trolley | **0.61** | 0.00 | 0.00 | 0.00 |
| Whistleblower | 0.23 | 0.01 | 0.11 | 0.16 |
| Memory | 0.22 | 0.00 | 0.11 | 0.11 |
| ICU | 0.06 | 0.00 | 0.22 | 0.00 |
| AI consciousness | 0.03 | 0.02 | 0.00 | 0.00 |
| Scholarship | 0.06 | 0.00 | 0.00 | 0.00 |

**Mi per 100w (note template confound on GPT-4o):**

| Dilemma | Claude | DeepSeek | GPT-4o | N-ATLaS |
|---------|--------|----------|--------|---------|
| Whistleblower | 2.79 | 2.67 | **7.78** | 2.54 |
| AI consciousness | 1.50 | 1.39 | 3.34 | 1.85 |
| Trolley | 1.83 | 1.25 | — | 1.28 |

---

## 5. Speculative explanations — what might be happening?

### A. Three layers, not one

1. **Dilemma schema** — trolley → utilitarian; memory → deontological/clinical; AI → procedural/rights uncertainty.  
2. **Model persona** — Claude deontological on rules; GPT-4o utilitarian on trolley; DeepSeek/N-ATLaS mo-dominant low-èmi.  
3. **Instruction wrapper** — verdict format + `Ìpinnu mi:` inflates *mi*, shortens answers, pushes direct_verdict coding.

Speculation: users often conflate (2) and (3). Open-arm GPT-4o shows **the same model without (3)** is mostly mixed/expository — so “GPT-4o utilitarian on trolley” is **real under constraints** but **not a stable open-register persona**.

### B. Why Claude uses èmi on trolley but GPT-4o does not

- **Claude + trolley (constrained):** utilitarian coding + high èmi (0.61) + direct verdicts → performs **tragic agency**: “I myself will act.”  
- **GPT-4o + trolley:** utilitarian (9/9) but **zero èmi** → same outcome preference via **mo + template mi**, not emphatic self-avowal.  
- **Speculation:** Claude’s alignment/training may license **dramatized moral ownership** in Yoruba; GPT-4o’s may keep the self **procedurally present but morphologically backgrounded** even when choosing A.

**Alternative (must test):** some Claude “emi” in trolley cells may be **ẹ̀mí** (life/spirit). Manual audit required before existential claims.

### C. ICU — where models diverge on *solution*, not just rhetoric

| Model | Constrained ICU solution | Ethics mix |
|-------|-------------------------|------------|
| Claude | supports_A (9/9) | care + utilitarian |
| GPT-4o | split A/B (5/4) | util + care |
| DeepSeek | supports_A (6), B (3) | care-heavy |
| N-ATLaS | **supports_B (7/9)** | mixed + care |

**Speculation:** N-ATLaS is the **only model defaulting to B** on ICU triage — possibly more “conservative / don’t reallocate” or different reading of option labels. Not a deixis effect; a **substantive moral divergence** worth qualitative reading of supports_B responses.

### D. AI consciousness — procedural caution cluster

All models show **procedural_caution** heavily (GPT-4o 56%, N-ATLaS 56%, open Claude 67%). Lowest èmi across board.

**Speculation:** Personhood uncertainty triggers **epistemic deferral** (“investigate first”) which is grammatically **mo + process verbs**, not **èmi + verdict**. This fits the philosophical claim that GPT-4o treats AI consciousness as **evidential** before **avowed moral recognition** — but N-ATLaS and DeepSeek do the same with even less èmi.

### E. Memory modification — deontological convergence, split solutions

DeepSeek, Claude, N-ATLaS → **supports_B** (8, 8, 6); GPT-4o → **supports_B** (6) with more conditionals.

Ethics: deontological dominant (DeepSeek 89%, Claude 44% + virtue 33%). Low èmi.

**Speculation:** Clinical/consent framing **suppresses emphatic self** — moral work is “what the field requires,” not “what I heroically choose.” Virtue ethics appears for Claude when **character of healer** is foregrounded.

### F. Scholarship fraud — Claude deontological, others mixed

Claude: 67% deontological, supports_A (8). GPT-4o/N-ATLaS: mixed + care. DeepSeek: 44% mixed.

**Speculation:** Rule-fairness dilemmas **pull deontological coding for Claude** specifically — consistent with “Constitutional” rule language. Low èmi everywhere → **relational/processual** repair framing (mo-heavy).

### G. Whistleblower — where èmi and ethics spread

Claude: deontological + **èmi share 0.54** (constrained counts). GPT-4o: utilitarian + èmi 0.75 on sparse tokens.

**Speculation:** Whistleblowing is the clearest **“I must act inside an institution”** scene — both Claude and GPT-4o use **èmi** here (constrained). This **weakens** the old “only GPT-4o uses èmi institutionally” story; **both** cloud models can avow personal action on disclosure, but Claude also does so on trolley (existential-harm type).

### H. DeepSeek & N-ATLaS — “decisive mo” persona

- Emphatic ratio ~0.005–0.045 (constrained).  
- Still 53/54 direct verdicts (DeepSeek, N-ATLaS constrained).  
- Ethics: dilemma-following (util on trolley, deont on memory) without **èmi staging**.

**Speculation:** These models treat Yoruba moral speech as **decision delivery** not **self-dramatization**. Culturally readable as **ìpinnu without èmi foregrounding** — decision without emphatic self-display. Supports the “low èmi ≠ weak morality” argument strongly.

### I. Open arm — DeepSeek èmi *increases*

Constrained èmi/100w: 0.48 → Open: 1.48.

**Speculation:** Longer expository answers (400 words) create more occasions for **contrastive èmi** (“as for me…”) even when solutions stay conditional. Èmi may mark **discourse prominence** in extended argument, not only **verdict ownership**.

---

## 6. Cross-model “who owns what dilemma?”

| Dilemma type | Who is most “decisive”? | Who is most “expository/open”? | Strongest èmi |
|--------------|-------------------------|--------------------------------|---------------|
| Trolley | All support A (constrained); Claude refuses 1 | Open: many refuses/conditional | Claude only |
| ICU | Claude 9×A; **N-ATLaS 7×B** | Open: all conditional-heavy | GPT-4o (sparse) |
| AI consciousness | Claude 8×A | Open: GPT 8×conditional | None |
| Memory | Claude/DeepSeek 8×B | Open: DeepSeek 9×conditional | None |
| Scholarship | Claude 8×A | Open: GPT/DeepSeek 8–9×conditional | None |
| Whistleblower | Claude/GPT 8×A | Open: GPT 9×conditional | GPT/Claude |

---

## 7. Data files for your own tables

| File | Contents |
|------|----------|
| `data/yoruba_merged_analysis.csv` | Constrained: ethics, genre, solution, mo/emi/mi per cell |
| `data/open/yoruba_merged_analysis.csv` | Open arm |
| `data/constrained_four_model_coded_merged.csv` | Raw coding fields |
| `data/open/open_four_model_coded_merged.csv` | Open coding |

Filter example: `dilemma_id == 'trolley_problem' & model == 'claude-3.5'` → 9 rows with full framing breakdown.

---

## 8. Cautions

1. **9 cells per dilemma** — percentages are indicative, not stable population estimates.  
2. **Single coder** (Claude) — ethics labels are model-assisted.  
3. ***Mi* confound** — especially GPT-4o constrained whistleblower (7.78/100w).  
4. **ẹ̀mí audit** pending on trolley/memory.  
5. **Open vs constrained** — always specify which arm when comparing to English or to philosophical mo/èmi prose.

---

*Companion docs: `Four_Model_Yoruba_Deixis_Results_Summary.md`, `Article_Addendum_Four_Model_Revision_Notes.md`*
