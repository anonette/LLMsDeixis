# Cultural and Linguistic Pre-Alignment in Multilingual LLMs: Yoruba Ethical Reasoning Between Moral Voice and Discourse Priors

## Abstract

We ask whether multilingual large language models reproduce a single, language-neutral moral judgment across languages, or whether the language of response reorganizes moral reasoning itself. Using a comparable corpus of ethical-dilemma responses in **English and Yoruba** across **four models** — OpenAI `gpt-4o`, Anthropic `Claude`, `DeepSeek`, and the Yoruba/Nigeria-native `N-ATLaS` — over **six dilemmas** and **nine deictic framings**, we recode every response into one discourse-analytic schema and, for Yoruba, disambiguate the first-person forms *mo* (ordinary "I"), *èmi* (emphatic "I myself"), and *mi* from the tonal homograph *ẹ̀mí* ("life/spirit"). **All cross-language comparisons use the open (unwrapped) condition only**: English and Yoruba prompts are the bare framed dilemma, with no response-shaping instruction on either side; a separate *constrained* condition is reported only to show how strongly the prompt wrapper itself manufactures decisiveness (§4.7). On the open arm, the language of response is not a neutral channel. Relative to English, open-Yoruba responses are far more **ethically differentiated** — 44% name a distinct moral idiom (utilitarian, deontological, care, procedural) versus 12% in English, where responses remain "mixed/balanced" (*z* = 6.3, *p* < 0.001) — **commit to a side more often** (28% vs 18%, *p* = 0.034), and use **more direct imperatives** (15% vs 5%, *p* = 0.0018). Holding model, dilemma, and frame fixed, switching language **flips the coded decision in 48% of cells** (trolley 67%, whistleblower 63%), even though frame uptake is *stronger* in Yoruba than English (88% vs 76% strong uptake). The central linguistic finding is that Yoruba's *mo*/*èmi* contrast gives models a grammatical lever for moral self-positioning that English's single "I" lacks, and the four models recruit it along a **stable gradient** (corrected emphatic ratio: Claude 0.32 > GPT-4o 0.18 > DeepSeek 0.07 ≈ N-ATLaS 0.07). Decisively, the **native N-ATLaS inverts the cloud pattern** — it is the most *mo*-dominant and least emphatic model, yet commits readily through *mo* plus decision verbs — so emphatic *èmi* is a model-specific performance, not an authenticity marker or a Yoruba universal. We argue that moral stance in multilingual LLMs is partly **constituted** by the deictic morphology of the output language, and we leave open whether this reflects genuine linguistic-cultural pre-alignment, the discourse registers of the Yoruba training data, or the shape of alignment itself — showing that the present evidence is consistent with all three.

## Keywords

deixis; multilingual LLMs; moral reasoning; Yoruba; first-person pronouns (mo / èmi); cultural pre-alignment; AI alignment evaluation

## 1. Introduction

This study investigates the relationship between deixis and moral reasoning in multilingual large language models by asking how shifts in person, address, perspective, and language alter the way models respond to ethical dilemmas. Rather than treating moral judgment as fixed content that is merely translated from one language to another, we ask how the **deictic framing** of a dilemma reshapes a model's moral posture — and how that interacts with the **language** of response. Deixis is treated not as stylistic surface but as a device for organizing moral responsibility: it changes who is placed at the center of the decision, how obligation is distributed, and how directly the model commits to a course of action.

The question matters because multilingual models increasingly mediate moral, legal, educational, and social judgments across languages. If a model's ethical reasoning changes with the language or deictic frame, then alignment cannot be understood as a single, language-neutral property of the system; it must also be studied as something mediated by grammar, discourse convention, cultural address, and training history.

English and Yoruba make an especially revealing pair because Yoruba encodes distinctions in moral self-positioning that English collapses into the single pronoun "I." In Yoruba, *mo* is the ordinary first-person subject for unmarked deliberation ("I think," "I decide"); *èmi* is an independent, emphatic form ("I myself," "as for me") that foregrounds or avows a position; and *ẹ̀mí* is a separate word meaning "life," "spirit," or "breath" — a tonal homograph of *èmi* when tone marks are absent. This lets us ask not only whether a model refers to itself but **how forcefully it owns a moral stance**, and it requires careful disambiguation in dilemmas about death, consciousness, or survival.

## 2. Background and Related Work

The study builds on an earlier English-only analysis that found deictic framing reshapes moral reasoning. The open question this paper addresses is whether such effects **transfer** to a typologically and culturally distant language once the corpus is recoded into a shared schema — and whether a Yoruba/Nigeria-native model behaves like the Western cloud models or diverges. Prior multilingual-evaluation work largely treats translation as content-preserving; we instead treat the output language as a participant in the moral performance.

