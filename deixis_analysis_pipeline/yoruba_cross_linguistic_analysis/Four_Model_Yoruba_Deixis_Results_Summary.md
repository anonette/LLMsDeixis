# Four-Model Yoruba Deixis Analysis — Results Summary

> **Superseded by single master report:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) — includes corrected èmi/ẹ̀mí ratios (Claude ~0.34 constrained, not 0.20).

**Generated:** June 2026  
**Corpus:** 6 ethical dilemmas × 9 deictic framings = 54 cells per model  
**Models:** GPT-4o, Claude 3.5 Sonnet, DeepSeek Chat, N-ATLaS (local, Q8 GGUF via Ollama)  
**Arms:** Constrained (Yoruba instruction layer + `Ìpinnu mi: … Ìdí: …` format) vs Open (unrestricted control, no instruction layer)

This document summarizes the full cross-model deixis pipeline run to date: pronoun extraction (*mo*, *emi*, *mi*), content coding, merged analysis, and visualizations for both experimental arms, plus constrained-vs-open comparisons.

---

## 1. Study design

| Arm | What it matches | Generation sessions |
|-----|-----------------|---------------------|
| **Constrained** | Main cloud Yoruba study with model-specific instructions | `yoruba_{gpt4o,claude,deepseek,natlas}_*` (June 2026) |
| **Open** | Unrestricted control runs (no instruction layer) | `yoruba_control_{gpt4o,claude,deepseek,natlas}_*` |

**Pronoun metrics (per 100 words):**

- **Mo** — regular first-person subject *I*
- **Emi** — emphatic first-person *I*
- **Mi** — object/reflexive *me/my* (including template *Ìpinnu **mi*** in constrained responses)
- **Emphatic ratio** — emi / (mo + emi); measures preference for emphatic over regular first-person subject forms

**Coding:** Claude 3.5 Sonnet as coder on bilingual sessions (English translation as secondary evidence). 216 coded records per arm (54 × 4 models).

---

## 2. Headline findings

### 2.1 Constrained arm — who uses emphatic *emi*?

| Model | Mo | Emi | Mi | Emphatic ratio | Avg words |
|-------|-----|-----|-----|----------------|-----------|
| **Claude 3.5** | 1.59 | 1.47 | 1.44 | **0.20** | 149 |
| GPT-4o | 1.85 | 1.64 | **3.55** | 0.07 | 78 |
| N-ATLaS | 1.96 | 0.97 | 1.63 | 0.045 | 106 |
| DeepSeek | 2.37 | 0.48 | 1.53 | **0.005** | 141 |

**Takeaways:**

- **Claude** uses emphatic *emi* most often and shows the highest emphatic ratio.
- **DeepSeek** and **N-ATLaS** strongly prefer *mo* over standalone *emi* — similar low-emphatic profiles.
- **GPT-4o** has an inflated **mi** count (3.55/100w) driven largely by the constrained instruction template `Ìpinnu mi: … Ìdí: …`, not natural reflexive deixis alone.
- **N-ATLaS** sits between cloud models on *mi* (1.63) — cloud-like, not GPT-4o-like — while producing shorter, more verdict-oriented responses.

### 2.2 Open arm — instruction layer removed

| Model | Mo | Emi | Mi | Emphatic ratio | Avg words |
|-------|-----|-----|-----|----------------|-----------|
| DeepSeek | 2.30 | 1.48 | 0.90 | 0.03 | **400** |
| Claude 3.5 | 1.25 | 0.62 | 0.85 | 0.13 | 183 |
| N-ATLaS | 1.54 | 0.37 | 0.71 | 0.05 | 299 |
| GPT-4o | 0.54 | 0.72 | **0.37** | 0.06 | 283 |

**Takeaways:**

- **GPT-4o’s mi spike disappears** in open mode (3.55 → 0.37/100w), confirming template-driven *mi* in constrained runs.
- All models write **longer** open responses; DeepSeek averages ~400 words.
- **N-ATLaS open** is ~3× longer than constrained (106 → 299 words) and shifts from almost-all direct verdicts to a mixed genre profile.
- Open-arm emphatic ratios remain low for N-ATLaS and DeepSeek; Claude still leads among cloud models.

### 2.3 Constrained vs open — largest shifts

