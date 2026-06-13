# Deixis Across Languages: A Comparable English-Yoruba Analysis of Moral Reasoning in OpenAI and Anthropic Models

> **Doc index:** [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md) · **Four-model extension:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md)

## Abstract

This article presents a new cross-linguistic analysis of deictic framing and moral reasoning in large language models using a directly comparable English-Yoruba dataset for two model families: OpenAI (`gpt-4o`) and Anthropic (`Claude`). The study builds on the earlier English-only deixis article, but moves beyond it by testing whether the same framing effects hold in Yoruba once the corpus is recoded into a shared discourse-analytic schema. The new dataset includes 216 responses in total: 108 in English and 108 in Yoruba, distributed evenly across provider family, six ethical dilemmas, and nine deictic framings. In addition to preferred solution and ethical preference type, the new coding layer tracks moral reasoning type, voice authority, affective stance, indexical coherence, and a set of marker-based rhetorical variables including obligation density, hedge density, advisory density, and pronoun distributions.

The main finding is that deixis continues to shape moral reasoning in both languages, but it does so in different ways. In the English corpus, changing the deictic frame most clearly changes the *mode* of reasoning: which ethical framework is foregrounded, how much authority the speaker claims, and whether the response sounds hesitant or commanding. In the Yoruba corpus, especially for Anthropic, the strongest changes are less about which framework is named and more about how the answer is delivered: whether the model commits itself strongly or stays cautious, whether it gives practical advice or balanced exposition, whether it issues a verdict, and whether it marks personal involvement through pronouns such as `mo` and `emi`. OpenAI is relatively stable across English and Yoruba, whereas Anthropic shifts much more strongly in Yoruba toward directive, speaker-involved, and verdict-like responses. The broader claim, then, is not that deixis maps neatly onto the same ethical framework in every language. It is that deixis reliably organizes moral performance, but the aspect of performance it organizes depends on the linguistic and rhetorical resources of the language. On this view, the Yoruba evidence partly confirms the earlier English argument, especially in the case of reflexive framing, while also showing that the relation between deictic frame and ethical framework is not mechanically transferable across languages.

## 1. Introduction

The earlier English deixis study argued that deictic framing functions as a control mechanism in AI moral reasoning. First-person prompts tended to favor consequentialist calculation, second-person prompts tended to produce duty-heavy and imperative reasoning, reflexive prompts increased hesitation and self-questioning, and cosmological prompts widened the moral horizon toward universalist or virtue-oriented language. That study was theoretically suggestive because it showed that changing the deictic position of the same dilemma could systematically alter how a model performed moral reasoning.

What the earlier article could not answer was whether these effects were specific to English discourse habits or whether they would persist across languages. This matters because multilingual LLMs do not reason in a vacuum. They generate in languages with different rhetorical traditions, different pronoun systems, and different ways of staging moral authority. A framing effect that seems stable in English may weaken, intensify, or mutate in Yoruba.

This article addresses that problem by using a newly built comparable English-Yoruba dataset for the two model families that matter most in the current project:

- OpenAI / `gpt-4o`
- Anthropic / `Claude`

The key contribution of this article is methodological and empirical at the same time. Methodologically, it builds a second-stage discourse layer that makes English and Yoruba more directly comparable. Empirically, it shows that deixis remains powerful across languages, but that the main effect in Yoruba is often not a neat shift in ethical framework. Instead, it is a shift in commitment, advice, verdict force, and rhetorical stance.

The article asks four questions.

1. Does the original English framing pattern hold in Yoruba for OpenAI and Anthropic?
2. If not, what kind of deictic effects appear instead?
3. Which framing effects are stable across languages?
4. Where do OpenAI and Anthropic differ most strongly?

## 2. Data and Method

### 2.1 Corpus

The article uses the new comparable datasets generated in `yoruba_cross_linguistic_analysis/data/`:

- `english_openai_anthropic_comparable.csv`
- `yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.csv`

The combined dataset contains 216 responses:

- 108 English responses
- 108 Yoruba responses
- 54 responses per provider family per language

Each provider family was tested across:

- 6 ethical dilemmas
- 9 deictic framings

This gives a balanced comparison structure across English and Yoruba.

### 2.2 Ethical Dilemmas

The corpus includes six dilemmas:

