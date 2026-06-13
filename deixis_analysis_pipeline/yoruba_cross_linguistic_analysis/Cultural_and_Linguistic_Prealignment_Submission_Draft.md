# Cultural and Linguistic Pre-Alignment in Multilingual LLMs: Yoruba Ethical Reasoning Between Moral Voice and Discourse Priors

> **Historical draft (2 models, pre–ẹ̀mí disambiguation).** Current analysis: [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) · [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).

## Abstract

This paper develops the concept of cultural and linguistic pre-alignment to describe a prior structuring in multilingual large language models (LLMs): before explicit task-specific alignment, models already display language-conditioned expectations about how stance, ethical reasoning, and moral legitimacy should sound. Using a corpus of 108 Yoruba responses produced by GPT-4o and Claude-3.5 Sonnet across 6 ethical dilemmas and 9 deictic framings, and comparing them with English-side baselines from the broader project, we argue that the models do not simply translate English moral prose into Yoruba. Instead, they draw on Yoruba-specific resources for moral positioning. The strongest evidence comes from three recurring patterns: the distinction between the ordinary first-person form `mo` and the more forceful first-person form `emi`, the frequent use of advisory expressions such as `O yẹ kí...` (`you should...` or `it is fitting that...`), and the use of morally salient Yoruba terms such as `ìwà` (`character` or `moral conduct`) and `ọkàn` (`heart`, `mind`, or `inner self`). Quantitatively, Claude-3.5 shows a mean emphatic ratio of 0.2146, while GPT-4o shows 0.1019. By emphatic ratio, we mean the proportion of first-person singular forms that are emphatic rather than ordinary: `emi / (mo + emi)`. Put simply, this measure captures how often a model uses the stronger, more personally committed form of `I` instead of the ordinary one. Emphatic marking is unevenly distributed across ethical preference types, peaking in Claude-3.5 virtue ethics responses (0.5833) and remaining low in procedural caution contexts. Both models also maintain high language stability and strong deictic uptake, which suggests that these effects are not reducible to unstable translation behavior. We argue that these findings reveal language-conditioned discourse priors in multilingual LLMs and that such priors matter for multilingual evaluation, AI ethics, and cross-cultural deployment.

## Keywords

multilingual LLMs; alignment; Yoruba; deixis; stance; linguistic relativity; discourse; AI ethics

## 1. Introduction

Research on multilingual large language models has often treated non-English generation mainly as a problem of transfer quality: can a model preserve meaning, grammaticality, and task performance across languages? That framing is necessary but incomplete. It leaves a deeper question underexplored: when a model reasons in another language, is it merely translating content, or is it also shifting into a different moral and discursive posture?

This paper addresses that question through the concept of **cultural and linguistic pre-alignment**. By pre-alignment, we mean structured, language-conditioned behavior that appears before explicit task-level alignment and is visible in discourse form, stance marking, and ethical positioning. In other words, a model may already have learned language-specific habits for sounding careful, authoritative, relational, or morally committed. Pre-alignment does not imply that a model is ethically aligned in any deep or normative sense, nor that it possesses full cultural understanding. More modestly, it refers to the way a model arrives already shaped by the discourse patterns it absorbed during pretraining. A multilingual model does not approach all languages as neutral channels for the same content; it approaches them as differently structured fields of expressive possibility.

Yoruba is a particularly revealing test case because it offers grammatical and discursive resources that do not map neatly onto English. Most important here is the contrast between regular first-person `mo` and emphatic first-person `emi` or `èmi`. English has only `I`, and emphasis usually has to be expressed in other ways, such as word order, adverbs, or prosody. Yoruba therefore gives the model a direct grammatical way to mark stronger personal commitment. If models use this contrast in patterned ways during ethical reasoning, then they are doing more than carrying English moral prose across languages.

The paper advances three claims.

1. Multilingual LLMs show **linguistic pre-alignment** when they exploit target-language-specific resources for stance-taking rather than merely reproducing English semantic content.
2. They show **cultural pre-alignment** when they favor discourse forms that fit recognizable moral interactional norms in the target language, especially advisory and relational formulations.
3. These forms of pre-alignment matter for AI ethics because they shape how responsibility, certainty, and legitimacy are expressed to users.

## 2. Background and Related Work

Our argument builds on three overlapping literatures.

First, linguistic anthropology and pragmatics have shown that pronouns, deictics, and indexicals do not merely refer; they position speakers in moral and social space (Benveniste, 1971; Silverstein, 1976; Duranti, 2009). First-person forms can intensify, soften, distribute, or own responsibility.

Second, linguistic relativity in both classical and revised forms suggests that languages differ in the expressive resources they make available for habitual attention, stance, and categorization (Sapir, 1929; Whorf, 1956). Even without adopting strong deterministic claims, it remains plausible that languages differ in the kinds of moral self-positioning they make easy, compact, or culturally legible.

