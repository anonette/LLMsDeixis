# Cultural and Linguistic Pre-Alignment in Multilingual LLMs: Yoruba Ethical Reasoning Between Moral Voice and Discourse Priors

## Abstract

We ask whether multilingual large language models reproduce a single, language-neutral moral judgment across languages, or whether the language of response reorganizes moral reasoning itself. Using a comparable corpus of ethical-dilemma responses in **English and Yoruba** across **four models** — OpenAI `gpt-4o`, Anthropic `Claude`, `DeepSeek`, and the Yoruba/Nigeria-native `N-ATLaS` — over **six dilemmas** and **nine deictic framings**, we recode every response into one discourse-analytic schema and, for Yoruba, disambiguate the first-person forms *mo* (ordinary "I"), *èmi* (emphatic "I myself"), and *mi* from the tonal homograph *ẹ̀mí* ("life/spirit"). **All cross-language comparisons use the open (unwrapped) condition only**: English and Yoruba prompts are the bare framed dilemma, with no response-shaping instruction on either side; a separate *constrained* condition is reported only to show how strongly the prompt wrapper itself manufactures decisiveness (§4.7). On the open arm, the language of response is not a neutral channel. Relative to English, open-Yoruba responses are far more **ethically differentiated** — 44% name a distinct moral idiom (utilitarian, deontological, care, procedural) versus 12% in English, where responses remain "mixed/balanced." This effect is large and **survives clustering by dilemma and by model** (logistic regression, cluster-robust *p* < 0.001). Holding model, dilemma, and frame fixed, switching language **flips the coded decision in 48% of cells** (trolley 67%, whistleblower 63%; cluster-bootstrap 95% CI [36%, 59%]), even though frame uptake is *stronger* in Yoruba than English (88% vs 76% strong uptake). Open-Yoruba responses are also somewhat more committed (28% vs 18%) and more imperative (15% vs 5%), but — unlike the differentiation effect — this directness is **concentrated almost entirely in Claude** (commit 22%→57%, imperative 2%→30%; GPT-4o, the version-clean model, does not shift) and does not survive model-clustering, so we report it as directional and largely Claude-specific. The central linguistic finding is that Yoruba's *mo*/*èmi* contrast gives models a grammatical lever for moral self-positioning that English's single "I" lacks, and the four models recruit it along a **stable gradient** (corrected emphatic ratio: Claude 0.32 > GPT-4o 0.18 > DeepSeek 0.07 ≈ N-ATLaS 0.07). Decisively, the **native N-ATLaS inverts the cloud pattern** — it is the most *mo*-dominant and least emphatic model, yet commits readily through *mo* plus decision verbs — so emphatic *èmi* is a model-specific performance, not an authenticity marker or a Yoruba universal. We argue that moral stance in multilingual LLMs is partly **constituted** by the deictic morphology of the output language, and we leave open whether this reflects genuine linguistic-cultural pre-alignment, the discourse registers of the Yoruba training data, or the shape of alignment itself — showing that the present evidence is consistent with all three.

## Keywords

deixis; multilingual LLMs; moral reasoning; Yoruba; first-person pronouns (mo / èmi); cultural pre-alignment; AI alignment evaluation

## 1. Introduction

This study investigates the relationship between deixis and moral reasoning in multilingual large language models by asking how shifts in person, address, perspective, and language alter the way models respond to ethical dilemmas. Rather than treating moral judgment as fixed content that is merely translated from one language to another, we ask how the **deictic framing** of a dilemma reshapes a model's moral posture — and how that interacts with the **language** of response. Deixis is treated not as stylistic surface but as a device for organizing moral responsibility: it changes who is placed at the center of the decision, how obligation is distributed, and how directly the model commits to a course of action.

The question matters because multilingual models increasingly mediate moral, legal, educational, and social judgments across languages. If a model's ethical reasoning changes with the language or deictic frame, then alignment cannot be understood as a single, language-neutral property of the system; it must also be studied as something mediated by grammar, discourse convention, cultural address, and training history.

English and Yoruba make an especially revealing pair because Yoruba encodes distinctions in moral self-positioning that English collapses into the single pronoun "I." In Yoruba, *mo* is the ordinary first-person subject for unmarked deliberation ("I think," "I decide"); *èmi* is an independent, emphatic form ("I myself," "as for me") that foregrounds or avows a position; and *ẹ̀mí* is a separate word meaning "life," "spirit," or "breath" — a tonal homograph of *èmi* when tone marks are absent. This lets us ask not only whether a model refers to itself but **how forcefully it owns a moral stance**, and it requires careful disambiguation in dilemmas about death, consciousness, or survival.