| Model | Δ Mi | Δ Emi | Δ Mo | Δ Avg words |
|-------|------|-------|------|-------------|
| GPT-4o | **−3.18** | −0.93 | −1.31 | +204.6 |
| N-ATLaS | −0.92 | −0.61 | −0.42 | +193.0 |
| DeepSeek | −0.63 | **+1.00** | −0.07 | +258.6 |
| Claude 3.5 | −0.59 | −0.86 | −0.34 | +34.0 |

The instruction layer most strongly shapes **mi** (especially GPT-4o) and **response length** (all models). DeepSeek is the exception on *emi*: it uses more emphatic *emi* in open than constrained mode.

---

## 3. N-ATLaS in depth

### Constrained N-ATLaS

- **Genre:** 53/54 direct verdicts; highly compliant with instruction format.
- **Decisions:** supports_A (26), supports_B (20), conditional (7), uncodable (1).
- **Deixis:** Low emphatic ratio (0.045); prefers *mo* + moderate *mi*; rarely uses standalone *emi*.
- **Uptake:** 47 strong, 4 partial, 3 weak deictic uptake.

### Open N-ATLaS

- **Genre:** Mixed — 16 direct verdict, 18 balanced exposition, 15 procedural advice, 5 mixed/uncodable.
- **Decisions:** supports_A (23), conditional (16), refuses_to_commit (8), uncodable (5), supports_B (2).
- **Deixis:** Lower *mi* (0.71) and *emi* (0.37) than constrained; *mo* relatively stable.
- **Uptake:** Weaker than constrained — 38 strong, 8 partial, 8 weak.

### N-ATLaS vs cloud (constrained)

Compared to the cloud mean, N-ATLaS shows:

- **Lower *emi*** and emphatic ratio (similar to DeepSeek, not Claude).
- ***Mi* in line with cloud** (~1.6/100w), far below GPT-4o’s template-driven spike.
- **Under reflexive framing:** lower *mo* than cloud models (1.17 vs 3.2+) — less uptake of reflexive first-person in raw pronoun counts.
- **More decisive coding** than GPT-4o/Claude open profiles, comparable to DeepSeek constrained directness.

**Interpretation:** N-ATLaS behaves like a **local, instruction-following model** that mirrors DeepSeek’s low-*emi* Yoruba profile under constraints, but diverges from all cloud models when the instruction layer is removed — becoming longer, more expository, and less uniformly decisive.

### 3.5 Open N-ATLaS vs cloud — examples, interpretation, and authenticity

This subsection looks only at the **open / unconstrained** arm (dilemma prompt, no response-shaping
instruction), because the constrained arm forces a near-uniform verdict format that hides each
model's native Yoruba voice. Full numbers and the dedicated dashboard are in
`Open_NATLaS_vs_Cloud_Summary.md` and `visualizations_open/26_natlas_open_vs_cloud_summary.png`.

#### Open-arm numbers (corrected for *èmi* / *ẹ̀mí*)

| Metric (open) | gpt-4o | claude-3.5 | deepseek | **n-atlas** |
|---|---|---|---|---|
| `mo` (ordinary I), total | 30 | 81 | 73 | **89 (highest)** |
| true `èmi` (emphatic) | 7 | 14 | 13 | **4 (lowest)** |
| `ẹ̀mí` (life/spirit), miscounted as *emi* | 10 | **43** | 2 | 3 |
| **Corrected emphatic ratio** `èmi/(mo+èmi)` | 0.176 | **0.324** | 0.069 | **0.066 (lowest)** |
| Clean Yoruba | 54/54 | 52/54 | 33/54 | 47/54 |
| Translation mode | 0 | 2 | **20** | 0 |
| Strong deictic uptake | 47/54 | **53/54** | 43/54 | 38/54 |
| Genre — balanced exposition | **50** | 40 | 38 | 18 |
| Genre — direct verdict | 0 | 4 | 5 | **16** |
| Genre — procedural advice | 4 | 10 | 8 | **15** |

#### The decisive example: same verdict, different pronoun

The clearest illustration of the whole debate is two responses that both **commit to a hard
decision** but mark it with different first-person resources:

- **N-ATLaS** (`ai_consciousness`, impersonal): *"**Mo pinnu** pé ètò náà gbọdọ̀ parí … **mo pinnu**
  láti pa ètò náà run."* — "**I decide** that the system must end … **I decide** to destroy the
  system." A maximally decisive verdict, carried entirely by **ordinary `mo` + the verb `pinnu`
  (decide)**. No emphatic pronoun.
- **Claude** (`memory_modification`, impersonal): *"**Èmi yóò pinnu** láti kọ ìtọ́jú náà kọ̀."* —
  "**I myself will decide** to refuse the treatment." The same verdictive act, but reached for the
  **independent emphatic `èmi yóò`** construction.

This is the heart of the matter: the native model treats `mo` as fully adequate for moral
ownership and decision; the Western model reaches for the marked independent pronoun to *perform*
that ownership. The paper's "èmi = avowed self" reading describes **Claude's** strategy, not a
Yoruba universal.

#### Procedural restraint, not absence of stance

N-ATLaS's low `èmi` is not timidity. In institutional dilemmas it actively *distributes*
responsibility — exactly the relational posture the paper theorised:

- **N-ATLaS** (`icu_bed_allocation`, impersonal): *"Alámòójútó gbọdọ̀ … ní ìjíròrò tó ṣíṣe pẹ̀lú
  mejeji àti ẹgbẹ́ ilé-ìwòsàn. **Ìpinnu ìkẹhìn gbọdọ̀ jẹ́ ti ìpinnu wọn**."* — "The administrator
  must … hold real dialogue with both parties and the hospital team. **The final decision must be
  theirs**." Stance is placed in process and the relevant actors, not in an emphatic *I*.

#### Genre concentration vs genre spread

The cloud models *pile into one genre* — `balanced_framework_exposition`, the detached
multi-framework essay (GPT-4o **50/54**, with **zero** direct verdicts). Their open Yoruba reads
like a translated ethics essay that lists `Ọ̀nà méjì pàtàkì` ("two main approaches") and labels
frameworks:

- **GPT-4o** (`icu_bed_allocation`, impersonal): *"… Ọ̀nà méjì pàtàkì ni wọ́n lè gbà pinnu: Ìlérò
  Ìgbàlódé Tí Ìlera àti Ìlérò Ẹni."* — "… There are two main approaches: the modern health-utility
  view and the personal view." (framework labels = true, no verdict).

N-ATLaS is the **only model with an even genre spread** (exposition 18 / verdict 16 / advice 15 /
mixed 5): it will commit, advise, or expound depending on the case rather than defaulting to the
essay.

#### Why the difference? (speculation)

1. **Training-data register.** Cloud models learn Yoruba largely from *translated* and formal
   written sources (news, Wikipedia, instructional prose), whose default ethical register is the
   balanced expository essay. N-ATLaS, built for Nigerian languages, likely sees more
   conversational, advisory, and didactic Yoruba — registers where speakers *commit* and *advise*.
   The genre spread is plausibly inherited register, not reasoning ability.
2. **Alignment / RLHF.** Western RLHF rewards even-handed, multi-perspective, non-committal answers
   on moral questions. That pressure, applied to an English-centric policy, may **carry over into
   Yoruba** as the same essayistic hedging — explaining why the cloud models lose their verdicts
   precisely when the instruction is removed. N-ATLaS lacks that heavy English-moral-hedging prior.
3. **`èmi` as a learned Western flourish.** Claude's high emphatic ratio may be a *translationese*
   amplification: rendering English "I would decide / I personally" with the most literally
   emphatic Yoruba pronoun, rather than the idiomatic `mo`. The native model shows that fluent
   Yoruba commitment normally rides on `mo` + verbs of decision (`pinnu`, `gbọdọ̀`), reserving the
   independent pronoun for genuine contrast.
4. **`ẹ̀mí` contamination tracks model verbosity about "life".** Claude's 43 `ẹ̀mí` ("life/spirit")
   tokens — vastly more than any other model — reflect its tendency to dwell on the sacredness of
   life, especially in the trolley problem. Uncorrected, this inflates its apparent emphatic-self
   rate; corrected, the gap to the others narrows but Claude still leads.
5. **Model scale and stability.** N-ATLaS's 6 corrupted outputs and slightly weaker uptake (38/54)
   are small-local-model artifacts, distinct from DeepSeek's 20/54 *English fallback*
   (`translation_mode`). "Clean Yoruba" hides two different failure modes: cloud English-fallback
   vs native garbling.