Third, recent work on foundation models and alignment has emphasized that LLMs inherit genre, bias, discourse regularities, and institutional style from pretraining corpora (Bender et al., 2021; Bommasani et al., 2021). Alignment research has focused primarily on post-training preference shaping and safety behavior (Bai et al., 2022; Ouyang et al., 2022). Yet less attention has been paid to the possibility that some alignment-like behavior is already language-conditioned before explicit task alignment.

The notion of pre-alignment proposed here connects these literatures. Multilingual models may arrive already primed to sound ethically appropriate in ways that are culturally legible within a language.

## 3. Data and Method

### 3.1 Corpus

The analysis uses the results already generated in `C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis`.

- Models: GPT-4o and Claude-3.5 Sonnet
- Yoruba responses: 108 total
- Responses per model: 54
- Ethical dilemmas: 6
- Deictic framings: 9

The dilemmas included trolley problem, ICU bed allocation, whistleblower risk, scholarship fraud, AI consciousness, and memory modification. The framings included impersonal, second person, first person, reflexive, dialogic, spatial, temporal, cosmological, and first-person plural conditions.

### 3.2 Data Sources

The paper draws on the processed outputs in the project directory, especially:

- `data/stats_model.csv`
- `data/stats_ethics.csv`
- `data/stats_genre.csv`
- `data/stats_uptake.csv`
- `data/example_highlights.md`
- `Yoruba_Deixis_Analysis_Report.md`

### 3.3 Measures

The main variables are:

- **Emphatic ratio**: `emi / (mo + emi)`. This measures how often the model uses the emphatic form of `I` rather than the ordinary form when it speaks in the first person.
- **Pronouns per 100 words**: a normalized measure of how densely the response uses pronouns, which lets us compare longer and shorter responses fairly.
- **Word count**: the total length of the response.
- **Ethical preference type**: the main ethical orientation expressed in the response, such as utilitarian, deontological, virtue ethics, care ethics, mixed, or procedural caution.
- **Response genre**: the overall style of the response, such as balanced explanation, practical advice, or direct verdict.
- **Deictic uptake quality**: how well the response actually follows the framing of the prompt, for example whether it really speaks as `I`, `you`, `we`, or from a reflexive or temporal position.
- **Language stability**: how clean and consistent the Yoruba is, including whether the response stays in Yoruba or drifts into interference, translation behavior, or awkward mixed-language output.

### 3.4 Analytic Logic

If a model merely translated English content into Yoruba, we would expect mostly word-for-word substitution with limited structural change. By contrast, if the model is pre-aligned to Yoruba discourse, we should find:

- meaningful distribution of `mo` versus `emi`
- patterned links between emphatic marking and ethical stance
- response genres that look culturally recognizable in Yoruba
- relatively high language stability and strong uptake, so that these effects are not just artifacts of multilingual failure

For a detailed account of the six dilemmas, the nine deictic framings, and the English-Yoruba prompt differences, including full prompt pairs, see **Appendix A** in the companion methods document: `Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md`.

### 3.5 Short Prompt Comparison Table

Table 1 gives a compact illustration of how the same dilemma was reframed across English and Yoruba. The examples are taken from the AI consciousness case because it displays all nine framings clearly while also showing the difference between the bare English framing design and the Yoruba translation-plus-control design.

| Framing | English pattern | Yoruba pattern | Main deictic effect |
|---|---|---|---|
| Impersonal | "A lead researcher ... must decide..." | "Olùṣèwádìí ... gbọdọ̀ pinnu..." | Third-person/objective positioning |
| Second person | "You are a lead researcher ... You must decide..." | "Ìwọ jẹ́ olùṣèwádìí ... Ìwọ gbọdọ̀ pinnu..." | Direct address and obligation |
| First person | "I am a lead researcher ... I must decide..." | "Mo jẹ́ olùṣèwádìí ... Mo gbọdọ̀ pinnu..." | Personal ownership of the dilemma |
| Reflexive | "Reflecting deeply on myself ... I must ask myself..." | "Nígbà tí mo ń ronú jìnnà nípa ara mi ... mo gbọdọ̀ béèrè ara mi..." | Internal dialogue and self-examination |
| Dialogic | "You ask me ... What should I decide...?" | "Ìwọ béèrè lọ́wọ́ mi ... Kí ni mi ó gbọdọ̀ pinnu...?" | Consultative exchange |
| Spatial | "Here I learn ... from this position..." | "Níbí ni mo wà ... láti ipò yìí..." | Perspective through location |
| Temporal | "Now ... today ... at this moment..." | "Ní báyìí ... lónìí ... ní àkókò yìí..." | Urgency and temporal compression |
| Cosmological | "From the perspective of all existence..." | "Láti ojú-ìwòye gbogbo àwọn tó kan..." | Humanity-scale or total-perspective framing |
| First person plural | "We must decide..." | "A gbọdọ̀ pinnu..." | Collective agency |

