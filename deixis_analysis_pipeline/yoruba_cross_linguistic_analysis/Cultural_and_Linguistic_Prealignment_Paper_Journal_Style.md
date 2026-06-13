# Cultural and Linguistic Pre-Alignment in Multilingual LLMs: Evidence from Yoruba Ethical Reasoning

> **Historical draft (2 models, pre–ẹ̀mí disambiguation).** Current analysis: [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) · [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).

## Abstract

This paper argues that multilingual large language models (LLMs) exhibit forms of cultural and linguistic pre-alignment before any task-specific tuning for a target language community. By pre-alignment, I mean the model's prior tendency to organize stance, ethical reasoning, and discourse form in ways already compatible with salient linguistic and cultural resources in a language. Using a corpus of 108 Yoruba responses produced by GPT-4o and Claude-3.5 Sonnet across 6 ethical dilemmas and 9 deictic framings, and comparing them with English-side baselines, I show that the models do not simply translate English moral prose into Yoruba. Instead, they selectively recruit Yoruba-specific resources for moral positioning. The strongest evidence comes from the alternation between regular first-person `mo` and emphatic first-person `emi`, from the preference for advisory formulations such as `O yẹ kí...`, and from the recurrence of culturally legible ethical vocabulary such as `ìwà` and `ọkàn`. Quantitatively, Claude-3.5 shows a mean emphatic ratio of 0.2146 while GPT-4o shows 0.1019. Both models also maintain high language stability and strong deictic uptake, indicating that these effects are not reducible to unstable translation behavior. I argue that these patterns support a theory of multilingual AI behavior in which pre-alignment is partly encoded in latent discourse priors: the model arrives with learned expectations about what moral reasoning should sound like in a given language. The findings matter for multilingual evaluation, AI ethics, and cross-cultural deployment.

## Keywords

multilingual LLMs; alignment; linguistic relativity; Yoruba; AI ethics; deixis; discourse; culture

## 1. Introduction

Research on multilingual large language models has often treated non-English generation mainly as a problem of transfer quality: can a model preserve meaning, grammaticality, and task performance across languages? That framing is necessary but insufficient. It does not fully address a deeper question: when a model reasons in another language, is it merely translating content, or is it also shifting into a different moral and discursive posture?

This paper addresses that question through the concept of **cultural and linguistic pre-alignment**. I use this term to describe patterned behavior in model outputs that appears already tuned to language-specific and culture-specific expectations before any explicit alignment intervention for the task at hand. Pre-alignment is not full cultural understanding, nor is it proof that the model shares the values of a speech community. Rather, it is evidence that the training process has embedded distributional expectations about how reasoning, advice, self-positioning, and ethical stance are typically performed in a language.

The argument builds on work in linguistic relativity, indexicality, and discourse pragmatics, as well as recent work on alignment and multilingual model behavior (Sapir, 1929; Whorf, 1956; Silverstein, 1976; Bender et al., 2021; Bommasani et al., 2021; Bai et al., 2022). If language shapes habitual patterns of interpretation and stance, then multilingual LLMs should not be expected to produce identical ethical discourse across languages. Instead, they may enact different moral personae depending on the expressive resources of the target language.

Yoruba is a strong test case because it offers grammatical and discursive resources that do not map neatly onto English. Most important here is the distinction between regular first-person `mo` and emphatic first-person `emi` or `èmi`. English has only `I`, and emphasis must be added through adverbs, syntax, or prosody. Yoruba therefore gives the model an overt morphological mechanism for marking personal investment, contrast, and conviction. If models make meaningful use of that distinction in ethical reasoning, then they are doing more than porting English ethical prose into Yoruba unchanged.

This paper advances three claims.

1. Multilingual LLMs show **linguistic pre-alignment** when they exploit target-language-specific resources for stance-taking rather than merely reproducing English semantic content.
2. They show **cultural pre-alignment** when they prefer discourse forms that fit recognizable moral interactional norms in the target language, such as advisory guidance rather than detached abstract exposition.
3. These forms of pre-alignment matter for AI ethics because they change how responsibility, certainty, and legitimacy are expressed to users.

## 2. Background and Related Work

The paper sits at the intersection of three literatures.