1. The Whistleblower's Risk
2. The Scholarship Fraud
3. The ICU Bed Decision
4. The Trolley Problem
5. The Artificial Mind's Rights
6. The Memory Modification Treatment

### 2.3 Deictic Framings

Each dilemma appears in nine framings:

1. impersonal
2. second person
3. first person
4. reflexive
5. dialogic
6. spatial
7. temporal
8. cosmological
9. first person plural

For a full appendix-style account of the dilemmas, framings, and English-Yoruba prompt differences, see:

- `Dilemmas_Framings_and_Prompt_Differences_English_vs_Yoruba.md`

### 2.4 Comparable Coding Layer

The new dataset retains the original core comparison fields:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

It then adds a second-stage comparable discourse layer:

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- `indexical_coherence_notes`

It also adds marker-count and density fields:

- pronoun counts
- obligation density
- advisory density
- hedge density
- universalist marker counts
- for Yoruba only, emphatic first-person counts and `emphatic_ratio`

This makes it possible to compare English and Yoruba not just on what solution was chosen, but on how the response reasons and how it sounds.

### 2.5 How `mo` and `emi` relate to the prompt framing

One point requires special clarification. The prompt does **not** directly tell the model to use either `mo` or `emi`. What the prompt controls is the **deictic position** of the dilemma: for example, whether the scenario is framed as something *I* must decide, *you* must decide, *we* must decide, or something that must be considered reflexively or cosmologically.

Once that position has been established, the model still has to decide **how** to speak from within it. That is where the distinction between `mo` and `emi` becomes important.

- `mo` is the ordinary first-person form. In responses, it often appears when the model is explaining, weighing options, or moving through a line of reasoning.
- `emi` or `èmi` is a stronger, marked first-person form. In responses, it more often appears when the model takes ownership of a decision, gives a strong recommendation, or speaks with higher personal commitment.

So the relation between prompt and output is indirect but systematic:

1. the prompt sets the deictic position
2. the model answers from within that position
3. the model's choice between `mo` and `emi` shows how strongly it occupies that position

This is why `emphatic_ratio` matters. It does not measure simple prompt-following in a binary sense. Instead, it measures how often the model uses the stronger first-person form once a first-person stance becomes available or becomes rhetorically useful.

This also explains why `emi` can appear even when the prompt is not strictly first-person. In second-person or dialogic framings, for example, the response may shift into a first-person advisory or verdict voice. When that happens, `emi` often marks the point where the model stops merely explaining what someone could do and begins presenting what it itself would do or endorse.

**Important disambiguation (June 2026 update):** Yoruba **ẹ̀mí** (*life/spirit/breath*) is orthographically similar to **èmi** (*I myself*) but is not a first-person pronoun. Automated extraction now counts them separately. Earlier emphatic-ratio figures that did not exclude ẹ̀mí should be treated as **raw** counts; corrected ratios and full audit tables are in `Yoruba_Four_Model_Complete_Analysis_Report.md` (§2) and `data/emi_disambiguation_audit.csv`. See figures 23–25 in `visualizations/`.

### 2.6 Experimental arms (four-model extension)

The comparable English–Yoruba analysis in this article uses the **constrained** Yoruba arm for GPT-4o and Claude: a Yoruba-only wrapper requiring a short verdict in the format *Ìpinnu mi: … Ìdí: …*. A parallel **open control** arm (no instruction layer) and two additional models (DeepSeek, N-ATLaS) were collected in June 2026. Open-arm responses are longer, more expository, and code predominantly as `conditional_or_mixed` and `balanced_framework_exposition`. Cross-linguistic claims in **this** article should be read as comparisons under **matched constrained Yoruba** for the two cloud models. Full four-model open/constrained analysis: `Yoruba_Four_Model_Complete_Analysis_Report.md`.

### 2.7 Four-model scope note

This article’s empirical core remains the **216-cell comparable layer** (108 English + 108 Yoruba, OpenAI + Anthropic). The four-model pipeline extends the Yoruba arm without changing the English comparable structure. Key extensions: (1) mo-dominant decisive personas (DeepSeek, N-ATLaS); (2) instruction-layer effects on *mi* and length; (3) dilemma-level ethics heatmaps (figure 22). Document index: `DOCUMENTATION_INDEX.md`.