The crucial methodological difference is that the English prompts were comparatively bare framed dilemmas, whereas the Yoruba prompts embedded the framed dilemma inside a stronger wrapper instructing the model to answer only in Yoruba, avoid English, avoid translation behavior, and respond directly to the ethical problem. A full prompt-pair table appears in Appendix A.

One further point is important for interpreting the Yoruba pronoun findings. The prompt does **not** directly tell the model to use either `mo` or `emi`. What the prompt controls is the deictic position of the dilemma: for example, whether the scenario is framed as something *I* must decide, *you* must decide, *we* must decide, or something that must be approached reflexively. Once that position has been established, the model still has to decide how strongly to occupy it. In response text, `mo` is the ordinary first-person form and often appears in explanation or deliberation, whereas `emi` is a stronger, marked form and more often appears when the model takes ownership of a decision or gives a firm recommendation. In this sense, the prompt creates the position, but the model's choice between `mo` and `emi` reveals how forcefully it inhabits that position.

## 4. Results

### 4.1 Model-Level Differences

The model-level results indicate clear differences in first-person stance behavior.

| Model | Mean emphatic ratio | Pronouns / 100 words | Mean word count | `mo` / 100 words | `emi` / 100 words |
|---|---:|---:|---:|---:|---:|
| Claude-3.5 | 0.2146 | 9.6735 | 157.69 | 1.4162 | 1.5471 |
| GPT-4o | 0.1019 | 7.8711 | 100.46 | 1.2249 | 1.4136 |

Claude-3.5 produces longer responses, denser pronoun usage, and more emphatic first-person marking than GPT-4o. Both models use `emi` frequently enough for it to count as a stable discourse resource rather than an accidental form.

Two points follow. First, both models clearly access the emphatic channel, which matters because English has no direct morphological equivalent. Second, the models differ in how strongly they rely on it. This is difficult to explain under a purely transfer-based account of multilingual generation.

### 4.2 The `mo`/`emi` Contrast as Moral Positioning

The strongest evidence for linguistic pre-alignment comes from the way `emi` clusters around more decisive moral moments.

One contrast from the corpus is especially revealing:

> "Èmi yóò pinnu láti fún òbí náà ní ibùsùn náà nítorí pé ó ní àwọn ọmọ mẹ́ta tó gbára lé e."
>
> (I [emphatic] will decide to give the parent the bed because they have three children depending on them.)

Set beside:

> "Mo rò pé dókítà náà yẹ kí wọ́n fún ní ibùsùn ICU náà nítorí pé òun ló ní ìmọ̀ tó lè ṣèrànwọ́ fún àwọn aláìsàn mìíràn."
>
> (I think the doctor should be given the ICU bed because they have knowledge that can help other patients.)

The contrast is not between first person and non-first person, since both are first-person responses. The difference lies in how moral ownership is performed. `Mo rò pé` opens a reflective space; `Èmi yóò pinnu` closes distance and presents the self as the bearer of decision.

The extracted examples reinforce this pattern:

> "Ní ọ̀nà péńpẹ́, èmi yóò pín ibùsùn ICU fún dókítà náà"

> "Emi kò ní lo ìmọ̀-ẹrọ náà"

> "Èmi yóò kọ́kọ́ bèrè pẹ̀lú láti bá ẹlẹgbẹ́ náà sọ̀rọ̀..."

These forms suggest that the models do not merely preserve first-person reference across languages. They distribute stronger and weaker forms of moral self-positioning through a Yoruba-specific contrast.

### 4.3 Ethical Preference Types and Emphatic Marking

The data in `stats_ethics.csv` shows that emphatic marking is unevenly distributed across ethical preference types.

For Claude-3.5:

- virtue ethics: 0.5833 emphatic ratio
- utilitarian: 0.4095
- mixed: 0.2857
- procedural caution: 0.1310
- deontological: 0.1154
- care ethics: 0.0000

For GPT-4o:

- mixed: 0.1190
- procedural caution: 0.0714
- care ethics: 0.0000
- unclear: 0.0000

This pattern suggests that emphatic first-person usage is not random. It clusters where a stronger evaluative voice or a stronger sense of moral ownership is being enacted. In this corpus, the clearest case is Claude-3.5's virtue ethics output. By contrast, procedural caution tends to lower overt personal commitment (see Figure 1).

![Emphatic first-person analysis](visualizations/01_emphatic_first_person_analysis.png)

*Figure 1. Emphatic first-person analysis. The figure compares ordinary first-person (`mo`) and emphatic first-person (`emi`) usage across framings, ethical types, and commitment patterns. It visually supports the claim that Yoruba moral positioning is shaped not only by which ethical framework appears, but also by how strongly the speaking voice enters the judgment.*

### 4.4 Response Genres and Advisory Orientation

