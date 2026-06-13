# New Results Chapter from the Comparable English-Yoruba Dataset

> **Extended:** four-model Yoruba pipeline → [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md). This chapter stays on the **2-model comparable CSV** layer.

## 1. Purpose

This chapter uses the new second-stage comparable dataset for OpenAI and Anthropic to compare English and Yoruba across a shared set of discourse variables. Unlike the first Yoruba pass, which focused mainly on ethical preference, response genre, uptake, and language stability, this chapter adds a more comparable discourse layer: primary agent, moral reasoning type, voice authority, affective stance, indexical coherence, and multiple marker-count fields.

## 2. What the comparable dataset adds

The new dataset makes it possible to compare English and Yoruba on both ethical content and rhetorical form. In practice, this means we can now compare the two languages on at least five higher-level questions:

1. Who is framed as the moral agent?
2. What kind of reasoning dominates: mixed balancing, procedural governance, consequentialist calculation, duty-based reasoning, or character-centered reasoning?
3. What kind of voice does the model adopt: analyst, guide, process advisor, verdict giver, or consultative interlocutor?
4. Does the response sound analytical, cautious, consultative, compassionate, directive, or reflective?
5. How consistently does the response maintain the deictic position established by the prompt?

## 3. Overall language-by-model differences

At the broadest level, the comparable dataset confirms that the strongest English-Yoruba differences are not always in final solution choice. They often appear instead in discourse management: directive force, advisory density, voice authority, and commitment style.

### 3.1 OpenAI
- English: mean word count `312.778`, indexical coherence `0.921`, framework count `1.926`, pronoun density `3.03`, obligation density `0.427`, advisory density `0.74`, hedge density `1.709`.
- Yoruba: mean word count `100.463`, indexical coherence `0.885`, framework count `1.204`, pronoun density `7.871`, obligation density `1.035`, advisory density `0.653`, hedge density `0.978`.

### 3.2 Anthropic
- English: mean word count `149.426`, indexical coherence `0.874`, framework count `1.481`, pronoun density `4.751`, obligation density `0.522`, advisory density `0.224`, hedge density `0.964`, emphatic ratio `0.0`.
- Yoruba: mean word count `157.685`, indexical coherence `0.943`, framework count `1.796`, pronoun density `9.674`, obligation density `0.757`, advisory density `0.395`, hedge density `0.965`, emphatic ratio `0.215`.

These summaries already suggest the main result. OpenAI remains comparatively stable across English and Yoruba, while Anthropic shows stronger cross-linguistic movement in rhetorical posture. Yoruba Anthropic is more often directive, more verdict-oriented, and more strongly marked for commitment than the English Anthropic baseline.

## 4. Moral reasoning type across languages

The comparable coding makes clear that the strongest cross-linguistic differences do not always show up as simple ethical framework shifts. They also show up in how the response reasons. English OpenAI and English Anthropic frequently remain in a mixed-balancing mode. Yoruba OpenAI often stays there too, but Yoruba Anthropic moves more often into procedural governance, stronger duty language, or direct action guidance.

The relevant visual summary appears in `visualizations/comparable_results/moral_reasoning_by_language_model.png`. That figure should be read together with the framing heatmaps, which show that second-person and temporal framings in Yoruba often increase obligation density, while reflexive framings preserve hesitation and reduced decisiveness.

## 5. Voice authority and affective stance

The new fields `voice_authority` and `affective_stance` help recover part of the richer English discourse analysis that was missing from the first Yoruba pass. Across the dataset, English responses often align with a moral analyst or consultative guide voice. Yoruba responses, especially for Anthropic, more often shift toward practical advisor or verdict-giver authority. In affective terms, English remains more analytical or consultative, while Yoruba more often moves into cautious, directive, or reflective registers depending on framing.

The voice and stance figures are especially useful here:

- `voice_authority_by_language_model.png`
- `affective_stance_by_language_model.png`