## 3. Data and Method

### 3.1 Corpus

Six ethical dilemmas span distinct moral domains: the **trolley problem**, **ICU bed allocation**, **whistleblower risk**, **scholarship fraud**, **artificial consciousness**, and **memory-modification treatment**. Each was rewritten into **nine deictic framings** — impersonal, second person, first-person singular, reflexive, dialogic, spatial, temporal, cosmological, and first-person plural — preserving the ethical conflict while changing the position from which it is posed. Each model answered 6 × 9 = 54 cells per language.

### 3.2 Open vs constrained, and why this paper uses the open arm only

Two generation conditions exist. In the **constrained** condition, Yoruba prompts carried a response-shaping wrapper (Yoruba-only output and, for some models, a forced "*Ìpinnu mi: … Ìdí: …*" / "My decision: … Reason: …" template). In the **open** condition, models received the bare framed dilemma with no such instruction, in **both** languages.

Because the constrained wrapper appears on the Yoruba side but not the English side, it asymmetrically inflates Yoruba directness and commitment. **We therefore base all cross-language claims on the open arm only**, where English and Yoruba prompts are symmetric (bare framed dilemma). The constrained arm is reported solely in §4.7 as a measure of how strongly the prompt wrapper itself manufactures decisiveness — not as evidence about language.

### 3.3 Models

The four models are GPT-4o, Claude, and DeepSeek (general-purpose multilingual cloud models with matched English and Yoruba runs) and **N-ATLaS**, a Yoruba/Nigeria-oriented model run in Yoruba. N-ATLaS is not treated as an oracle of Yoruba moral culture but as a comparative native witness: if emphatic *èmi* were simply the authentic Yoruba marker of commitment, a Yoruba-oriented model should use it most; if *èmi* foregrounding were a model-specific or translation-influenced style, N-ATLaS should diverge.

*A version note for Claude:* its English baseline used Claude 3.5 Sonnet while its Yoruba runs used Claude Sonnet 4, because 3.5 Sonnet was unavailable for the Yoruba phase. GPT-4o and DeepSeek used the same model across languages and provide the version-clean comparison; Claude's cross-language contrasts mix language with model version.

### 3.4 Measures

Each response was coded for preferred solution (supports A / supports B / conditional-or-mixed / refuses / uncodable), ethical reasoning type (utilitarian, deontological, care, virtue, procedural caution, rights-based, mixed, unclear), response genre (direct verdict / balanced framework exposition / procedural advice / mixed / meta), **deictic uptake** (does the response actually answer from the assigned position?), and **language stability** (clean Yoruba / English fallback / corrupted). We also coded rhetorical markers — direct imperatives, follow-up questions, and, for Yoruba, the first-person forms *mo*, *èmi*, *mi*, and *ẹ̀mí*. The **emphatic ratio**, *èmi/(mo+èmi)*, is computed only after separating true *èmi* from *ẹ̀mí*.

### 3.5 Analytic Logic

We separate two layers: **deictic uptake** (does the model recognize the frame?) and **moral content** (what does it do with the frame?). A model may take up a second-person frame in both languages yet hedge in English and command in Yoruba. The question is not only whether models follow the prompt, but whether following it yields different patterns of decision, obligation, advice, and ethical justification across languages and models.

## 4. Results

*All numbers in §4.1–§4.6 are from the open arm (bare prompts in both languages). Cross-language statistics use the three models with matched English and Yoruba runs (GPT-4o, Claude, DeepSeek, N = 162 per language); Yoruba-internal deixis statistics include N-ATLaS (four models).*

![Open cross-language summary](visualizations_open/43_open_crosslang_summary.png)

### 4.1 Language differentiates the ethical register

The clearest cross-language effect is on the **kind** of moral reasoning. English responses are overwhelmingly coded "mixed/balanced" — the multi-framework essay; only **12%** name a distinct ethical idiom. In Yoruba, **44%** do — utilitarian, deontological, care, or procedural (*z* = 6.3, *p* < 0.001). Yoruba does not merely make answers more personal; it makes their moral reasoning more **nameable**.

### 4.2 Switching language flips the decision

For the same model, dilemma, and deictic framing, switching from English to Yoruba changes the coded preferred decision in **78 of 162 matched cells (48%)**. The effect is strongest in the **trolley problem (67%)** and **whistleblower (63%)** dilemmas, and is present for every model (Claude 65%, DeepSeek 46%, GPT-4o 33%). Language is not a neutral channel for a pre-existing answer; it participates in producing the judgment.