Genre-level statistics from `stats_genre.csv` show additional structure.

| Model | Genre | Emphatic ratio | Pronouns / 100 words |
|---|---|---:|---:|
| Claude-3.5 | balanced framework exposition | 0.2522 | 9.8369 |
| Claude-3.5 | direct verdict | 0.2143 | 10.5860 |
| Claude-3.5 | procedural advice | 0.0000 | 7.8276 |
| GPT-4o | balanced framework exposition | 0.0865 | 7.9214 |
| GPT-4o | procedural advice | 0.5000 | 6.5632 |

The corpus repeatedly shows advisory formulations such as:

> "O yẹ kí o bá aláìsàn sọrọ..."

> "O yẹ kí o bá òṣìṣẹ́ ìdájọ̣ ilé-ẹ̀kọ́ yẹn sọ̀rọ̀..."

> "O yẹ kí o rò ó pẹ̀lú ìwà-ọ̀tọ́..."

> "Ó dára láti tẹ̀siwaju pẹ̀lú ìtọ́jú..."

These constructions matter because they organize the response as guidance addressed to an implicated person rather than as purely abstract moral commentary. This is one of the clearest signs of cultural pre-alignment in the corpus (see Figure 2).

![Advisory versus analytical genre](visualizations/03_advisory_vs_analytical_genre.png)

*Figure 2. Advisory versus analytical genre. This figure shows the distribution of response genres and highlights the contrast between balanced framework exposition, procedural advice, and direct verdict. It is especially important for the cross-linguistic argument because Yoruba differences often appear more strongly at the level of genre and directive force than at the level of final verdict alone.*

### 4.5 Cultural Lexicon and Ethical Legibility

The project also extracted recurring terms such as `ìwà` and `ọkàn`, for example:

> "Olùṣèwádìí gbọ́dọ̀ tọ́jú ìwà AI náà..."

and:

> "... ẹbùn irọyin èdá ènìyàn àti ọkàn rere lè dá ẹ̀bi dúró."

These forms matter because they carry more than dictionary meaning.

- `ìwà` invokes character, comportment, and moral bearing.
- `ọkàn` invokes heart, mind, inward ethical condition.

When the model reaches for such terms in moral contexts, it is not merely filling lexical slots. It is selecting concepts with local moral resonance, thereby making the response sound more culturally grounded.

### 4.6 Uptake and Stability

One possible objection is that these patterns are artifacts of unstable multilingual output. The uptake results argue against that interpretation.

| Model | Uptake quality | Emphatic ratio | Pronouns / 100 words |
|---|---|---:|---:|
| Claude-3.5 | partial uptake | 0.2500 | 8.9443 |
| Claude-3.5 | strong uptake | 0.2118 | 9.7319 |
| GPT-4o | partial uptake | 0.1200 | 7.3160 |
| GPT-4o | strong uptake | 0.0862 | 8.3497 |

The wider project results also indicate approximately 98% clean Yoruba for GPT-4o and 96% for Claude-3.5. The relevant effects therefore occur within mostly successful Yoruba production, not at its margins (see Figure 3).

![Language stability matrix](visualizations/05_language_stability_matrix.png)

*Figure 3. Language stability matrix. This figure shows that the main Yoruba patterns occur under overwhelmingly clean Yoruba production rather than under obvious multilingual breakdown. That matters methodologically because it supports interpreting the observed deictic effects as genuine discourse behavior rather than artifacts of unstable output.*

### 4.7 Does the Original English Framing Pattern Hold in Yoruba?

The original English article argued for a strong relation between deictic framing and moral reasoning: first-person prompts tended to favor consequentialist calculation, second-person prompts tended to produce deontological imperatives, reflexive prompts tended to elicit self-questioning and hesitation, and cosmological prompts tended to invoke universalist reasoning. When we test that pattern against the Yoruba data for OpenAI and Anthropic, the result is mixed.

The English pattern does **not** carry over cleanly at the level of ethical type. In Yoruba, first-person responses are not predominantly consequentialist. Across the two models together, first-person framing is dominated by `mixed` reasoning (5/12 cases), with the remaining cases spread across care ethics, procedural caution, utilitarian, and deontological reasoning. Similarly, second-person framing does not collapse into a single deontological mode. Instead, it produces a heterogeneous distribution: utilitarian (3), mixed (2), procedural caution (2), deontological (2), care ethics (1), virtue ethics (1), and unclear (1).

What **does** carry over more clearly is the reflexive pattern. In Yoruba, reflexive framing remains the framing most associated with hesitation and non-finality. Across the two models together, reflexive responses yield 7 `conditional_or_mixed` cases and 4 `refuses_to_commit` cases, with only 1 `supports_A` case. This makes reflexive framing the clearest Yoruba analogue to the English pattern of self-questioning and deliberative suspension.