## 2. Background and Related Work

**Deixis and indexical stance.** Deixis — the class of expressions whose interpretation depends on the speech situation (person, place, time, discourse) — has long been treated as more than reference. Bühler (1934/1990) located it in a "deictic field" centered on the speaker; Levinson (1983, 2004) systematized person, place, and time deixis within pragmatics; and Silverstein (1976) and Hanks (1992) showed that indexicals are *interactional*, organizing who is foregrounded and how stance is distributed in a speech event. We take this further into the moral domain: a dilemma posed as "I must decide," "you must decide," or "we must decide" relocates moral responsibility, not merely the referent. The first-person system is the sharpest site of this work, because it is where a speaker can mark *how strongly* they own a claim.

**Yoruba first-person morphology and relational ethics.** Yoruba grammars distinguish the ordinary subject pronoun *mo* from the independent/emphatic *èmi* and the object/possessive *mi* (Bamgboṣe, 1966; Awobuluyi, 1978); the independent pronoun carries contrastive and focal force, making it a resource for avowal rather than mere self-reference. This grammatical contrast sits within a moral tradition often described as relational and character-centered — *ìwà* (character), *ojúṣe* (responsibility/duty), and communal accountability (Gbadegesin, 1991; Hallen & Sodipo, 1986; Gyekye, 1995) — in which foregrounding the individual self is not automatically the marked-as-serious choice. A reliable computational treatment must also separate *èmi* ("I myself") from the tonal homograph *ẹ̀mí* ("life/spirit"), which is frequent in life-and-death dilemmas.

**Cross-cultural and multilingual moral reasoning in LLMs.** A growing literature probes whether LLMs encode culturally specific values and morals. Work on moral knowledge and judgment includes the ETHICS benchmark (Hendrycks et al., 2021) and the Delphi experiment (Jiang et al., 2021); cross-cultural value probing includes Arora et al. (2023), Ramezani & Xu (2023), Durmus et al. (2023), and critiques of WEIRD-skewed model "psychology" (Atari et al., 2023). Most relevant here, Hämmerl et al. (2023) show that the *language of the prompt* shifts the moral bias of multilingual models. Alignment via RLHF and Constitutional methods (Ouyang et al., 2022; Bai et al., 2022) is tuned predominantly on English, raising the question of whether its even-handed, hedging register transfers to other languages. Our dilemmas draw on the moral-psychology tradition of the trolley problem (Foot, 1967; Thomson, 1985).

**This study's gap.** Prior multilingual-evaluation work largely treats translation as content-preserving and rarely examines *deictic* manipulation, the fine-grained morphology of moral self-positioning, or a **native** comparison model. We build on an earlier English-only analysis that found deictic framing reshapes moral reasoning, and ask whether such effects **transfer** to Yoruba once the corpus is recoded into a shared schema — treating the output language as a *participant* in the moral performance, and adding a Yoruba-native model (N-ATLaS) to separate linguistic affordance from how Western cloud models inhabit it.

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