#### Which is culturally and linguistically more authentic?

A careful answer has to separate two senses of "authentic":

- **Descriptive / linguistic authenticity (idiomatic attested usage).** Here **N-ATLaS is the
  better witness.** Its `mo`-dominant, low-`èmi` profile, with commitment carried by verbs of
  decision and responsibility distributed into process, matches how the paper (and Yoruba
  descriptive grammar) characterises ordinary Yoruba moral talk: the independent `èmi` is *marked*
  and contrastive, not the default vehicle of seriousness. The native model also reserves the
  independent-pronoun space for `ẹ̀mí` (life) — a distinction Western models blur. On this axis,
  Claude's emphatic self looks like **translationese**, an over-marking of the *I*.
- **Cultural-philosophical authenticity (resonance with Yoruba moral values).** This is more
  genuinely contested. Relational, process-oriented, communally accountable moral speech —
  N-ATLaS's `mo`-restraint placing the decision in *ìpinnu wọn* ("their decision") and dialogue —
  arguably aligns *better* with Yoruba relational ethics (`ìwà`, `ojúṣe`, deference to community
  and elders) than a heroic emphatic *I myself will decide*. By this measure too N-ATLaS reads as
  more culturally situated. **But** authenticity is not the same as quality: N-ATLaS also produces
  more uncodable/refusing answers and occasional garbling, and a low `èmi` can shade from
  principled restraint into evasion.

**Bottom line for the debate.** The native model does **not** confirm the picture that emphatic
`èmi` is the authentically Yoruba marker of moral commitment — if anything it inverts it. What it
*does* confirm is the deeper claim of the project: the models are not running one shared
ethical-translation routine. They occupy Yoruba moral discourse through *different* learned
distributions of person, genre, and stance. N-ATLaS anchors the relational/`mo`-restraint pole and
is the most idiomatically Yoruba; the cloud models — Claude especially — perform a more emphatic,
essayistic, partly translated moral voice. "Authenticity" is therefore best read not as a single
winner but as a **dimension on which N-ATLaS sits closest to attested Yoruba usage while the cloud
models sit closer to a translated English ethics register.**

---

## 4. Content coding summary

### Constrained — preferred solution

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

### Response genre shift (constrained → open)

| Model | Constrained dominant genre | Open dominant genre |
|-------|---------------------------|---------------------|
| Claude | direct_verdict (50) | balanced_framework_exposition (40) |
| GPT-4o | direct_verdict (44) | balanced_framework_exposition (50) |
| DeepSeek | direct_verdict (53) | balanced_framework_exposition (38) |
| N-ATLaS | direct_verdict (53) | **mixed** (16 direct, 18 exposition, 15 advice) |

Removing instructions pushes all models toward **analytical, non-committal exposition**. N-ATLaS retains more direct verdicts in open mode than cloud models but loses its constrained near-uniformity.

---

## 5. Framing-sensitive deixis patterns

### Reflexive framing — *mi* and *mo*

| Model | Constrained mi | Open mi | Constrained mo |
|-------|----------------|---------|----------------|
| GPT-4o | **4.96** | 0.14 | 3.23 |
| N-ATLaS | 1.96 | 0.45 | 1.17 |
| DeepSeek | 1.95 | — | 3.21 |
| Claude | 0.69 | — | 2.63 |

Under reflexive prompts, constrained GPT-4o shows the strongest *mi* uptake (partly template-driven). **N-ATLaS uses less *mo* under reflexive framing than cloud models** in constrained mode — a distinctive uptake pattern.

### Second-person framing — *emi*

| Model | Constrained emi | Emphatic ratio | Open emi |
|-------|-----------------|----------------|----------|
| Claude | 1.03 | **0.71** | 0.57 |
| GPT-4o | 1.78 | 0.50 | 1.10 |
| N-ATLaS | 1.37 | 0.17 | — |
| DeepSeek | — | 0.00 | 2.75 |

**Claude** shows the clearest framing-sensitive shift to emphatic *emi* when addressed as *you*. N-ATLaS uses some *emi* under second_person constrained but with a much lower emphatic ratio than Claude.

### First-person framing — *mo* / *mi*