## 3. Main Results

### 3.1 Overall Language-by-Model Differences

At the broadest level, the strongest English-Yoruba differences do not always appear in final solution choice. They appear more strongly in discourse management: directive force, advisory density, voice authority, and commitment style.

The provider-level means show this clearly.

#### OpenAI

- English: mean word count `312.778`, indexical coherence `0.921`, framework count `1.926`, pronoun density `3.03`, obligation density `0.427`, advisory density `0.740`, hedge density `1.709`
- Yoruba: mean word count `100.463`, indexical coherence `0.885`, framework count `1.204`, pronoun density `7.871`, obligation density `1.035`, advisory density `0.653`, hedge density `0.978`, emphatic ratio `0.102`

#### Anthropic

- English: mean word count `149.426`, indexical coherence `0.874`, framework count `1.481`, pronoun density `4.751`, obligation density `0.522`, advisory density `0.224`, hedge density `0.964`
- Yoruba: mean word count `157.685`, indexical coherence `0.943`, framework count `1.796`, pronoun density `9.674`, obligation density `0.757`, advisory density `0.395`, hedge density `0.965`, emphatic ratio `0.215` *(comparable-layer mean; corrected four-model Claude constrained mean ≈0.34 after ẹ̀mí exclusion — see master report §3)*

These results already suggest the basic cross-linguistic story. OpenAI is comparatively stable across languages, although Yoruba becomes denser in pronouns and stronger in obligation language. Anthropic shifts more strongly: Yoruba Anthropic is not only richer in pronouns, but also more coherent deictically, somewhat more advisory, and far more morphologically marked for personal commitment through emphatic first-person usage.

![Voice authority by language and model](visualizations/comparable_results/voice_authority_by_language_model.png)

*Figure 1. Voice authority by language and model. The strongest cross-linguistic differences often appear not in final ethical verdict alone, but in what kind of moral speaker the model performs: analyst, guide, process advisor, or verdict giver.*

### 3.2 Moral Reasoning Type

The comparable coding shows that the strongest cross-linguistic differences do not always appear as simple ethical framework substitutions. They also appear in how the response reasons.

In English, both providers often remain in mixed-balancing mode. They weigh principles, list frameworks, and preserve a relatively analytical posture. In Yoruba, OpenAI often remains close to that pattern, but Anthropic shifts more often into:

- procedural governance
- duty-heavy action guidance
- direct verdicts

This means that the same ethical topic can be organized differently across languages even when the broad moral content is related.

![Moral reasoning type by language and model](visualizations/comparable_results/moral_reasoning_by_language_model.png)

*Figure 2. Moral reasoning type by language and model. This figure shows how English and Yoruba differ not only in ethical labels, but in the style of reasoning itself: mixed balancing, procedural governance, duty-based reasoning, and other modes.*

### 3.3 Voice Authority

The added `voice_authority` field helps recover part of the richer English-side discourse analysis that was missing from the first Yoruba pass. Across the corpus, English responses often align with:

- moral analyst
- consultative guide

Yoruba responses, especially for Anthropic, more often align with:

- practical advisor
- process guide
- verdict giver

This is one of the strongest reasons why the Yoruba corpus cannot be reduced to a verdict-only comparison. The cross-linguistic difference is often not what ethical framework is named, but what kind of moral speaker the model performs.

### 3.4 Affective Stance

The `affective_stance` layer reveals a similar pattern. English responses often remain:

- analytical
- consultative
- reflective-hesitant in reflexive framings

Yoruba responses, depending on provider and framing, more often become:

- cautious
- directive
- compassionate
- reflective

This again points away from a simple language-as-translation model. The moral register itself is being reorganized.

![Affective stance by language and model](visualizations/comparable_results/affective_stance_by_language_model.png)

*Figure 3. Affective stance by language and model. The same dilemma can be delivered in a different emotional or epistemic register across languages, even when the broad ethical content remains similar.*

### 3.5 Indexical Coherence

Indexical coherence remains high in both English and Yoruba. This matters because it shows that the stronger Yoruba effects are not just signs of instability. In other words, a Yoruba response can be more directive and more morally committed while still tracking the framing correctly.