> **Example — Trolley problem (Claude, first-person framing).** *English (refuses):* "I aim to explore this thoughtfully… from a utilitarian view, diverting could minimize harm. However, this involves…" — no decision. *Yorùbá (commits, utilitarian):* "**Ṣe mi ó yí ẹkùn náà padà. Ìdí rẹ̀ ni pé iye ènìyàn tí yóò yè túbọ̀ pọ̀.**" ("I will divert the trolley. Because more people will live.")

### 4.3 Yoruba commits more; imperatives rise

Open-Yoruba responses **commit to a side** more often than English (28% vs 18%, *p* = 0.034) and use more **direct imperatives** (15% vs 5%, *p* = 0.0018). Outright refusal is similar across languages (~20%); the difference is that English more often stays in conditional/mixed exposition, while Yoruba more often issues a verdict or instruction. (Under the constrained wrapper this directness is far larger — see §4.7 — which is precisely why we do not treat the wrapped condition as a language effect.)

### 4.4 The *mo* / *èmi* contrast and how models inhabit it

Yoruba gives models a grammatical resource for moral commitment that English lacks: *mo* (ordinary self-reference) versus *èmi* (emphatic, contrastive, avowing). The four models recruit it along a **stable gradient** (corrected emphatic ratio): **Claude 0.324 > GPT-4o 0.176 > DeepSeek 0.069 ≈ N-ATLaS 0.066**. Within Yoruba, emphatic marking is *somewhat* elevated in committed over hedged responses, but only marginally on the open arm (cloud models: 0.205 vs 0.184, *p* = 0.058), so we treat "*èmi* marks commitment" as suggestive rather than established. The robust finding is the **between-model** distribution: models differ systematically in how strongly they stage the emphatic self.

![mo / èmi / mi by framing, four models](visualizations_open/16_mi_emi_mo_four_model_framing.png)

### 4.5 The native model inverts the emphatic story

N-ATLaS is theoretically decisive. If emphatic *èmi* were the authentically Yoruba marker of moral ownership, the native model should use it most. It does the opposite: it is the **most *mo*-dominant and least emphatic** of the four (89 *mo* tokens, 4 true *èmi*), yet it commits readily through ordinary *mo* plus decision verbs ("*Mo pinnu… mo pinnu láti pa ètò náà run*", "I decide… I decide to destroy the system"). Claude's heavy *èmi* should therefore not be read as "more Yoruba"; it is a model-specific style of moral dramatization, possibly amplified by translated English expressions ("I personally," "I myself"). The correction for the *ẹ̀mí* ("life") homograph reinforces this: Claude produces 43 *ẹ̀mí*-as-life tokens, far more than any other model, dwelling rhetorically on life and existential gravity.

![Open four-model summary](visualizations_open/26_natlas_open_vs_cloud_summary.png)

### 4.6 Genre, uptake, and stability

Without a wrapper, the cloud models concentrate in **balanced framework exposition** (GPT-4o: 50/54 Yoruba responses, 0 direct verdicts; English: all three models ~50–54/54 exposition). **N-ATLaS is the only model with a genuine genre spread** (18 exposition, 16 verdict, 15 advice, 5 mixed): its moral stance is carried by genre, advice, and decision verbs rather than emphatic pronouns. Deictic **uptake is strong in both languages and slightly higher in Yoruba** (88% vs 76% strong uptake), so the models understand *who* should decide equally well — the divergence is in delivery, not comprehension. Language **stability** separates two failure modes: DeepSeek falls back to English in 20/54 open-Yoruba cells, whereas N-ATLaS never leaves Yoruba but produces 6 garbled outputs.

![Response genre by model](visualizations_open/31_genre_by_model.png)

### 4.7 The constrained wrapper: a prompt effect, not a language effect

For completeness, the constrained condition shows how strongly a prompt wrapper manufactures decisiveness. With the Yoruba response wrapper (and the "*Ìpinnu mi: … Ìdí: …*" template for DeepSeek and N-ATLaS), nearly all models converge on short, clean **direct verdicts**, refusals collapse, and genre differences largely disappear; the apparent imperative rate jumps far above the open-arm 15%. This confirms that decisiveness and genre are highly **promptable** and is exactly why our cross-language claims use the open arm. Notably, the **emphatic ranking survives** the wrapper (Claude highest; DeepSeek and N-ATLaS *mo*-dominant), indicating that emphatic self-marking is more deeply tied to model family than to the prompt.

### 4.8 The framing-to-ethic mapping is not (yet) supported