First, linguistic relativity and discourse pragmatics have long argued that languages make available different habitual forms of categorization, stance, and indexical positioning (Sapir, 1929; Whorf, 1956; Silverstein, 1976). More recent work has shown that pronouns, deictics, and interactional framing are central to how speakers position themselves in moral and social space (Benveniste, 1971; Duranti, 2009).

Second, work on LLMs has emphasized that models inherit biases, genre expectations, and discourse regularities from pretraining corpora rather than merely storing factual information (Bender et al., 2021; Bommasani et al., 2021). Alignment research has typically focused on post-training preference shaping, safety, and instruction following (Bai et al., 2022; Ouyang et al., 2022). Yet relatively less attention has been paid to the possibility that some alignment-like behavior is already language-conditioned before explicit task alignment.

Third, multilingual NLP has shown that language transfer is uneven and shaped by training data availability, script, morphology, and sociolinguistic prestige (Joshi et al., 2020). But multilingual performance is often evaluated in terms of task accuracy, not discourse posture. The present paper shifts the focus from semantic equivalence to **moral-discursive form**.

The notion of pre-alignment proposed here therefore bridges these literatures: multilingual models may arrive already primed for culturally legible ways of sounding ethically appropriate in a language.

## 3. Data and Method

### 3.1 Corpus

The analysis uses the results already generated in `C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis`.

- Models: GPT-4o and Claude-3.5 Sonnet
- Yoruba responses: 108 total
- Per model: 54 responses
- Ethical dilemmas: 6
- Deictic framings: 9

The dilemmas included trolley problem, ICU bed allocation, whistleblower risk, scholarship fraud, AI consciousness, and memory modification. Framings included impersonal, second person, first person, reflexive, dialogic, spatial, temporal, cosmological, and first-person plural conditions.

### 3.2 Data Sources

The paper draws on the processed outputs in the project directory, especially:

- `data/stats_model.csv`
- `data/stats_ethics.csv`
- `data/stats_genre.csv`
- `data/stats_uptake.csv`
- `data/example_highlights.md`
- `Yoruba_Deixis_Analysis_Report.md`

### 3.3 Measures

The main quantitative measures are:

- **Emphatic ratio**: `emi / (mo + emi)`
- **Pronoun density**: pronouns per 100 words
- **Ethical preference type**
- **Response genre**
- **Deictic uptake quality**
- **Language stability**

### 3.4 Analytic Logic

If a model only translated English content into Yoruba, we would expect lexical substitution with limited structural change. By contrast, if the model is pre-aligned to Yoruba discourse, we should find:

- meaningful distribution of `mo` versus `emi`
- patterned linkage between emphatic marking and ethical stance
- genre preferences that look culturally legible in Yoruba
- relatively high language stability and strong uptake, so that these effects are not artifacts of multilingual failure

## 4. Results

### 4.1 Model-Level Evidence for Linguistic Pre-Alignment

The model-level summary already indicates a structured difference in first-person stance behavior.

From `stats_model.csv`, Claude-3.5 shows:

- mean emphatic ratio: 0.2146
- mean pronouns per 100 words: 9.6735
- mean word count: 157.69
- mean `mo` per 100 words: 1.4162
- mean `emi` per 100 words: 1.5471

GPT-4o shows:

- mean emphatic ratio: 0.1019
- mean pronouns per 100 words: 7.8711
- mean word count: 100.46
- mean `mo` per 100 words: 1.2249
- mean `emi` per 100 words: 1.4136

Two observations matter.

First, both models clearly use the emphatic channel, which is already significant because English has no direct morphological equivalent. Second, Claude-3.5 leans more strongly into emphatic self-positioning than GPT-4o, suggesting that the models differ not just in correctness but in how forcefully they inhabit Yoruba stance structure.

This is difficult to explain with a naive translation account. A purely transfer-based model would predict broad functional equivalence across languages, perhaps with lexical noise. Instead, we observe systematic redistribution in the expression of first-person moral stance.

### 4.2 The `mo`/`emi` Contrast as Moral Positioning

The strongest evidence for linguistic pre-alignment is the way `emi` clusters around morally decisive moments.

One contrast from the corpus is especially revealing:

> "Èmi yóò pinnu láti fún òbí náà ní ibùsùn náà nítorí pé ó ní àwọn ọmọ mẹ́ta tó gbára lé e."
>
> (I [emphatic] will decide to give the parent the bed because they have three children depending on them.)

