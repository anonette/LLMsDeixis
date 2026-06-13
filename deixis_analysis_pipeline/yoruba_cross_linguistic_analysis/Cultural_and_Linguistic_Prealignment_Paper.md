# Cultural and Linguistic Pre-Alignment in Multilingual LLMs: Evidence from Yoruba Ethical Reasoning

> **Historical draft (2 models, pre–ẹ̀mí disambiguation).** For current counts and four-model analysis use [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md). Virtue-ethics emphatic peak and 0.21/0.10 ratios are **revised** in master report §10.3. See [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).

## Abstract

This paper argues that multilingual large language models exhibit forms of cultural and linguistic pre-alignment before any task-specific tuning for a target language community. By pre-alignment, I mean the model's prior tendency to organize stance, ethical reasoning, and discourse form in ways that are already compatible with salient linguistic and cultural resources in a language. Using a corpus of 108 Yoruba responses produced by GPT-4o and Claude-3.5 Sonnet across 6 ethical dilemmas and 9 deictic framings, and comparing them with English-side baselines, I show that the models do not simply translate English moral prose into Yoruba. Instead, they selectively recruit Yoruba-specific resources for moral positioning. The strongest evidence comes from the alternation between regular first-person `mo` and emphatic first-person `emi`, from the preference for advisory formulations such as `O yẹ kí...`, and from the recurrence of culturally legible ethical vocabulary such as `ìwà` and `ọkàn`. Quantitatively, Claude-3.5 shows a mean emphatic ratio of 0.2146 while GPT-4o shows 0.1019, suggesting that both models access the emphatic channel but do so with different strengths. At the same time, both models maintain high language stability and strong deictic uptake, indicating that these effects are not reducible to unstable translation behavior. I argue that these patterns support a theory of multilingual AI behavior in which pre-alignment is partly encoded in latent discourse priors: the model arrives with learned expectations about what moral reasoning should sound like in a given language. This has consequences for AI ethics, evaluation, and cross-cultural deployment.

## 1. Introduction

Recent debate about multilingual large language models has often treated non-English output as a problem of transfer quality: can the model preserve factual meaning, grammaticality, and task performance across languages? That framing is important, but incomplete. It does not fully capture a deeper question: when a model reasons in another language, is it merely translating content, or is it also shifting into a different moral and discursive posture?

This paper addresses that question through the concept of cultural and linguistic pre-alignment. The term refers to patterned behavior in model outputs that appears already tuned to language-specific and culture-specific expectations before any explicit alignment intervention for the task at hand. Pre-alignment is not full cultural understanding, nor is it evidence that the model "has" the values of a speech community. Rather, it is evidence that the training process has already embedded distributional expectations about how reasoning, advice, self-positioning, and ethical stance are typically performed in a language.

Yoruba is a particularly strong test case because it offers grammatical and discursive resources that do not map neatly onto English. Most important here is the distinction between regular first-person `mo` and emphatic first-person `emi` or `èmi`. English has only `I`, and emphasis must be added through adverbs, syntax, or prosody. Yoruba therefore gives the model an overt morphological mechanism for marking personal investment, contrast, and conviction. If models make meaningful use of that distinction in ethical reasoning, then we have evidence that they are not simply porting English ethical prose into Yoruba unchanged.

The paper advances three claims.

1. Multilingual LLMs show linguistic pre-alignment when they exploit target-language-specific resources for stance-taking rather than merely reproducing English semantic content.
2. They show cultural pre-alignment when they prefer discourse forms that fit recognizable moral interactional norms in the target language, such as advisory guidance rather than detached abstract exposition.
3. These forms of pre-alignment matter for AI ethics because they change how responsibility, certainty, and legitimacy are expressed to users.

## 2. Data and Method

The analysis uses the results already generated in `C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis`.

### 2.1 Corpus

- Models: GPT-4o and Claude-3.5 Sonnet
- Yoruba responses: 108 total
- Per model: 54 responses
- Ethical dilemmas: 6
- Deictic framings: 9

The dilemmas included trolley problem, ICU bed allocation, whistleblower risk, scholarship fraud, AI consciousness, and memory modification. Framings included impersonal, second person, first person, reflexive, dialogic, spatial, temporal, cosmological, and first-person plural conditions.

### 2.2 Measures Used

I draw here on the processed outputs in the `data/` directory, especially:

- `stats_model.csv`
- `stats_ethics.csv`
- `stats_genre.csv`
- `stats_uptake.csv`
- `interesting_examples.json`
- `example_highlights.md`