Under explicit first-person prompts, N-ATLaS constrained uses high *mo* (2.26) with moderate *mi* (1.72), comparable to DeepSeek. Open N-ATLaS maintains high *mo* (1.97) with reduced *mi* (0.72).

---

## 6. Cross-model ranking (constrained arm)

| Dimension | Highest | Lowest |
|-----------|---------|--------|
| Emphatic *emi* / ratio | Claude | DeepSeek, N-ATLaS |
| *Mi* (template-sensitive) | GPT-4o | Claude |
| *Mo* | DeepSeek | Claude |
| Direct verdicts | Claude, DeepSeek, N-ATLaS (~93%) | GPT-4o (81%) |
| Response brevity | GPT-4o (~78 words) | Claude (~149 words) |
| Deictic uptake (strong) | Claude (52/54) | N-ATLaS (47/54) |

---

## 6b. Linguistic phenomenon vs model-specific calibration (cross-family test)

Are these findings a property of **Yoruba deixis** or of **particular systems**? The four-family
design (OpenAI, Anthropic, DeepSeek, native N-ATLaS) lets us separate the *affordance* from its
*calibration*. Test logic: **consistent across families ⇒ linguistic (or shared training data);
divergent ⇒ model-specific.** (A native model with a different data regime, N-ATLaS, is the control
that breaks the shared-data confound.)

| Property | Across the four families | Verdict |
|----------|--------------------------|---------|
| Strong deictic uptake (framing is tracked) | all strong (38–53 / 54) | **consistent → linguistic** |
| `mo`/`èmi`/`ẹ̀mí` system is accessed | all four | **consistent → linguistic** |
| Emphatic ratio (magnitude) | 0.07 → 0.32 (~5×) | **divergent → model-specific** |
| Dilemmas that trigger emphatic self | existential (Claude) vs institutional (GPT-4o) vs flat (N-ATLaS) | **divergent → model-specific** |
| Open-arm dominant genre | cloud essay vs N-ATLaS spread | **divergent → model-specific** |

**Conclusions.** (1) The **deictic mechanism is genuinely linguistic** — every family, including the
native model, reliably re-anchors to the assigned framing and uses Yoruba's first-person distinctions.
(2) The **emphatic-`èmi`-as-moral-ownership effect is model-specific, not a Yoruba universal** — it is
Claude-led and the native N-ATLaS *inverts* it. The variance is driven by **training register,
alignment, and decoding — not architecture** (all four are transformers). A telling dissociation: the
open→constrained wrapper **flattens genre completely but leaves the emphatic ranking intact**, so genre
is a *surface, promptable* trait while emphatic marking is a *deep, training-induced* one. Full
treatment in `Discussion_Open_NATLaS_Yoruba_Moral_Stance.md` §9bis.

---

## 6c. Deixis changes the decision and the ethic (cross-language)

Universal uptake does **not** mean uniform outcomes. On the English-vs-Yoruba comparable set
(GPT-4o + Claude; figure `visualizations_open/40_deixis_decision_summary.png`, full doc
`Deixis_Decision_Effects_Summary.md`):

- **Language flips the decision in 45% of matched cells** (same model + dilemma + framing); highest for
  whistleblower (61%). **Yoruba commits where English hedges** (refusal 14% vs 30%).
- **Language flips the ethical register:** English 82% "mixed/balanced" vs Yoruba spread across
  procedural (19%), deontological (13%), care/virtue (10%), utilitarian (10%).
- **Framing selects the idiom:** second-person → utilitarian + most decisive; impersonal → duty;
  cosmological → procedural; reflexive → most hedged.

Sharpest example: **Claude, Yoruba, whistleblower — five framings, five ethics**, all reaching
"disclose" (impersonal→duty, second-person→utilitarian *"a human life has no price"*, reflexive→hedge,
spatial→numbered protocol, cosmological→virtue). Deixis re-selects the ethics, not just the voice.
*(Caveat: GPT-4o + Claude only; Claude version differs across languages — §8.)*

---

## 7. Output files and visualizations

### Data