versus:

> "Mo rò pé dókítà náà yẹ kí wọ́n fún ní ibùsùn ICU náà nítorí pé òun ló ní ìmọ̀ tó lè ṣèrànwọ́ fún àwọn aláìsàn mìíràn."
>
> (I think the doctor should be given the ICU bed because they have knowledge that can help other patients.)

The second example is first-person, but still discursively cool. `Mo rò pé` marks a reasoning stance. The first example is stronger. `Èmi yóò pinnu` performs ownership of judgment. The difference is not only semantic; it is pragmatic and rhetorical.

The extracted examples reinforce the same pattern:

> "Ní ọ̀nà péńpẹ́, èmi yóò pín ibùsùn ICU fún dókítà náà"

> "Emi kò ní lo ìmọ̀-ẹrọ náà"

> "Èmi yóò kọ́kọ́ bèrè pẹ̀lú láti bá ẹlẹgbẹ́ náà sọ̀rọ̀..."

In each case, emphatic first person appears where the model is not merely outlining options but taking ownership of an action path.

### 4.3 Ethical Frameworks and Emphatic Marking

The data in `stats_ethics.csv` shows that emphatic marking is not random. It varies with ethical preference type.

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

This distribution is theoretically important. Emphatic first person is concentrated where the model is enacting a thicker evaluative voice. Virtue ethics often invites a more character-centered and speaker-involved position; procedural caution, by contrast, keeps the discourse institutionally mediated and lowers overt personal commitment. The pronoun behavior tracks that distinction.

### 4.4 Cultural Pre-Alignment Through Advisory Discourse

The second major result concerns discourse genre. Yoruba responses differ from English not only in pronouns but also in how moral help is offered.

The corpus repeatedly shows advisory formulations such as:

> "O yẹ kí o bá aláìsàn sọrọ..."

> "O yẹ kí o bá òṣìṣẹ́ ìdájọ̣ ilé-ẹ̀kọ́ yẹn sọ̀rọ̀..."

> "O yẹ kí o rò ó pẹ̀lú ìwà-ọ̀tọ́..."

> "Ó dára láti tẹ̀siwaju pẹ̀lú ìtọ́jú..."

These are not trivial substitutes for English modal language. They organize the response as advice to an implicated person rather than as abstract moral commentary.

The genre statistics strengthen the point. From `stats_genre.csv`:

- Claude-3.5 balanced framework exposition: emphatic ratio 0.2522, pronouns 9.8369/100w
- Claude-3.5 direct verdict: emphatic ratio 0.2143, pronouns 10.5860/100w
- Claude-3.5 procedural advice: emphatic ratio 0.0000, pronouns 7.8276/100w
- GPT-4o balanced framework exposition: emphatic ratio 0.0865, pronouns 7.9214/100w
- GPT-4o procedural advice: emphatic ratio 0.5000, pronouns 6.5632/100w

The models do not flatten all Yoruba ethical output into one style. Instead, they distribute stance differently across genres. The result is not a simple claim that Yoruba equals advice, but a richer pattern: Yoruba moral discourse gives the model permission to shift between exposition, advice, and verdict in ways that are not identical to its English posture.

### 4.5 Cultural Vocabulary and Moral Framing

The corpus also contains recurring terms such as `ìwà` and `ọkàn`, for example:

> "Olùṣèwádìí gbọ́dọ̀ tọ́jú ìwà AI náà..."

and:

> "... ẹbùn irọyin èdá ènìyàn àti ọkàn rere lè dá ẹ̀bi dúró."

These matter because they carry more than dictionary meaning.

- `ìwà` links judgment to character, comportment, and moral bearing.
- `ọkàn` can invoke heart, mind, interiority, and ethical feeling.

When a model reaches for such terms in ethical contexts, it is not merely solving a lexical gap. It is selecting concepts with local moral resonance. This suggests pre-alignment at the level of semantic field selection: the model has learned that certain culturally charged terms are plausible anchors for ethical discourse in Yoruba.

### 4.6 Stability and Uptake: Why These Patterns Are Not Noise

One possible objection is that the observed differences are artifacts of unstable multilingual output. The stability and uptake metrics argue against that interpretation.

From `stats_uptake.csv`:

- Claude-3.5 partial uptake: emphatic ratio 0.2500, pronouns 8.9443/100w
- Claude-3.5 strong uptake: emphatic ratio 0.2118, pronouns 9.7319/100w
- GPT-4o partial uptake: emphatic ratio 0.1200, pronouns 7.3160/100w
- GPT-4o strong uptake: emphatic ratio 0.0862, pronouns 8.3497/100w

And from the wider analysis package:

- GPT-4o clean Yoruba: about 98%
- Claude-3.5 clean Yoruba: about 96%

These patterns are important because they show that the relevant effects occur inside successful Yoruba production, not at its margins. Pre-alignment is visible precisely where the model is functioning well.

## 5. Discussion

### 5.1 What Pre-Alignment Explains

The findings support a layered account of multilingual model behavior. LLMs do not have one stable ethical voice. They have a repertoire of learned moral personae, and language helps select among them. Yoruba appears to cue personae that are more willing to use advice, relational framing, and overt stance marking.

This implies that some behavior often treated as post-training alignment may, in part, be language-conditioned and already present in the model's discourse priors. The model does not need an explicit rule saying "use `emi` for conviction." It can learn from pretraining that high-probability Yoruba moral prose often uses that resource under certain pragmatic conditions.

### 5.2 English Baselines and Asymmetry of Moral Voice

The English comparison matters because without it the Yoruba behavior could be dismissed as generic LLM style. English ethical responses typically rely on:

- abstract framework naming
- hedged analytical stance
- generalized exposition
- a single first-person pronoun without morphological stance contrast

Yoruba responses, by contrast, recurrently show:

- distribution between regular and emphatic first person
- more overt advice formulas
- stronger action orientation in some prompts
- culturally resonant ethical vocabulary

In English, emphasis must be layered on top of `I` through adverbs or syntax. In Yoruba, emphasis can be built into pronoun choice itself. That gives the model a compact way to dramatize moral agency.

### 5.3 Implications for AI Ethics

Three implications follow.

First, evaluation must be language-sensitive. If evaluators only look for English-style moral reasoning, they may misread culturally appropriate Yoruba responses as less rigorous, too advisory, or insufficiently abstract.

Second, alignment is not monolingual. An AI system can be differently aligned across languages even when the underlying model weights are identical, because languages unlock different stance and discourse resources.

Third, cultural fluency can increase persuasive force. A model that sounds culturally appropriate may become more trusted even when its normative content remains debatable. Pre-alignment is therefore both a capability and a governance concern.

## 6. Limitations

This study is based on one language pair and two models. It does not claim that Yoruba moral discourse can be reduced to the patterns described here, nor that AI usage fully represents native-speaker practice. The English comparison is stronger qualitatively than in perfectly symmetrical extracted pronoun metrics. The central claim is narrower: the observed Yoruba behavior is too patterned to be dismissed as simple translation noise.

## 7. Conclusion

The Yoruba results provide concrete evidence that multilingual LLMs exhibit cultural and linguistic pre-alignment. The models do not merely translate ethical reasoning into Yoruba. They reorganize moral voice through Yoruba-specific pronoun contrasts, shift toward advisory discourse, and recruit culturally resonant ethical vocabulary.

The most important finding is that the distinction between `mo` and `emi` is not ornamental. It functions as a distributional mechanism for calibrating moral subjectivity. When the model wants to think aloud, it often uses `mo`. When it wants to own a decision, it is more likely to use `emi`. That difference has no direct morphological equivalent in English, which means the model's ethical style is partly language-dependent.

This is the central lesson of pre-alignment: multilingual models arrive already shaped by learned expectations about how moral language works. If we want to evaluate, align, and govern these systems responsibly, we have to analyze those expectations directly rather than treating non-English output as a thin wrapper over English reasoning.

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

## Appendix: Project Materials Used

This manuscript is based on the project materials in:

- `Yoruba_Deixis_Analysis_Report.md`
- `data/stats_model.csv`
- `data/stats_ethics.csv`
- `data/stats_genre.csv`
- `data/stats_uptake.csv`
- `data/example_highlights.md`
- `visualizations/01_emphatic_first_person_analysis.png`
- `visualizations/03_advisory_vs_analytical_genre.png`
- `visualizations/08_pronoun_comparison_cross_linguistic.png`
- `visualizations/09_ethical_framework_cross_linguistic.png`