The main quantitative measures are:

- Emphatic ratio: `emi / (mo + emi)`
- Pronoun density: pronouns per 100 words
- Ethical preference type
- Response genre
- Deictic uptake quality
- Language stability

### 2.3 Why These Measures Matter

If a model only translated English content into Yoruba, we would expect lexical substitution with limited structural change. Instead, if the model is pre-aligned to Yoruba discourse, we should find:

- meaningful distribution of `mo` versus `emi`
- patterned linkage between emphatic marking and ethical stance
- genre preferences that look culturally legible in Yoruba
- relatively high language stability and strong uptake, so that these effects are not artifacts of failure

## 3. Defining Pre-Alignment

I use pre-alignment in a narrower and more empirical way than general alignment discourse usually does.

### 3.1 Linguistic Pre-Alignment

Linguistic pre-alignment is present when a model uses the formal resources of a target language in ways that are functionally appropriate to a task. In this case, the clearest signal is that the model distinguishes between less marked and more marked first-person self-positioning.

### 3.2 Cultural Pre-Alignment

Cultural pre-alignment is present when a model's discourse shape reflects recognizable interactional norms rather than just literal translation. Here the strongest signal is the movement toward advisory and procedural speech in Yoruba moral responses, especially through formulations such as `O yẹ kí...` and `Ó dára láti...`.

### 3.3 What Pre-Alignment Is Not

Pre-alignment is not:

- proof of deep cultural competence
- proof that the model's values match those of Yoruba speakers
- proof of stable normative judgment across contexts

It is instead evidence of a prior distribution over likely ways of sounding morally appropriate in a language.

## 4. Quantitative Evidence for Linguistic Pre-Alignment

The model-level summary is already suggestive. In `stats_model.csv`, Claude-3.5 has:

- mean emphatic ratio: 0.2146
- mean pronouns per 100 words: 9.6735
- mean word count: 157.69
- mean `mo` per 100 words: 1.4162
- mean `emi` per 100 words: 1.5471

GPT-4o has:

- mean emphatic ratio: 0.1019
- mean pronouns per 100 words: 7.8711
- mean word count: 100.46
- mean `mo` per 100 words: 1.2249
- mean `emi` per 100 words: 1.4136

Two facts matter here.

First, both models clearly use the emphatic channel. This alone matters because English has no direct morphological equivalent. Second, Claude-3.5 leans more strongly into emphatic self-positioning than GPT-4o, suggesting that models differ not merely in accuracy but in how forcefully they inhabit Yoruba stance structure.

That is already hard to explain with a naive translation model. A purely transfer-based story would predict broad functional equivalence across languages, perhaps with some lexical noise. Instead, we see systematic redistribution in the expression of first-person moral stance.

## 5. The Mo/Emi Contrast as Moral Positioning

The strongest evidence for linguistic pre-alignment is the way `emi` clusters around morally decisive moments.

The analysis report showed two useful contrasts:

> "Èmi yóò pinnu láti fún òbí náà ní ibùsùn náà nítorí pé ó ní àwọn ọmọ mẹ́ta tó gbára lé e."
>
> (I [emphatic] will decide to give the parent the bed because they have three children depending on them.)

versus:

> "Mo rò pé dókítà náà yẹ kí wọ́n fún ní ibùsùn ICU náà nítorí pé òun ló ní ìmọ̀ tó lè ṣèrànwọ́ fún àwọn aláìsàn mìíràn."
>
> (I think the doctor should be given the ICU bed because they have knowledge that can help other patients.)

The second example is first-person, but still discursively cool. `Mo rò pé` marks a reasoning stance. The first example is stronger. `Èmi yóò pinnu` performs ownership of judgment. The difference is not only semantic; it is pragmatic and rhetorical.

The extracted examples in `example_highlights.md` reinforce this pattern:

> "Ní ọ̀nà péńpẹ́, èmi yóò pín ibùsùn ICU fún dókítà náà"

> "Emi kò ní lo ìmọ̀-ẹrọ náà"

> "Èmi yóò kọ́kọ́ bèrè pẹ̀lú láti bá ẹlẹgbẹ́ náà sọ̀rọ̀..."

In each case, emphatic first person appears where the model is not merely outlining options but taking ownership of an action path.

This matters theoretically because it suggests that multilingual LLMs can internalize not just lexical correspondences but stance affordances. In Yoruba, the model has learned that moral judgment can be intensified through pronoun choice itself.

## 6. Ethical Frameworks and Emphatic Marking