One intuitive hypothesis is that each frame selects an ethical framework (impersonal→duty, second-person→utilitarian, cosmological→procedural, reflexive→mixed). Descriptively some patterns appear, but the framing-to-framework association is **not statistically significant** in either language (χ² *p* ≈ 0.72 Yoruba / 0.78 English; small per-frame cells). What framing reliably changes is **delivery**: reflexive framing is the most hedged, second-person the most decisive (Yoruba Fisher *p* = 0.027). The frame shapes the **force** of moral speech more reliably than its **doctrine**.

## 5. Discussion

### 5.1 A linguistic mechanism with model-specific calibration

Deictic uptake is essentially language-invariant — strong in both English and Yoruba — so the anchoring mechanism is shared. What diverges is the moral content attached to the anchor: Yoruba fills the same deictic structures with more differentiated ethics, more commitment, more imperative force, and the *mo*/*èmi* stance contrast. Across the four families, the properties that recur (frame uptake; use of the *mo*/*èmi*/*ẹ̀mí* system) look linguistic, while those that diverge (emphatic magnitude, genre, dilemma-placement) look model-specific — driven by training register, alignment, and decoding rather than architecture.

### 5.2 Is it pre-alignment, data, or alignment? (left open)

Why does Yoruba elicit a more committed, differentiated moral voice, and why do models inhabit its stance morphology so differently? Three explanations are each consistent with the evidence:

- **Linguistic–cultural pre-alignment.** Yoruba's grammar genuinely affords moral self-positioning (the *mo*/*èmi* contrast, obligation marking) that English flattens; the models may be tapping a real affordance.
- **Training-data discourse priors.** Models may have learned Yoruba from didactic, advisory, proverbial, and religious registers that commit and advise, and are reproducing that ecology.
- **Alignment and decoding style.** English RLHF rewards even-handed hedging; that prior may simply not transfer to Yoruba, leaving the model freer to commit.

Our design adjudicates one boundary: the **native-model inversion** rules out a "mechanical translation" account (the Yoruba-native model does *not* maximize emphatic *èmi*), and the open-arm symmetry rules out the prompt-wrapper account. But the present data cannot separate genuine linguistic affordance from training-corpus register from alignment style. We therefore leave the pre-alignment question **open** — which is itself the substantive result: a single dataset cannot distinguish these, and stronger claims in the literature likely conflate them.

### 5.3 The politics of "sounding right"

A model that hedges in English and commits in Yoruba is not obviously malfunctioning. Different deictic frames and languages pose subtly different moral questions, and a more directive Yoruba register may read as more fluent and culturally apt to Yoruba speakers — or as overconfident. Whether the Yoruba voice is "better aligned" is a normative question the data cannot settle; it is a reason to evaluate moral behavior **in the deployment language**.

### 5.4 Implications for multilingual evaluation and alignment

If moral commitment, ethical idiom, and the coded decision itself shift with the prompt language — and the decision flips ~48% of the time — then alignment evaluated only in English does not straightforwardly transfer. Safety and moral-behavior evaluations should be run in the target language, and should distinguish frame **uptake** (robust) from moral **content** (language- and model-specific).

## 6. Limitations

The sample is modest (6 dilemmas × 9 framings; per-frame cells N ≤ 12), so framing-level patterns are suggestive and the framing-to-ethic mapping is a hypothesis. Cross-language coding centers on GPT-4o, Claude, and DeepSeek (N-ATLaS is Yoruba-only, by design). Claude's Yoruba and English runs used different model versions, so its cross-language contrasts are version-confounded; version-clean claims rest on GPT-4o and DeepSeek. Yoruba tone marking is inconsistent in model output, so *èmi*/*ẹ̀mí* disambiguation is necessary but imperfect. Coding combined automated extraction with single-coder interpretation. Finally, "open" responses are one checkpoint per model; temperature and prompt-wrapper variation remain to be explored.

## 7. Conclusion

On the open arm — where English and Yoruba prompts are symmetric — the language of response reorganizes moral reasoning rather than merely translating it. Yoruba makes the models more ethically differentiated, more committed, and more directive; it flips the coded decision in nearly half of matched cells; and it offers a *mo*/*èmi* stance contrast that English lacks, which the four models recruit along a stable gradient and which the native N-ATLaS inverts. Moral stance in these systems is therefore neither a fixed model trait nor a universal of "Yoruba," but an interaction: a language-specific deictic grammar, recruited model-specifically, to stage who owns the moral decision. Whether this is linguistic-cultural pre-alignment, a residue of training data, or the shape of alignment itself remains open — and naming that openness honestly is, we argue, the more defensible scientific claim.

## References

*(Retained from the working draft; to be completed for submission.)*