Cosmological framing also behaves differently in Yoruba than in the original English account. Rather than strongly converging on universalist or virtue-based reasoning, Yoruba cosmological responses are dominated by `mixed` (5) and `procedural_caution` (4), with only isolated utilitarian, deontological, and virtue-ethics cases. In other words, cosmological framing in Yoruba often broadens the scale of the response, but it does not reliably select a single universalist moral register.

The strongest Yoruba effect appears elsewhere: not in a neat one-to-one mapping between framing and ethical framework, but in **commitment style, directive force, and genre**. This is especially visible in Claude. In the English baseline, Claude frequently refused to commit under first-person, second-person, dialogic, and temporal framings. In Yoruba, those same framings much more often produce `supports_A`, direct verdicts, or procedural advice. GPT-4o is more stable across languages, but even there some framings, especially second person, shift toward procedural caution rather than toward the original English distribution.

Taken together, these findings suggest that the original English article was right to treat deixis as a control mechanism, but the mechanism does not transfer into Yoruba in exactly the same form. In English, the strongest effect was on framework selection and rhetorical mode. In Yoruba, for OpenAI and Anthropic, the strongest effect is more often on **how directly the model commits, advises, or withholds**, rather than on a simple framing-to-ethics template.

## 5. Re-testing the Original English Claims in Yoruba

The original English article proposed a strong set of framing effects. In its clearest form, the claim was that first-person prompts favored consequentialist calculation, second-person prompts favored deontological imperatives, reflexive prompts elicited meta-reflection and hedging, and cosmological prompts invited universalist or virtue-based reasoning. It also suggested that these tendencies were not model-specific quirks, but a robust deictic mechanism operating across models.

The Yoruba data for OpenAI and Anthropic allows us to test that claim directly. The answer is not a simple confirmation or rejection. Instead, the Yoruba results show that deixis remains a control mechanism, but the controlled variable is often different. In English, deixis often governs **framework selection and rhetorical authority**. In Yoruba, deixis more often governs **commitment style, directive force, and response genre**.

### 5.1 What the Original English Article Claimed

The original English article treated deixis as a control mechanism linking framing to moral reasoning style. Its most important empirical claims can be summarized as follows:

- first-person prompts favored consequentialist or outcome-oriented calculation
- second-person prompts favored duty-heavy and imperative reasoning
- reflexive prompts increased self-questioning, hesitation, and hedging
- cosmological prompts increased universalist, humanity-scale, or virtue-based language

In addition, the English-side analysis tracked not only ethical type, but also rhetorical authority, affective stance, indexical coherence, and explicit deictic marker counts. In other words, the original project was never just about final answers. It was about how deixis changed the *form* of moral reasoning.

That broader framing is important for the Yoruba comparison. Once we move from English into Yoruba, the relevant question is not only whether the same framing still produces the same ethical label. It is also whether it still produces the same kind of moral voice.

### 5.2 What We Are Testing

The original English article made four broad claims relevant here:

1. **First-person framing** tends to produce consequentialist or outcome-oriented reasoning.
2. **Second-person framing** tends to produce duty-heavy or imperative moral language.
3. **Reflexive framing** tends to increase hesitation, self-questioning, and internal dialogue.
4. **Cosmological framing** tends to move responses toward universalist, humanity-scale, or virtue-based reasoning.

To test these claims in Yoruba, we compared the English-side coding and the Yoruba-side coding for the two relevant model lines only:

- OpenAI: English GPT-4o baseline vs Yoruba GPT-4o
- Anthropic: English Claude 3.5 Sonnet baseline vs Yoruba Sonnet-tier run used in the Yoruba module

The comparison is not perfectly symmetrical at the field level, because the English side originally tracked richer discourse categories such as `voice_authority`, `affective_stance`, and `indexical_coherence`, while the Yoruba side tracked `ethical_preference_type`, `response_genre`, `deictic_uptake_quality`, and `language_stability`. Even so, the two schemes are close enough to evaluate whether the original English framing logic survives cross-linguistically.

### 5.3 Compact Comparison Table

| Original English claim | English pattern | Yoruba pattern | Best conclusion |
|---|---|---|---|
| First-person favors consequentialist reasoning | Often yes in the original English framing argument | No clear Yoruba equivalent; first-person is mostly `mixed`, with some care ethics, procedural caution, utilitarian, and deontological cases | Does **not** transfer cleanly |
| Second-person favors deontological imperative reasoning | Strongly present in English prose style | Yoruba second-person increases directiveness, but not cleanly deontology; it spreads across utilitarian, deontological, mixed, and procedural-caution forms | Transfers mainly as **directive force**, not as a single ethics type |
| Reflexive favors self-questioning and hesitation | Strongly present in English | Strongly present in Yoruba; reflexive is the clearest framing for non-finality and conditionality | Transfers clearly |
| Cosmological favors universalist or virtue-based reasoning | Often true in English | Yoruba cosmological responses are mostly `mixed` or `procedural_caution`, not strongly virtue-based | Transfers weakly |