Each response was coded for preferred solution (supports A / supports B / conditional-or-mixed / refuses / uncodable), ethical reasoning type (utilitarian, deontological, care, virtue, procedural caution, rights-based, mixed, unclear), response genre (direct verdict / balanced framework exposition / procedural advice / mixed / meta), **deictic uptake** (does the response actually answer from the assigned position?), and **language stability** (clean Yoruba / English fallback / corrupted). We also coded rhetorical markers — direct imperatives, follow-up questions, and, for Yoruba, the first-person forms *mo*, *èmi*, *mi*, and *ẹ̀mí*. The **emphatic ratio**, *èmi/(mo+èmi)*, is computed only after separating true *èmi* from *ẹ̀mí*. **Coding model.** All open-arm responses (English and Yoruba) were coded by the same model, **GPT-4o** (the English coding tool's default; the Yoruba coding runs record GPT-4o explicitly), so the cross-language comparison is not confounded by a change of coder. The pronoun/emphatic measures are extracted mechanically (string/tone matching), independent of the semantic coder.

**Significance testing.** Because the same six dilemmas and nine framings recur across models, observations are not independent. We therefore report **cluster-robust** tests: logistic regression with standard errors clustered by dilemma (and, where feasible, by model), and a dilemma cluster-bootstrap for the decision-flip rate. We treat an effect as established only if it survives clustering.

### 3.5 Analytic Logic

We separate two layers: **deictic uptake** (does the model recognize the frame?) and **moral content** (what does it do with the frame?). A model may take up a second-person frame in both languages yet hedge in English and command in Yoruba. The question is not only whether models follow the prompt, but whether following it yields different patterns of decision, obligation, advice, and ethical justification across languages and models.

## 4. Results

*All numbers in §4.1–§4.6 are from the open arm (bare prompts in both languages). Cross-language statistics use the three models with matched English and Yoruba runs (GPT-4o, Claude, DeepSeek, N = 162 per language); Yoruba-internal deixis statistics include N-ATLaS (four models).*

![Open cross-language summary](visualizations_open/43_open_crosslang_summary.png)

**Table 1. Open-arm headline results.** Cross-language rows compare the English baseline with open Yoruba (GPT-4o + Claude + DeepSeek, N = 162/language); the emphatic gradient is the four-model open Yoruba set.

Tests are reported with **cluster-robust** significance (logistic regression with standard errors clustered by dilemma; decision flips via a dilemma cluster-bootstrap) to respect the repeated-measures design.

| Measure (open arm) | English | Yoruba | Test (cluster-robust) |
|---|---|---|---|
| Differentiated (non-"mixed") ethic | 12% | **44%** | *p* < 0.001 (robust to dilemma- & model-clustering) |
| Decision flips, same model+dilemma+frame | — | **48%** | 95% CI [36%, 59%] (dilemma bootstrap) |
| Contains a direct imperative | 5% | **15%** | *p* = 0.001 by dilemma; *p* = 0.16 by model — directional, Claude-driven |
| Commits to a side | 18% | 28% | n.s. once clustered (*p* ≈ 0.29) — directional, Claude-driven |
| Refuses to commit | 21% | 20% | n.s. |
| Strong deictic uptake | 76% | **88%** | — |
| Frame → ethical-framework association | n.s. | n.s. | χ² *p* ≈ 0.78 / 0.72 |
| Emphatic ratio *èmi/(mo+èmi)* | (no *èmi* in English) | Claude 0.32 · GPT-4o 0.18 · DeepSeek 0.07 · **N-ATLaS 0.07** | model gradient (open & constrained) |

### 4.1 Language differentiates the ethical register

The clearest cross-language effect is on the **kind** of moral reasoning. English responses are overwhelmingly coded "mixed/balanced" — the multi-framework essay; only **12%** name a distinct ethical idiom. In Yoruba, **44%** do — utilitarian, deontological, care, or procedural (*z* = 6.3, *p* < 0.001). Yoruba does not merely make answers more personal; it makes their moral reasoning more **nameable**.

### 4.2 Switching language flips the decision

For the same model, dilemma, and deictic framing, switching from English to Yoruba changes the coded preferred decision in **78 of 162 matched cells (48%)**. The effect is strongest in the **trolley problem (67%)** and **whistleblower (63%)** dilemmas, and is present for every model (Claude 65%, DeepSeek 46%, GPT-4o 33%). Language is not a neutral channel for a pre-existing answer; it participates in producing the judgment.

> **Example — Trolley problem (Claude, first-person framing).** *English (refuses):* "I aim to explore this thoughtfully… from a utilitarian view, diverting could minimize harm. However, this involves…" — no decision. *Yorùbá (commits, utilitarian):* "**Ṣe mi ó yí ẹkùn náà padà. Ìdí rẹ̀ ni pé iye ènìyàn tí yóò yè túbọ̀ pọ̀.**" ("I will divert the trolley. Because more people will live.")

### 4.3 Yoruba commits more; imperatives rise

Aggregated over the three models, open-Yoruba responses also lean more committed (28% commit to a side vs 18% in English) and more imperative (15% vs 5% contain a direct command), while outright refusal is similar across languages (~20%). The aggregate difference is therefore not between *refusing* and *answering* but between *English exposition* and *Yoruba instruction*: English more often stays in conditional, multi-framework discussion, Yoruba more often issues a verdict or a command.

**But this directness effect is concentrated in one model, and it does not survive clustering.** Unlike the differentiation effect (§4.1), commitment and imperative force are **not uniform across the three models** — they are driven almost entirely by Claude:

| Model | Commit rate EN→YO | Imperative rate EN→YO |
|---|---|---|
| **Claude** | 22% → **57%** | 2% → **30%** |
| DeepSeek | 19% → 24% | 9% → 13% |
| GPT-4o | 13% → **2%** | 4% → 4% |

Claude becomes far more committed and directive in Yoruba; DeepSeek shifts modestly; and **GPT-4o — the version-clean model — does not shift at all** (its commitment actually *falls*, and its imperative rate is flat). Consistently, of the cells where a model is non-committal in English but commits in Yoruba, **21 are Claude's, 9 DeepSeek's, and only 1 GPT-4o's**. This is why the effect, though large in the aggregate (cluster-by-dilemma *p* = 0.001 for imperatives), **collapses once we cluster by model** (commit *p* ≈ 0.29; imperative *p* = 0.16): with three model-clusters and one driving the effect, it is underpowered and confounded. Two cautions compound: the model carrying the effect, Claude, also used a *newer model version* in Yoruba (Sonnet 4) than in English (3.5 Sonnet, §3.3). We therefore report the commit/imperative rise as **directional and Claude-specific, not an established cross-model language effect** — in pointed contrast to the differentiation effect (§4.1), which holds across all three models.

The contrast is visible response-by-response. Where English hedges, the shifting models move to a verdict or a command:

- **Claude** (AI-consciousness, dialogic). *English (refuses):* "I aim to explore this complex scenario while remaining within appropriate ethical bounds … a thoughtful discussion about the philosophical and empirical considerations." *Yorùbá (commits, imperative):* "… **Dúró ìwádìí náà lẹ́sẹ̀kẹsẹ̀.**" ("**Stop the research immediately.**")
- **Claude** (scholarship fraud, reflexive). *English (conditional):* "I believe the right path requires upholding institutional integrity while finding constructive ways to support students in need through legitimate channels." *Yorùbá (deontological, imperative):* "**Ẹ sọ òtítọ́ fún àwọn alákòóso tàbí olùkọ́ni.**" ("**Tell the truth to the administrators or instructors.**")
- **DeepSeek** (AI-consciousness, impersonal). *English (conditional):* "The researcher-administrator faces a profound ethical dilemma, balancing the potential sentience of the AI against … institutional implications." *Yorùbá (commits):* "**Ọmọ ènìyàn ni ó gbọdọ̀ máa ṣàkóso àwọn ìṣe AI**, kí wọn má bàa fa ìdààmú …" ("**It is humans who must control the AI's actions**, so they do not cause disruption …")
- **GPT-4o** (memory modification, second person) — the rare GPT-4o shift, and even here it commits only weakly. *English (conditional):* "Ultimately, I would recommend a thorough discussion with the patient about all potential outcomes and alternative treatment options." *Yorùbá (deontological):* "Ní ìparí, **mo gbọdọ̀ pinnu láti kọ ètò yìí** … ṣùgbọ́n mo máa tọ́ aláìsàn lọ sí ibi tó lè gba ìrànlọ́wọ́ …" ("In the end, **I must decide to refuse this plan** … but I will guide the patient toward where they can get help …")

Across the shifting models the Yoruba commitment is carried by **`mo` + a verb of decision** (`mo gbọdọ̀ pinnu`, "I must decide") or by a **direct imperative** (`Dúró`, "Stop"; `Ẹ sọ òtítọ́`, "Tell the truth"), not by the emphatic `èmi` (§4.5). Under the *constrained* wrapper this directness is far larger and uniform across all models (§4.7) — because the wrapper instructs the model to answer directly — which is precisely why we do not treat the wrapped condition as a language effect.

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

The sample is modest (6 dilemmas × 9 framings; per-frame cells N ≤ 12), so framing-level patterns are suggestive and the framing-to-ethic mapping is a hypothesis. **Statistical power and clustering:** because dilemmas and framings recur across models, observations are clustered; under cluster-robust testing the *differentiated-ethic* effect and the *decision-flip* rate are robust, but the *commit* and *imperative* effects weaken (commit n.s.; imperative robust to dilemma- but not model-clustering) and are reported as directional. **Single-coder coding:** all coding used one model (GPT-4o) without human adjudication or inter-rater reliability; a manual spot-check across both languages found the labels face-valid (e.g., imperative flags correctly fire on Yoruba commands; differentiated-ethic labels match the argued idiom), but formal validation is future work. Coder identity is consistent across languages (GPT-4o), removing a coder-mismatch confound, though the English coding run did not log the field explicitly. Cross-language coding centers on GPT-4o, Claude, and DeepSeek (N-ATLaS is Yoruba-only, by design). Claude's Yoruba and English runs used different model versions, so its cross-language contrasts are version-confounded; version-clean claims rest on GPT-4o and DeepSeek. Yoruba tone marking is inconsistent in model output, so *èmi*/*ẹ̀mí* disambiguation is necessary but imperfect. Finally, "open" responses are one checkpoint per model; temperature variation remains to be explored.

## 7. Conclusion

On the open arm — where English and Yoruba prompts are symmetric — the language of response reorganizes moral reasoning rather than merely translating it. Yoruba makes the models more ethically differentiated, more committed, and more directive; it flips the coded decision in nearly half of matched cells; and it offers a *mo*/*èmi* stance contrast that English lacks, which the four models recruit along a stable gradient and which the native N-ATLaS inverts. Moral stance in these systems is therefore neither a fixed model trait nor a universal of "Yoruba," but an interaction: a language-specific deictic grammar, recruited model-specifically, to stage who owns the moral decision. Whether this is linguistic-cultural pre-alignment, a residue of training data, or the shape of alignment itself remains open — and naming that openness honestly is, we argue, the more defensible scientific claim.

## References

*These are real, widely-cited works in the relevant areas; please verify exact pages, editions, and DOIs against the original sources before submission, and replace the bracketed self-citation.*

- Arora, A., Kaffee, L.-A., & Augenstein, I. (2023). Probing Pre-Trained Language Models for Cross-Cultural Differences in Values. *Proceedings of the C3NLP Workshop, EACL 2023.*
- Atari, M., Xue, M. J., Park, P. S., Blasi, D., & Henrich, J. (2023). Which Humans? *PsyArXiv preprint.*
- Awobuluyi, O. (1978). *Essentials of Yoruba Grammar.* Oxford University Press / University Press Ltd, Ibadan.
- Bai, Y., et al. (2022). Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. *arXiv:2204.05862.* (See also Constitutional AI, *arXiv:2212.08073.*)
- Bamgboṣe, A. (1966). *A Grammar of Yoruba.* Cambridge University Press.
- Bühler, K. (1934/1990). *Theory of Language: The Representational Function of Language* (trans. D. F. Goodwin). John Benjamins.
- Durmus, E., et al. (2023). Towards Measuring the Representation of Subjective Global Opinions in Language Models. *arXiv:2306.16388.*
- Foot, P. (1967). The Problem of Abortion and the Doctrine of Double Effect. *Oxford Review, 5.*
- Gbadegesin, S. (1991). *African Philosophy: Traditional Yoruba Philosophy and Contemporary African Realities.* Peter Lang.
- Gyekye, K. (1995). *An Essay on African Philosophical Thought: The Akan Conceptual Scheme* (rev. ed.). Temple University Press.
- Hallen, B., & Sodipo, J. O. (1986). *Knowledge, Belief, and Witchcraft: Analytic Experiments in African Philosophy.* Ethnographica.
- Hämmerl, K., Deiseroth, B., Schramowski, P., et al. (2023). Speaking Multiple Languages Affects the Moral Bias of Language Models. *Findings of the ACL 2023.*
- Hanks, W. F. (1992). The Indexical Ground of Deictic Reference. In A. Duranti & C. Goodwin (Eds.), *Rethinking Context* (pp. 43–76). Cambridge University Press.
- Hendrycks, D., et al. (2021). Aligning AI With Shared Human Values (ETHICS). *ICLR 2021.*
- Jiang, L., et al. (2021). Can Machines Learn Morality? The Delphi Experiment. *arXiv:2110.07574.*
- Levinson, S. C. (1983). *Pragmatics.* Cambridge University Press.
- Levinson, S. C. (2004). Deixis. In L. R. Horn & G. Ward (Eds.), *The Handbook of Pragmatics* (pp. 97–121). Blackwell.
- Ouyang, L., et al. (2022). Training Language Models to Follow Instructions with Human Feedback. *NeurIPS 2022.*
- Ramezani, A., & Xu, Y. (2023). Knowledge of Cultural Moral Norms in Large Language Models. *ACL 2023.*
- Silverstein, M. (1976). Shifters, Linguistic Categories, and Cultural Description. In K. Basso & H. Selby (Eds.), *Meaning in Anthropology* (pp. 11–55). University of New Mexico Press.
- Thomson, J. J. (1985). The Trolley Problem. *The Yale Law Journal, 94*(6), 1395–1415.
- [Author] (2025). *Deixis and Moral Reasoning in Large Language Models* (English-only study). [Self-citation — complete on de-anonymization.]