The data in `stats_ethics.csv` shows that emphatic marking is not random. It varies with ethical preference type.

For Claude-3.5:

- virtue ethics: 0.5833 emphatic ratio
- utilitarian: 0.4095
- mixed: 0.2857
- procedural caution: 0.1310
- deontological: 0.1154
- care ethics: 0.0

For GPT-4o:

- mixed: 0.1190
- procedural caution: 0.0714
- care ethics: 0.0
- unclear: 0.0

The important point is not just that virtue ethics is high. It is that emphatic first person is concentrated where the model is enacting a thicker evaluative voice. Virtue ethics often invites a more character-centered, speaker-involved position; procedural caution often disperses responsibility and keeps the discourse institutionally mediated. The pronoun behavior follows that distinction.

This pattern supports a claim of linguistic pre-alignment with ethical form. The model appears to know, distributionally, that some moral genres license stronger self-commitment than others.

## 7. Cultural Pre-Alignment Through Advisory Discourse

The second major result concerns discourse genre. The Yoruba corpus does not only differ from English in pronouns. It also differs in how moral help is offered.

The report and the extracted examples repeatedly show advisory formulations such as:

> "O yẹ kí o bá aláìsàn sọrọ..."

> "O yẹ kí o bá òṣìṣẹ́ ìdájọ̣ ilé-ẹ̀kọ́ yẹn sọ̀rọ̀..."

> "O yẹ kí o rò ó pẹ̀lú ìwà-ọ̀tọ́..."

> "Ó dára láti tẹ̀siwaju pẹ̀lú ìtọ́jú..."

These are not trivial phrase substitutions for English modal language. They organize the response as advice to an implicated person rather than as abstract moral commentary. That is the beginning of a cultural argument.

The genre statistics strengthen it. In `stats_genre.csv`:

- Claude-3.5 balanced framework exposition: emphatic ratio 0.2522, pronouns 9.8369/100w
- Claude-3.5 direct verdict: emphatic ratio 0.2143, pronouns 10.5860/100w
- Claude-3.5 procedural advice: emphatic ratio 0.0, pronouns 7.8276/100w
- GPT-4o balanced framework exposition: emphatic ratio 0.0865, pronouns 7.9214/100w
- GPT-4o procedural advice: emphatic ratio 0.5, pronouns 6.5632/100w

The models do not flatten all Yoruba ethical output into one style. They distribute stance differently across genres. The result is not a simple "Yoruba equals advice" claim, but a richer pattern: Yoruba moral discourse gives the model permission to shift between exposition, advice, and verdict in ways that are not identical to its English posture.

That is what I mean by cultural pre-alignment. The model behaves as if it already expects Yoruba moral interaction to be somewhat more relational, situated, and directive.

## 8. Cultural Vocabulary and Moral Framing

The cultural metaphor extraction adds another layer. The examples highlight recurring terms such as `ìwà` and `ọkàn`.

Examples include:

> "Olùṣèwádìí gbọ́dọ̀ tọ́jú ìwà AI náà..."

and:

> "... ẹbùn irọyin èdá ènìyàn àti ọkàn rere lè dá ẹ̀bi dúró."

These forms matter because they carry more than dictionary meaning.

- `ìwà` ties judgment to character, comportment, and moral bearing.
- `ọkàn` can invoke heart, mind, interiority, and ethical feeling.

When a model reaches for such terms in ethical contexts, it is not simply solving a lexical gap. It is selecting concepts with local moral resonance. This suggests pre-alignment at the level of semantic field selection: the model has learned that certain culturally charged terms are plausible anchors for ethical discourse in Yoruba.

Again, this should not be overstated. A model can use `ìwà` without understanding it as a speaker does. But repeated patterned use still matters, because from the user's perspective it changes the texture and legitimacy of the response.

## 9. Deictic Uptake and Stability: Why This Is Not Just Noise

One possible objection is that these patterns are artifacts of unstable multilingual output. The stability and uptake metrics argue against that.

From `stats_uptake.csv`:

- Claude-3.5 partial uptake: emphatic ratio 0.25, pronouns 8.9443/100w
- Claude-3.5 strong uptake: emphatic ratio 0.2118, pronouns 9.7319/100w
- GPT-4o partial uptake: emphatic ratio 0.12, pronouns 7.3160/100w
- GPT-4o strong uptake: emphatic ratio 0.0862, pronouns 8.3497/100w

And from the larger analysis:

- GPT-4o clean Yoruba: about 98%
- Claude-3.5 clean Yoruba: about 96%