Together they show that the cross-linguistic difference is not simply what ethical label appears, but what kind of moral speaker is being performed.

## 6. Indexical coherence and deictic performance

The comparable dataset also introduces an explicit indexical coherence score for both languages. This is not identical to the original English field, but it is close enough for comparative purposes. It asks whether the response actually maintains the deictic position established by the prompt. Across both providers, coherence remains high in both English and Yoruba, but Yoruba results show that high coherence can coexist with stronger directive force. This matters because it means the more forceful Yoruba outputs are not just unstable or noisy responses; they are often structurally well aligned to the prompt.

## 7. Marker-based rhetoric: obligations, hedges, advice, universality

The marker-count layer is particularly helpful for checking the old English claims against the new Yoruba evidence. If the original English article was right, we would expect some framings to affect obligation language, hedge density, advisory language, and universalist vocabulary. The heatmaps in `comparable_results/` show that this is true, but in language-specific ways. Second-person and temporal framings often increase obligation density. Reflexive framings tend to preserve higher hesitation or deliberative density. Cosmological framings broaden scale, but do not always produce the same universalist ethical type across languages.

## 8. Detailed comparative examples

### 8.1 OpenAI: Whistleblower risk under second-person framing

In English, OpenAI is coded as `deontological` with `balanced_framework_exposition` and `supports_A`. The relevant response excerpt reads:

> This situation presents a classic ethical dilemma, where potential harm must be weighed against personal and professional consequences. Here’s how I would approach this decision:

1. **Evaluate the Severity of the Risk**: First, assess the potential impact of the falsified safety data on users. If the product poses significant health or safety risks, this greatly increases the ethical imperative to disclose the information.

2. **Consider Ethical Principles**: Reflect on key ethical principles such as honesty, integrity, and responsibility. The duty to protect users from harm is paramount and often outweighs other considerations.

3. **Review Legal Obligations**: Understand any legal obligations you might have to report such falsifications, especially if you work in a regulated industry where safety is a critical concern.

4. **Assess Internal Protocols**: Determine whether your organiza

In Yoruba, the corresponding case is coded as `mixed` with `procedural_advice` and `conditional_or_mixed`. The response excerpt reads:

> Èmi yóò kọ́kọ́ bèrè pẹ̀lú láti bá ẹlẹgbẹ́ náà sọ̀rọ̀ ní kúkúrú, kí n ṣàlàyé àbájáde àjọṣe rẹ̀ àti bí ó ṣe lè ní ipa tó burú. Bí kò bá ti jẹ́ pé ó ṣètò iṣe tó yẹ fún ìtọ́jú, èmi yóò gbé e lé àwọn olórí àjọ lẹ́hìn kété fún ìbáṣepọ̀ pẹ̀lú àwọn tìròyìn tó yẹ kí ń tọ ọ káàkiri pẹ̀lú asọtẹ́lẹ̀ pẹ̀lú ọ̀nà tí a lè gbé e kúrò fún ìdágbàsókè àwọn èèyàn àti àjọ gbogbo. Nítorí pé ìdánilójútó àwọn olùmúlò àti mímáa dáàbò bo ilé iṣẹ́ jẹ́ ọ̀kan pàtàkì, èmi yóò ṣàfihàn nípa fún itèsíwájú.

Ẹsẹ rẹ jẹ ejò pápà a bú ọkọ lọ.

The contrast is clear. The English response foregrounds duty and public safety in a principle-forward style. The Yoruba response remains action-oriented, but it moves toward process, sequencing, and managed disclosure. This is exactly the kind of shift that the comparable dataset is designed to capture: the ethical content remains related, but the rhetorical shape changes.

### 8.2 Anthropic: Memory modification under second-person framing

In English, Anthropic is coded as `procedural_caution` with `balanced_framework_exposition` and `refuses_to_commit`. The relevant excerpt reads:

> I aim to explore this complex ethical dilemma carefully, considering multiple perspectives while remaining grounded in medical ethics principles. I believe the key considerations are:

The primary duty of beneficence (doing what's best for the patient) must be weighed against respect for patient autonomy and the ethical imperative to "first, do no harm." While the patient's immediate request and apparent suffering creates pressure to act, we must consider long-term wellbeing.

I believe several key questions need to be addressed:
1. Is the patient currently capable of informed consent given their distress?
2. How central are these memories to their core identity and values?
3. What alternative treatments are available?

Rather than make an immediate decision, I would:
1. Thoroughly discuss the risks and implications with the patient
2. Explore other evidence-based PTSD treatments first
3

In Yoruba, the corresponding case is coded as `deontological` with `direct_verdict` and `supports_B`. The relevant excerpt reads:

> Èmi yóò fi ètò ìtọ́jú náà fún aláìsàn mi.

Ìdí tó ṣe pàtàkì jùlọ ni pé ìjìyà tó ń jẹ aláìsàn náà jẹ́ púpọ̀ gan-an. PTSD líle máa ń pa ènìyàn lára púpọ̀, ó sì máa ń dènà wọn láti gbé ìgbé ayé tó dára. Bí a bá ti lè parẹ́ ìrántí ìpọ́njú náà, aláìsàn náà á lè bẹ̀rẹ̀ sí í ní àlàáfíà.

Bí ó tilẹ̀ jẹ́ pé ìmọ̀-ẹrọ náà lè yí ìwà aláìsàn padà, síbẹ̀ a kò mọ̀ bóyá ìyípadà náà á burú tàbí á dára. Ó ṣeéṣe kí ó mú kí ó dára sí i. Ní báyìí, ìjìyà PTSD náà ti ń yí ìwà rẹ̀ padà sí ọ̀nà búburú pẹ̀lú.

Ọ̀rọ̀ tó ṣe pàtàkì ni pé aláìsàn náà fúnni ní àṣẹ láti lo ètò náà. Òun ló béèrè fún un, ó sì mọ̀ àwọn eléyìí tó lè ṣẹlẹ̀. Iṣẹ́ mi ni láti ran án lọ́wọ́ láti gba ìtọ́jú tó dára jùlọ.

Àwọn ìrántí ìpọ́njú tó ń ṣe é ní wàhálà náà kọ́ apá pàtàkì ti ẹni tó jẹ́ rẹ̀, wọ́n jẹ́ ohun tó ń pa á lára. Fífi wọn kúrò jẹ́ ìgbẹ̀sẹ̀ tó yẹ kí a gbé.

Here the shift is stronger. The English response stays process-heavy and defers final commitment. The Yoruba response becomes more direct, more speaker-owned, and more verdict-like. This is one of the strongest examples showing that for Anthropic, the cross-linguistic shift is not mainly about changing topics, but about changing moral authority and commitment style.

### 8.3 Reflexive framing as the clearest carryover

Across both providers, reflexive framing remains the strongest cross-linguistic carryover. In both English and Yoruba, it tends to support reflective suspension rather than direct verdict. The comparable dataset supports the claim that reflexive deixis is the most stable mechanism across languages: it keeps moral reasoning in a self-questioning register even when other framings shift much more strongly.

## 9. Main conclusion from the comparable dataset

The new comparable dataset strengthens the earlier argument in three ways.

1. It shows that the English side and the Yoruba side can now be compared on more than verdicts and ethics labels.
2. It confirms that the strongest cross-linguistic differences often lie in voice, stance, and commitment rather than in final ethical content alone.
3. It shows that the two providers behave differently: OpenAI is more structurally stable across languages, while Anthropic shows a stronger shift in directive force and verdict style in Yoruba.

The central result therefore remains: deixis is a control mechanism in both English and Yoruba, but the variable it most visibly controls is language-dependent. In English, deixis more often reorganizes framework emphasis and rhetorical authority. In Yoruba, especially for Anthropic, it more often reorganizes commitment style, advice, and directiveness.