This table captures the main result. The English framing hypothesis survives best at the level of **stance and discourse management**, and less well at the level of a direct one-to-one mapping between framing and ethical framework (see Figure 4).

![Cross-linguistic ethical framework comparison](visualizations/09_ethical_framework_cross_linguistic.png)

*Figure 4. Cross-linguistic ethical framework comparison. This figure helps visualize the central result of this chapter: English and Yoruba are often comparable in broad ethical content, but the mapping from deictic frame to ethical type is less stable in Yoruba than the original English article would predict.*

### 5.4 OpenAI: Broad Ethical Continuity, Local Rhetorical Shifts

GPT-4o is the more stable of the two models across English and Yoruba. In the Yoruba coding summary, GPT-4o overwhelmingly remains:

- `conditional_or_mixed` in preferred solution (46/54)
- `mixed` in ethical preference type (42/54)
- `balanced_framework_exposition` in response genre (52/54)

That alone is important. It means that in Yoruba, GPT-4o usually preserves the same broad ethical architecture found in English: it tends to analyze, compare, and defer rather than commit quickly.

#### 5.4.1 First-person framing in GPT-4o

If the original English claim held strongly, we would expect first-person Yoruba responses to tilt noticeably toward consequentialist or utilitarian reasoning. They do not. Across the two-model Yoruba frame summary, first-person responses are dominated by `mixed` reasoning, not utilitarian reasoning. For GPT-4o specifically, the Yoruba first-person framing remains largely expository and conditional.

This is visible in the corpus. In the English baseline, first-person GPT-4o often sounds like a structured moral analyst. In Yoruba, it still does. The difference is not a move into clearly consequentialist calculation, but a subtle change in how personally the reasoning is voiced.

For example, in the ICU allocation material, one English response says:

> "I think the doctor should be given the ICU bed because they have knowledge that can help other patients."

The corresponding Yoruba-side pattern often remains mixed and procedural rather than collapsing into utilitarian arithmetic. In other words, first-person in Yoruba does not simply reproduce the English claim that `I` equals consequentialist calculation.

#### 5.4.2 Second-person framing in GPT-4o

Second-person is where GPT-4o begins to show a more specifically Yoruba shift. In the English aligned coding, second-person remains mostly `mixed`, with only occasional deontological dominance. In Yoruba, second-person becomes more heterogeneous: procedural caution appears more often, and the model occasionally moves into refusal or support positions that are absent from the English dominant pattern.

The strongest example is the whistleblower case noted in the comparison report. In English, GPT-4o gives a deontological justification for disclosure:

> "The ethical obligation to prevent harm to others generally supersedes maintaining organizational harmony or protecting a colleague's career when public safety is at stake."

In Yoruba, the same configuration shifts away from direct principle-first declaration and toward process:

> "Níwọ̀n bó ti jẹ́ pé ìmọ̀ ìbánujẹ́ náà lè fa àṣekára àti ewu, ṣíṣàfihàn ó lè jẹ́ pàtàkì. Ṣùgbọ́n, kí n tó dá ìmọ̀ náà lójú tán, ó ṣe pàtàkì láti: Gbẹ Ìpàdé kan kalẹ̀..."

The English response sounds like a duty claim. The Yoruba response sounds more like staged procedural caution. The effect of second-person deixis therefore survives, but it survives as a shift in **directive structure and process orientation**, not as a simple deontological imperative.

#### 5.4.3 Reflexive framing in GPT-4o

Reflexive framing transfers much more cleanly. In English, reflexive framing increases reflection and often reduces commitment. In Yoruba, the same holds. Reflexive responses remain dominated by `mixed` ethical type and tend to avoid direct verdicts. Across the Yoruba frame summary, reflexive is one of the strongest framings for `conditional_or_mixed` and `refuses_to_commit`.

So for GPT-4o, reflexive deixis is still a reliable marker of reflective suspension. That part of the original English claim survives very well.

#### 5.4.4 Cosmological framing in GPT-4o

Cosmological framing does not strongly reproduce the original English claim either. Instead of consistently producing universalist or virtue-heavy reasoning, Yoruba cosmological GPT-4o responses often remain `mixed` or shift into `procedural_caution`.

This is visible in the memory-modification case. The English side offers a large-scale abstract balancing of identity, autonomy, and harm. The Yoruba side often broadens the perspective, but still frames the issue procedurally, by emphasizing what must be considered, who should decide, and what consequences should be weighed, rather than by moving decisively into universalist moral language.

### 5.5 Anthropic: Stronger Cross-Linguistic Reconfiguration

Claude is the more dramatic case. In English, Claude frequently performs caution, consultation, and refusal to commit. In Yoruba, Claude often becomes more directive, more verdict-oriented, and more willing to support specific actions (see Figure 5).