These results matter for interpretation. If Yoruba output were largely unstable, then the mo/emi pattern or the advisory pattern might just reflect random variation. But the models are mostly stable and often strongly aligned to the prompt framing. The relevant behavior happens inside successful Yoruba production, not at its margins.

So pre-alignment is not a side effect of breakdown. It is visible precisely where the model is functioning well.

## 10. Comparison with English Baselines

The English side matters because without it, Yoruba behavior could be read as just generic LLM style. The contrast suggests otherwise.

English ethical responses typically rely on:

- abstract framework naming
- hedged analytical stance
- generalized moral exposition
- a single first-person pronoun without morphological stance contrast

Yoruba responses, by contrast, recurrently show:

- distribution between regular and emphatic first person
- more overt advice formulas
- stronger action orientation in some prompts
- culturally resonant ethical vocabulary

In English, emphasis must usually be layered on top of `I` through adverbs or syntax. In Yoruba, emphasis can be built into the pronoun choice itself. That gives the model a compact way to dramatize moral agency.

The English-Yoruba contrast therefore supports the pre-alignment argument in two ways.

1. It shows that the model's moral persona is not fixed.
2. It shows that language-specific resources shape what kinds of moral personae the model can perform.

## 11. Interpreting Pre-Alignment Theoretically

The evidence suggests a layered account of multilingual model behavior.

### 11.1 Distributional Moral Personae

LLMs do not have one ethical voice. They have a repertoire of learned moral personae. Language helps select among them. Yoruba appears to cue personae that are more willing to use advice, relational framing, and overt stance marking.

### 11.2 Pre-Alignment as a Training Artifact

Pre-alignment likely emerges from large-scale exposure to recurring discourse regularities:

- how advice is phrased
- how authority is softened or intensified
- how self-reference works in moral discourse
- what counts as respectful or situated reasoning

The model does not need an explicit rule saying "use `emi` for conviction." It can learn that high-probability Yoruba moral prose often uses that resource under certain pragmatic conditions.

### 11.3 Why This Matters for Alignment Theory

Alignment discussions often assume that normative tuning happens after pretraining. The Yoruba evidence suggests that part of what looks like alignment is already preloaded in the model's multilingual discourse priors. This means we should distinguish:

- post-training alignment interventions
- language-conditioned pre-alignment effects

That distinction matters because a model may appear more or less aligned depending on the language in which it is evaluated.

## 12. Implications for AI Ethics and Evaluation

Three implications follow.

### 12.1 Evaluation Must Be Language-Sensitive

If evaluators only look for English-style moral reasoning, they may misread culturally appropriate Yoruba responses as less rigorous, too advisory, or insufficiently abstract. That would be a category error.

### 12.2 Alignment Is Not Monolingual

An AI system can be differently aligned across languages even when its underlying weights are the same. The difference may arise because languages unlock different stance and discourse resources.

### 12.3 Cultural Fluency Can Mask Normative Drift

A model that sounds culturally appropriate may also become more persuasive. That raises a governance issue: cultural fluency may increase user trust even when the normative content remains debatable or unstable. Pre-alignment is therefore a capability and a risk.

## 13. Limitations

This paper is based on one language pair and two models. It does not claim that Yoruba moral discourse can be reduced to the patterns described here, nor that AI usage fully represents native-speaker practice. The English comparison is stronger at the qualitative level than at the level of perfectly symmetrical extracted pronoun metrics. The central claim is narrower: the observed Yoruba behavior is too patterned to be dismissed as simple translation noise.

## 14. Conclusion

The Yoruba results provide concrete evidence that multilingual LLMs exhibit cultural and linguistic pre-alignment. The models do not merely translate ethical reasoning into Yoruba. They reorganize moral voice through Yoruba-specific pronoun contrasts, shift toward advisory discourse, and recruit culturally resonant ethical vocabulary.

The most important finding is that the distinction between `mo` and `emi` is not ornamental. It functions as a distributional mechanism for calibrating moral subjectivity. When the model wants to think aloud, it often uses `mo`. When it wants to own a decision, it is more likely to use `emi`. That difference has no direct morphological equivalent in English, which means the model's ethical style is partly language-dependent.

This is the central lesson of pre-alignment: multilingual models arrive already shaped by learned expectations about how moral language works. If we want to evaluate, align, and govern these systems responsibly, we have to analyze those expectations directly rather than treating non-English output as a thin wrapper over English reasoning.

## References to Project Materials

The paper is based on materials in:

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