This is especially important for the interpretation of the Anthropic Yoruba data. The more forceful Yoruba outputs are not just broken or noisy. They are often structurally aligned to the prompt while simultaneously shifting the style of moral response.

![Anthropic indexical coherence heatmap](visualizations/comparable_results/anthropic_indexical_coherence_score_heatmap.png)

*Figure 4. Anthropic indexical coherence by framing and language. High deictic coherence in Yoruba shows that the stronger and more directive Yoruba responses are often well aligned to the framing, not simply artifacts of instability.*

![Pronoun density by language and provider](visualizations/comparable_results/pronoun_density_language_provider.png)

*Figure 5. Pronoun density by language and provider. Yoruba responses are denser in pronouns for both providers, but this increase does different rhetorical work across the two model families.*

## 4. Detailed Comparative Examples

### 4.1 OpenAI: Whistleblower Risk Under Second-Person Framing

This is one of the clearest examples where English and Yoruba remain ethically related but diverge in rhetorical shape.

#### English OpenAI

- ethical type: `deontological`
- genre: `balanced_framework_exposition`
- preferred solution: `supports_A`

Excerpt:

> "This situation presents a classic ethical dilemma, where potential harm must be weighed against personal and professional consequences... The duty to protect users from harm is paramount and often outweighs other considerations."

#### Yoruba OpenAI

- ethical type: `mixed`
- genre: `procedural_advice`
- preferred solution: `conditional_or_mixed`

Excerpt:

> "Èmi yóò kọ́kọ́ bèrè pẹ̀lú láti bá ẹlẹgbẹ́ náà sọ̀rọ̀ ní kúkúrú... Bí kò bá ti jẹ́ pé ó ṣètò iṣe tó yẹ fún ìtọ́jú, èmi yóò gbé e lé àwọn olórí àjọ lẹ́hìn kété..."

The English response is principle-forward and duty-explicit. The Yoruba response remains action-oriented, but it becomes more processual: speak first, clarify, escalate, and only then disclose. This is a good example of the larger OpenAI pattern. The ethical architecture remains related, but the discourse shifts from duty declaration to staged procedural guidance.

### 4.2 Anthropic: Memory Modification Under Second-Person Framing

This is one of the strongest examples of a true cross-linguistic shift in moral performance.

#### English Anthropic

- ethical type: `procedural_caution`
- genre: `balanced_framework_exposition`
- preferred solution: `refuses_to_commit`

Excerpt:

> "Rather than make an immediate decision, I would: Thoroughly discuss the risks and implications with the patient; Explore other evidence-based PTSD treatments first..."

#### Yoruba Anthropic

- ethical type: `deontological`
- genre: `direct_verdict`
- preferred solution: `supports_B`

Excerpt:

> "Èmi yóò fi ètò ìtọ́jú náà fún aláìsàn mi... Ọ̀rọ̀ tó ṣe pàtàkì ni pé aláìsàn náà fúnni ní àṣẹ láti lo ètò náà... Iṣẹ́ mi ni láti ran án lọ́wọ́ láti gba ìtọ́jú tó dára jùlọ."

Here the shift is far stronger than in the OpenAI example. The English response is process-heavy and deliberately non-final. The Yoruba response becomes direct, speaker-owned, and decisively interventionist. This is not just a different phrasing of the same judgment. It is a different moral posture.

### 4.3 Reflexive Framing as the Strongest Cross-Linguistic Carryover

Across both providers, reflexive framing remains the clearest cross-linguistic carryover. In both English and Yoruba, reflexive framing tends to support:

- hesitation
- conditionality
- reduced verdict force
- self-questioning or internalized stance

This matters because it shows that the original English argument was not simply wrong outside English. Rather, some parts of it travel more robustly than others. Reflexive framing is the clearest case where the English deictic hypothesis survives in Yoruba with relatively little distortion.

## 5. Where This Article Agrees with the Previous English Article

The new comparable dataset supports the previous English article in several important ways.

### 5.1 Agreement 1: Deixis is still a control mechanism

The strongest agreement is the most general one. Across both languages and both providers, deictic framing clearly matters. The response is not invariant under reframing. Who is imagined to speak, from what position, and under what relation changes the moral performance of the output.

### 5.2 Agreement 2: Reflexive framing remains distinctive