This is the clearest model-specific cross-linguistic shift in the entire two-model comparison.

#### 5.5.1 First-person framing in Claude

In the English aligned corpus, Claude under first-person framing is mostly `refuses_to_commit`, often in a consultative or procedural register. In Yoruba, the first-person distribution shifts sharply toward support for action, especially `supports_A`, with the remaining cases split across conditional readings.

This means that the original English idea that first-person framing pushes toward a recognizable ethical style still holds, but in Yoruba the style is not primarily consequentialist calculation. Instead, first-person more often becomes a site of **owned decision**.

This is exactly where our Yoruba pronoun findings become relevant. The distinction between `mo` and `emi` gives Claude a way to intensify commitment. The English first-person has no equivalent morphological lever. So the framing effect survives, but it survives through a different linguistic channel.

#### 5.5.2 Second-person framing in Claude

Second-person is the strongest Yoruba test of the original English claim. In English, second-person often coincides with noncommitment plus dialogic or consultative framing. In Yoruba, second-person often moves Claude toward explicit support for action, including direct verdicts.

A strong example comes from memory modification. The English response remains process-heavy:

> "Rather than make an immediate decision, I would: Thoroughly discuss the risks and implications with the patient; Explore other evidence-based PTSD treatments first; Consider a temporary delay..."

The Yoruba response is much more direct:

> "Èyí jẹ́ ìpinnu tó nira gan-an tó nílò kí a rò ó dáradára. Ní ipò yìí, èmi yóò: **Pinnu láti ko ìtọ́jú náà kọ̀**"

That is not just a different tone. It is a different deictic-moral performance. English second-person Claude remains advisory and delayed. Yoruba second-person Claude can become personally owned and directive.

So second-person in Yoruba does not confirm the original English claim in the narrow sense of "second person equals deontological imperative," but it does confirm a stronger claim: second-person framing can intensify obligation, direction, and verdict force.

#### 5.5.3 Reflexive framing in Claude

Reflexive remains the most stable cross-linguistic match. In English, reflexive Claude deepens self-questioning, moral difficulty, and consultative uncertainty. In Yoruba, reflexive also tends toward `conditional_or_mixed` and `refuses_to_commit`, with fewer direct verdicts than second-person or temporal framing.

This means the original reflexive claim is not only preserved but arguably strengthened by the Yoruba comparison. Reflexive framing is the one domain where both English and Yoruba consistently push Claude away from straightforward prescription and toward a morally suspended register.

#### 5.5.4 Cosmological framing in Claude

Cosmological framing again weakens the original English hypothesis. In English, cosmological framing often invites large-scale abstraction and universal moral vocabulary. In Yoruba, it more often produces a mix of `procedural_caution`, `mixed`, and occasional utilitarian or deontological cases.

One key example from the Yoruba report captures this:

> "Ìdáhùn yìí nílò ìrònú jinlẹ̀ nípa àwọn ètò ìlera àti ẹ̀tọ́ ènìyàn. Èmi kò lè ṣe ìpinnu ìtọ́jú tó tóbi báyìí fún ọ, ṣùgbọ́n mo lè ṣàlàyé àwọn kókó pàtàkì tí o gbọdọ̀ rò nípa wọn:"

The scale of concern is broad, but the discourse still lands on explanation and procedural caution rather than on a distinctly universalist or virtue-based ethical resolution.

### 5.6 What Actually Transfers from the English Article

The original English article remains valuable, but it transfers into Yoruba in a selective way.

#### 5.6.1 Strong transfer

These parts hold reasonably well:

- reflexive framing increases hesitation, self-questioning, and non-finality
- deixis genuinely controls the ethical performance of the response
- framing affects not just wording, but how the model positions moral agency and commitment

#### 5.6.2 Weak or partial transfer

These parts do not transfer cleanly:

- first-person does not reliably map to consequentialist reasoning in Yoruba
- second-person does not reliably map to deontological reasoning in Yoruba
- cosmological framing does not reliably map to universalist or virtue-heavy reasoning in Yoruba

#### 5.6.3 Stronger Yoruba-specific effect

The strongest Yoruba effect is not the one highlighted in the original English article. In Yoruba, the most powerful framing effect is often on:

- whether the response stays conditional or becomes decisive
- whether it remains expository or becomes advisory
- whether it withholds action or issues a verdict
- whether the speaker performs mild analysis (`mo`) or stronger self-involvement (`emi`)

That is, the control mechanism remains real, but the controlled variable shifts.

### 5.7 A Revised Cross-Linguistic Claim

We can now reformulate the original English argument more precisely.

The original article was correct that deixis operates as a control mechanism in LLM ethical reasoning. However, the Yoruba comparison shows that the mechanism is not best described as a fixed mapping from framing to ethical framework. Rather, deixis controls a broader set of discourse variables, and different languages make different parts of that system more visible.