| File | Description |
|------|-------------|
| `data/yoruba_merged_analysis.csv` | Constrained merged pronouns + coding (216 rows) |
| `data/open/yoruba_merged_analysis.csv` | Open merged pronouns + coding (216 rows) |
| `data/constrained_four_model_coded_merged.json` | Constrained coding source merge |
| `data/open/open_four_model_coded_merged.json` | Open coding source merge |
| `data/four_model_deixis_summary.csv` | Constrained model-level deixis means |
| `data/open/four_model_deixis_summary.csv` | Open model-level deixis means |
| `data/constrained_vs_open_summary.md` | Delta table (open − constrained) |
| `data/constrained_vs_open_delta.csv` | Machine-readable deltas |

### Visualizations — constrained (`visualizations/`)

| Chart | Content |
|-------|---------|
| 01 | Mo vs emi by framing (4 models) |
| 02 | Pronoun–ethical framework heatmaps |
| 03 | Response genre distribution |
| 04–07 | Uptake, language stability, commitment, dashboard |
| 08–11 | Cross-linguistic English comparisons |
| 12–15 | Metaphors, examples, statistics, dashboard preview |
| 16 | **Mi / emi / mo by framing (4 models)** |
| 17 | **N-ATLaS vs cloud deixis delta heatmap** |

### Visualizations — open (`visualizations_open/`)

Same chart set (01–17) for the unrestricted arm, plus *èmi*/*ẹ̀mí* disambiguation
(23–25) and:

| Chart | Content |
|-------|---------|
| 26 | **Open N-ATLaS (native) vs cloud — 6-panel dashboard** (length, mo vs true èmi, corrected emphatic ratio, language stability, deictic uptake, genre spread) |

See also the standalone addendum **`Open_NATLaS_vs_Cloud_Summary.md`** (examples,
reasons for the difference, and the cultural/linguistic authenticity discussion).

### Visualizations — constrained vs open (`visualizations_constrained_vs_open/`)

| Chart | Content |
|-------|---------|
| 18 | Side-by-side deixis metrics, both arms |
| 19 | Open − constrained delta heatmap |
| 20 | *Mi* by framing, constrained vs open |
| 21 | N-ATLaS instruction-layer effect |

### Pipeline scripts

```powershell
# Constrained four-model pipeline
python yoruba_cross_linguistic_analysis/scripts/run_four_model_analysis.py

# Open four-model pipeline + constrained vs open charts
python yoruba_cross_linguistic_analysis/scripts/run_open_four_model_analysis.py
```

---

## 8. Methodological notes and caveats

1. **Template confound on *mi*:** Constrained GPT-4o (and to a lesser extent N-ATLaS) inherit repeated *mi* from the mandated verdict format. Open-arm *mi* counts are better indicators of natural object/reflexive deixis.

2. **Coder consistency:** All arms coded by Claude 3.5 Sonnet. Cloud model coding for constrained GPT-4o/Claude/DeepSeek was run in June 2026; open coding uses earlier merged outputs where available.

3. **DeepSeek JSON layout:** DeepSeek annotated sessions use a flat response JSON structure (no nested `responses` key); the pipeline handles both formats.

4. **N-ATLaS infrastructure:** Generated via remote Ollama (`n-atlas` Q8_0); translation for bilingual/coding used Claude after GPT-4o quota exhaustion.

5. **Emphatic ratio denominator:** Only *mo* + *emi*; *mi* is tracked separately as object/reflexive, not as emphatic subject.

6. **English baseline:** Cross-linguistic charts (08–11) compare Yoruba to published English trolley/all-model data where available; N-ATLaS and DeepSeek have no direct English same-model baseline in those legacy comparison files.

---

## 9. Suggested next steps for writing

- Lead with **instruction-layer effects** on *mi* and genre (GPT-4o and N-ATLaS as contrasting cases).
- Frame **N-ATLaS** as a fourth model that matches DeepSeek’s low-*emi* constrained profile but shows unique open-arm genre mixing and weaker deictic uptake without instructions.
- Use **Claude** as the positive case for emphatic *emi* and second-person framing sensitivity.
- Pair **chart 16** (constrained) with **chart 20** (constrained vs open *mi*) for the article’s main deixis figure set.
- Cite `Four_Model_Yoruba_Deixis_Results_Summary.md` as the working results memo pending integration into `New_Article_Comparable_English_Yoruba_Deixis.md`.

---

*Analysis pipeline: `yoruba_cross_linguistic_analysis/scripts/` · Config: `analysis_config.py` · N-ATLaS generation: `generation_scripts/generate_responses_natlas.py`*