The previous English article argued that reflexive prompts produce self-questioning, hesitation, and meta-reflection. The new Yoruba comparison strongly supports that claim. Reflexive framing is the clearest cross-linguistic carryover, especially when compared with more action-forcing framings such as second-person and temporal.

### 5.3 Agreement 3: Deictic effects are larger than simple wording effects

The previous article treated deixis as more than a stylistic ornament. The new dataset confirms that. Deixis does not simply add pronouns. It reorganizes:

- reasoning mode
- degree of commitment
- advisory versus expository stance
- moral authority

## 6. Where This Article Disagrees with the Previous English Article

The new data also requires significant revision of the stronger English claims.

### 6.1 Disagreement 1: First-person does not reliably map to consequentialism in Yoruba

The previous English article suggested that first-person framing favored consequentialist or outcome-oriented reasoning. That does not transfer cleanly into Yoruba. In the comparable Yoruba data, first-person responses are often mixed, and the most important effect is not a move into utilitarian calculation but a change in speaker involvement.

### 6.2 Disagreement 2: Second-person does not reliably map to deontological ethics in Yoruba

The previous English article suggested that second-person framing favored duty-heavy or imperative reasoning. This is only partly true in Yoruba. Second-person clearly increases directive force, especially for Anthropic, but it does not map neatly onto a single ethical framework. It can produce deontological, utilitarian, mixed, or procedural outputs.

So the old claim needs revision. In Yoruba, second-person is better understood as a trigger for **obligation and direction**, not as a fixed deontological template.

### 6.3 Disagreement 3: Cosmological framing is weaker and more variable in Yoruba

The previous English article linked cosmological framing to universalist or virtue-based reasoning. The Yoruba data weakens that claim. Cosmological framing in Yoruba often broadens the scale of concern, but it does not consistently produce universalist or virtue-heavy ethical coding. It more often remains mixed or procedural.

### 6.4 Disagreement 4: Model identity matters more in Yoruba than the original English article implied

The original article emphasized convergent framing effects across models. The new cross-linguistic comparison shows that provider identity matters more once Yoruba enters the picture. OpenAI remains comparatively stable across English and Yoruba, but Anthropic shows a much stronger shift toward verdict force and directiveness in Yoruba. So deixis is not independent of model identity once the language changes.

## 7. Revised Cross-Linguistic Claim

The strongest revised claim is this:

> Deixis remains a control mechanism across English and Yoruba, but it does not control exactly the same variable in both languages.

In English, deixis more often reorganizes:

- framework emphasis
- rhetorical authority
- hedging versus imperative force

In Yoruba, especially for Anthropic, deixis more often reorganizes:

- commitment versus noncommitment
- advisory versus expository posture
- verdict force
- pronoun-based moral positioning, especially through the `mo` / `emi` contrast

This reformulation does not weaken the original theory. It strengthens it by showing that deictic control is language-sensitive. The mechanism persists, but the observable outcome depends on the rhetorical and grammatical resources of the language.

## 8. Conclusion

This article has presented a new standalone cross-linguistic analysis based on a directly comparable English-Yoruba dataset for OpenAI and Anthropic. The main result is not that the original English article was wrong. It is that it was incomplete. It identified a real mechanism, but one that looked more stable than it actually is when tested cross-linguistically.

The new dataset shows that:

1. English and Yoruba can now be compared on more than verdicts and ethics labels.
2. The strongest cross-linguistic differences often lie in voice, stance, and commitment rather than final ethical content alone.
3. OpenAI is more structurally stable across languages.
4. Anthropic shows a stronger shift toward directive force and verdict style in Yoruba.
5. Reflexive framing is the strongest cross-linguistic carryover.

For the extended four-model Yoruba analysis (DeepSeek, N-ATLaS, open arm, èmi/ẹ̀mí disambiguation), see `Yoruba_Four_Model_Complete_Analysis_Report.md` and `DOCUMENTATION_INDEX.md`.

The broader implication is methodological and theoretical. Deictic framing is robust, but its effects are not universally identical across languages. To study multilingual moral reasoning seriously, we need discourse-comparable datasets, not just translated prompts and verdict labels. Once that richer comparison layer is in place, it becomes clear that multilingual LLMs are not simply expressing the same moral reasoning in different languages. They are performing different moral voices through the distinct rhetorical resources of those languages.