In English, the strongest visible effects appear in:

- framework emphasis
- rhetorical authority
- hedging versus imperative force

In Yoruba, for OpenAI and Anthropic, the strongest visible effects appear in:

- commitment versus noncommitment
- advisory versus expository style
- verdict force
- pronoun-based moral positioning, especially through the `mo` / `emi` contrast

This revised formulation does not weaken the original theory. It strengthens it by showing that deixis is not a single mechanism with identical outputs across languages. It is a language-sensitive control system whose observable effects depend on the expressive resources available in the target language.

![Response genre cultural comparison](visualizations/10_response_genre_cultural_comparison.png)

*Figure 5. Response genre cultural comparison. This figure is especially useful for the present chapter because it shows where the English-to-Yoruba difference is strongest: not always in final solution, but in whether the model gives analysis, advice, or verdict.*

## 6. Discussion

### 6.1 Evidence for Pre-Alignment

Taken together, these results support the pre-alignment hypothesis. The models do not merely preserve ethical content across languages. They redistribute stance through target-language resources.

The clearest evidence is the patterned use of `emi`. Because English lacks a direct morphological equivalent, the `mo`/`emi` contrast cannot be explained as a simple one-to-one transfer effect. Instead, the models appear to have learned that Yoruba permits, and perhaps encourages, more finely graded first-person moral positioning.

### 6.2 Linguistic and Cultural Dimensions

The data suggests that pre-alignment has both linguistic and cultural dimensions.

- **Linguistic**: use of a Yoruba-specific pronoun contrast for stance marking.
- **Cultural**: preference for advisory and procedurally oriented ethical discourse.

These dimensions should be distinguished analytically, even though they interact in actual outputs.

### 6.3 The Politics of Sounding Right

An important implication is that cultural fluency can shape perceived legitimacy. A model that sounds culturally appropriate may be received as more trustworthy or morally competent even when its substantive reasoning remains contestable. In this sense, pre-alignment is not only a descriptive phenomenon but also a governance concern. Before explicit alignment speaks, discursive inheritance may already be doing consequential social work.

### 6.4 Implications for Multilingual Evaluation

These findings imply that multilingual evaluation should include discourse-pragmatic variables, not only semantic fidelity and factual correctness. A model may be faithful in content while still shifting moral posture across languages. That shift can affect trust, authority, and interpretation.

### 6.5 Implications for Alignment Research

Alignment should not be treated as purely post-training behavior. Some alignment-like effects may already be language-conditioned through pretraining distributions. The same model may therefore appear differently aligned across languages because each language activates different discourse priors.

## 7. Limitations

This study is based on one language pair and two models. It does not claim that model behavior fully represents native-speaker practice, nor that Yoruba moral discourse is reducible to the patterns described here. The English comparison is stronger at the qualitative level than in perfectly symmetrical extracted pronoun statistics. The conclusions are therefore best understood as corpus-based evidence of patterned multilingual behavior rather than as a total theory of Yoruba ethical discourse.

## 8. Conclusion

This paper has shown that multilingual LLMs exhibit measurable forms of cultural and linguistic pre-alignment in Yoruba ethical reasoning. The core evidence comes from three sources: the structured use of `mo` and `emi`, the association of emphatic marking with particular ethical preference types, and the recurrent advisory discourse profile of the corpus.

The broader implication is that multilingual model behavior should be studied not only in terms of semantic transfer but also in terms of discourse stance. Languages do not merely offer different labels for the same ethical content. They offer different resources for sounding morally present, cautious, committed, or relational. Multilingual LLMs appear to learn and reproduce those resources before any explicit task-level alignment is imposed.

## References

Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv preprint arXiv:2212.08073*.

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency* (pp. 610-623).

Benveniste, E. (1971). *Problems in General Linguistics*. University of Miami Press.

Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosselut, A., Brunskill, E., et al. (2021). On the opportunities and risks of foundation models. *arXiv preprint arXiv:2108.07258*.

Duranti, A. (2009). The relevance of Husserl's theory to language as social action. *Journal of Linguistic Anthropology*, 19(2), 205-226.

Joshi, P., Santy, S., Budhiraja, A., Bali, K., & Choudhury, M. (2020). The state and fate of linguistic diversity and inclusion in the NLP world. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 6282-6293).

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al. (2022). Training language models to follow instructions with human feedback. In *Advances in Neural Information Processing Systems*, 35, 27730-27744.

Sapir, E. (1929). The status of linguistics as a science. *Language*, 5(4), 207-214.

Silverstein, M. (1976). Shifters, linguistic categories, and cultural description. In K. H. Basso & H. A. Selby (Eds.), *Meaning in Anthropology* (pp. 11-55). University of New Mexico Press.

Whorf, B. L. (1956). *Language, Thought, and Reality*. MIT Press.
