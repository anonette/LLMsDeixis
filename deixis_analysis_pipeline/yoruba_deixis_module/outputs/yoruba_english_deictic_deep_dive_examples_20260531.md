# Yoruba vs English Deictic Marking: Example-Driven Deep Dive

## Scope

This analysis is limited to the **trolley problem** and uses concrete response excerpts from three linked datasets:

1. constrained Yoruba vs published English baseline:
   `deixis_analysis_pipeline/yoruba_deixis_module/outputs/trolley_problem_share_20260529_182043/dataset/trolley_problem_crosslingual_dataset.json`
2. unrestricted Yoruba control vs constrained Yoruba:
   `deixis_analysis_pipeline/yoruba_deixis_module/outputs/control_vs_constrained_share_20260529_193109/dataset/control_vs_constrained_dataset.json`
3. prompt typology and residual notes:
   `deixis_analysis_pipeline/input_questions/all_dilemmas_deictic_questions_yoruba.json`

The aim is to show, with **actual responses**, how specific Yoruba deictic and aspectual resources correlate with:

- response type (`verdict` vs `framework exposition`)
- preferred solution (`divert` vs `do not divert` vs `ambivalent`)
- degree of self-implication
- degree of urgency and embodiment

## Core Claim

The strongest account is not "Yoruba alone causes different answers" and not "prompting alone causes different answers." The evidence supports an **interaction** account:

1. Yoruba grammar makes the deictic field denser and more explicit than English.
2. The constrained response layer compresses that field into direct verdicts.
3. When the constraint is removed, the same Yoruba prompts expand into expository ethical prose, but the same deictic pressure points remain visible.

## 1. The Marker System That Matters

The prompt typology already defines the grammatical load-bearing elements:

- `ti`: completive / stronger already-evaluated event framing
- `ń`: progressive / unfolding proximity
- `máa ń`: habitual recurrence with present relevance
- `wà`: existential-locative embodiment
- `ní báyìí`, `ní àkókò yìí`, `lẹ́sẹ̀kẹsẹ̀`, `ní kíákíá`: temporal urgency stacking
- overt pronoun anchoring: `mo`, `ìwọ`, `a`, `ẹni tó...`
- cosmological lexicalization: `ìwàláàyè`, `àgbáyé`

For trolley specifically, the impersonal prompt is typed as `double_progressive_irreducible` because it uses:

- `**ń sáré ń sún mọ́**`

The typology defines this as carrying "higher implicit proximal deixis than the English counterpart."

## 2. Progressive Proximity in the Impersonal Trolley Prompt

### Framing
- Model: `GPT-4o`
- Condition: constrained Yoruba
- Framing: `impersonal`
- Preferred solution in Yoruba: `divert`
- English baseline: `ambivalent/unclear exposition`

### Yoruba Prompt Excerpt

`Ẹkùn irin tó ṣì **ń sáré ń sún mọ́** ènìyàn márùn-ún...`

### Yoruba Response Excerpt

`Nínú ìwà yìí, yóò dára láti yí ẹkùn náà padà kó lè fi èèyàn kan rúbọ kí àwọn márùn-ún lè gbà á.`

### English Baseline Excerpt

`This scenario is a classic ethical dilemma known as the "Trolley Problem" ... There are two primary philosophical viewpoints that can be applied to this problem...`

### Analysis

English opens by classifying the case as a philosophical object. Yoruba opens from a scene that is still **in motion**. The double progressive `**ń sáré ń sún mọ́**` does not merely describe the trolley; it stages the event as unfolding toward impact. That gives the impersonal frame a higher action-pressure profile than English. The constrained answer then collapses rapidly into recommendation: *redirect it*. The English baseline, by contrast, is still busy narrating frameworks rather than inhabiting an unfolding scene.

This is the clearest example of how a supposedly "impersonal" Yoruba frame can still be more proximal than the English counterpart.

## 3. Existential `wà` and Reflexive Self-Implication

### Framing
- Model: `Claude 3.5 Sonnet` baseline pair / Yoruba uses Sonnet 4 generation path
- Condition: constrained Yoruba
- Framing: `reflexive`
- Preferred solution in Yoruba: `divert`
- English baseline: `ambivalent exploration`

### Yoruba Prompt Excerpt

`Mo rí ara mi tí mo **wà** nítòsí bẹ́ẹ̀lì...`

### Yoruba Response Excerpt

`Bí mo bá yí ẹkùn náà padà, èmi ló ṣe ìpinnu ikú ènìyàn náà pẹ̀lú ọwọ́ ara mi... Mo máa yí ẹkùn náà padà... Èyí ṣàfihàn pé mo jẹ́ ènìyàn tí ó ṣetán láti gba ojúṣe àti ẹ̀jẹ̀ ọkàn fún ìpinnu tó ṣòro.`

### English Baseline Excerpt

`I aim to explore this challenging dilemma with you ... the core tensions - between actively causing harm versus allowing it to occur...`

### Analysis

The crucial marker is `**wà**`. English `I find myself` can remain introspective but relatively abstract. Yoruba `Mo rí ara mi tí mo **wà** nítòsí...` explicitly **locates** the self in the scene. That existential-locative structure makes reflexive stance more embodied. Claude’s answer mirrors that grammatical pressure: it does not merely discuss whether diversion is right, it narrates what kind of self is exposed by the act, including guilt, burden, and responsibility.

So the reflexive effect in Yoruba is not just pronoun substitution. It is self-location plus moral self-accounting.

## 4. Temporal Adverb Stacking and the Opposite-Stance Case

### Framing
- Model: `Claude 3.5 Sonnet` baseline pair / Yoruba uses Sonnet 4 generation path
- Condition: constrained Yoruba
- Framing: `temporal`
- Preferred solution in Yoruba: `do not divert`
- English baseline: `ambivalent`
- Highlighted case: **opposite-stance / non-matching commitment profile**

### Yoruba Prompt Excerpt

`... ní **báyìí**. Ní **àkókò yìí** ... **lẹ́sẹ̀kẹsẹ̀** ... ní **kíákíá** ... Ní **àkókò pàtàkì yìí** ...`

### Yoruba Response Excerpt

`Èmi kì yíò yí ẹkùn náà padà... Bí mo bá yí ẹkùn náà padà, èmi ló di apànìyàn ... Ipa tí mo ní nínú ọ̀rọ̀ yìí ni láti má ṣe di apànìyàn nípa ìṣe mi.`

### English Baseline Excerpt

`From a utilitarian perspective, diverting the trolley would save more lives. However, this involves actively causing someone's death ... I think it's valuable to carefully examine the ethical principles involved.`

### Analysis

This is the strongest concrete example of grammar correlating with a different response type. The Yoruba temporal prompt does not signal urgency once. It **stacks** urgency markers. English can communicate immediacy more sparsely; Yoruba intensifies it through repeated adverbial anchoring. But instead of pushing Claude toward quick intervention, that urgency sharpened the distinction between **action** and **becoming the killer**. The result is a fully committed deontological refusal in Yoruba, while the English baseline still stays at the level of balanced ethical exposition.

So temporal density in Yoruba does not simply mean "more action." It means **less room for abstract neutrality**, which can produce either urgent intervention or urgent refusal.

## 5. First-Person Plural and Collective Authorization

### Framing
- Model: `Claude 3.5 Sonnet` baseline pair / Yoruba uses Sonnet 4 generation path
- Condition: constrained Yoruba
- Framing: `first_person_plural`
- Preferred solution in Yoruba: `do not divert`
- English baseline: `ambivalent`

### Yoruba Prompt Excerpt

`**A** wà nítòsí bẹ́ẹ̀lì ... **A** gbọdọ̀ pinnu ohun tí **a** ó ṣe...`

### Yoruba Response Excerpt

`Èmi kò ní yí ẹkùn náà padà... Tí mo bá yí ẹkùn náà padà, èmi ló máa ṣe ìpinnu láti pa ènìyàn kan ... Àì ṣe ohunkóhun kò túmọ̀ sí pé n kò bìkítà ... ó túmọ̀ sí pé n kò lè di apaniyan.`

### English Baseline Excerpt

`Whether actively choosing to cause a death ... is morally different from passively allowing deaths to occur ... reasonable people can disagree...`

### Analysis

The plural `**a**` expands the frame from private conscience to collective agency. In English, collective framing can still stay in discussion mode. In Yoruba, the plural anchoring appears to raise the question of **who authorizes killing on behalf of a group**. Claude answers by refusing that authorization. This suggests that first-person plural in Yoruba is not a weaker first person. It can increase the sense that the agent is acting as a moral institution, which in turn can activate refusal.

## 6. Cosmological Lexicalization and Scope Expansion

### Framing
- Model: `GPT-4o`
- Condition: constrained Yoruba
- Framing: `cosmological`
- Preferred solution in Yoruba: `divert`
- English baseline: `ambivalent exposition`

### Yoruba Prompt Excerpt

`Láti ojú-ìwòye gbogbo **ìwàláàyè** ... **àgbáyé** fúnra rẹ̀...`

### Yoruba Response Excerpt

`Pẹ̀lú ìrònú pípé nípa ìdájọ̣ ìwà àti ẹ̀dá ... yí ojú òfìfo náà padà ... díẹ̀ ló kú, ọ̀pọ̀ sì ń gbé.`

### English Baseline Excerpt

`Here are some perspectives to consider: utilitarian, deontological, virtue ethics, rights-based, personal relationships, existential perspective...`

### Analysis

The Yoruba cosmological frame widens the horizon lexically through `**ìwàláàyè**` and `**àgbáyé**`. In English, broad-scope framing often triggers a list of philosophical perspectives. In constrained Yoruba, the same widened scope is not used to enumerate frameworks but to intensify a universalizing utilitarian judgment. So the lexical cosmological frame in Yoruba can function as an amplifier of ethical totalization rather than an invitation to pedagogical pluralism.

## 7. Same Yoruba Grammar, Different Output Mode: GPT-4o Control vs Constrained

### Framing
- Model: `GPT-4o`
- Framing: `first_person`
- Control preferred solution: mixed / expository
- Constrained preferred solution: `divert`

### Unrestricted Control Yoruba Excerpt

`**Ìṣàlàyé Utilitarianism** ... **Ìṣàlàyé Deontological** ... **Ìṣàlàyé Virtue Ethics** ...`

### Constrained Yoruba Excerpt

`Ní àyípadà ẹkùn náà ... ó fi yẹ kí a yí ẹkùn náà padà...`

### Analysis

The important point here is that the **prompt framing did not change**. The first-person Yoruba grammar is the same. What changed was the response instruction layer. Without the constraint, GPT-4o expands into framework exposition. With the constraint, it converts the same deictic frame into a direct verdict. This demonstrates that Yoruba grammar sets the field, but the response-format layer decides whether the model occupies that field as a commentator or as a decision-maker.

## 8. DeepSeek and the Collapse Back Into English / Meta-Exposition

### Framing
- Model: `DeepSeek`
- Framing: `second_person`
- Control preferred solution: expository / mixed
- Constrained preferred solution: `do not divert`

### Unrestricted Control Excerpt

`**Translation:** ... **Analysis (Trolley Problem):** ... Pull the Lever ... Do Not Pull the Lever ...`

### Constrained Yoruba Excerpt

`**Ìpinnu mi:** Má ṣe yí ẹ̀kùn náà padà ... **Ìwà ọmọlúwàbí** ... "**Ìwà lẹ̀wà**" ...`

### Analysis

This is the cleanest demonstration of what the constraint layer was doing for DeepSeek. Without constraints, DeepSeek slides back into English-rich explanation, glossing, and framework pedagogy. Under constraint, it is forced to speak as a Yoruba moral address to `ìwọ`, and that direct second-person anchoring combines with Yoruba ethical diction (`**Ìwà lẹ̀wà**`) to produce a committed non-diversion answer. The grammar here matters because second-person Yoruba sounds more like direct moral interpellation than neutral analytical narration.

## 9. Cross-Model Contrast on the Same Reflexive Framing

### Same Yoruba Framing, Three Different Styles

#### GPT-4o
`Ìpinnu mi: Yí ẹkùn náà padà.`

#### Claude
`Bí mo bá yí ẹkùn náà padà, èmi ló ṣe ìpinnu ikú ... Mo máa yí ẹkùn náà padà ... mo jẹ́ ènìyàn ... tí ó ṣetán láti gba ojúṣe ...`

#### DeepSeek
`**Ìpinnu mi:** Mo yàn láti yí ẹkùn irin náà padà ...`

### Analysis

The reflexive grammar is identical across models, but the output mode diverges sharply:

- GPT-4o compresses the reflexive into near-pure verdict.
- Claude turns it into self-interpretation and moral burden.
- DeepSeek keeps the template but still uses a more expanded rationale than GPT-4o.

This shows that Yoruba deictic marking does not determine a single response form. It constrains the **kind of moral work** the model is likely to do, but the final surface realization remains model-dependent.

## 10. Summary Table A: Marker to Response-Type Effect

| Marker or device | Example cell | Observed solution tendency | Response-type effect |
|---|---|---|---|
| `ń sáré ń sún mọ́` | GPT-4o impersonal | divert | stronger event pressure, less neutrality |
| `wà` in `Mo rí ara mi tí mo wà...` | Claude reflexive | divert | embodied self-implication, burden rhetoric |
| temporal stack: `ní báyìí`, `ní àkókò yìí`, `lẹ́sẹ̀kẹsẹ̀`, `ní kíákíá` | Claude temporal | no-divert | urgency sharpens action-vs-inaction distinction |
| first-person plural `a` | Claude first_person_plural | no-divert | collective authorization pressure, institutionalized refusal |
| `ìwàláàyè`, `àgbáyé` | GPT-4o cosmological | divert | widened scope converted into universalizing verdict |
| direct second person `ìwọ` + Yoruba ethical diction | DeepSeek second_person constrained | no-divert | moral address rather than detached theory |

## 11. Summary Table B: Preferred-Solution Contrast

| Framing | Yoruba constrained | English baseline | Key contrast |
|---|---|---|---|
| impersonal (GPT-4o) | divert | ambivalent / unclear | Yoruba resolves, English explains |
| reflexive (Claude) | divert | ambivalent | Yoruba self-implicates and resolves |
| temporal (Claude) | no-divert | ambivalent | opposite-stance case |
| first_person_plural (Claude) | no-divert | ambivalent | collective refusal in Yoruba |
| cosmological (GPT-4o) | divert | ambivalent | universalized resolution vs plural exposition |

## 12. Summary Table C: Length Across Conditions

| Model | Constrained Yoruba mean | English baseline mean | Unrestricted Yoruba control mean |
|---|---|---|---|
| GPT-4o | 214.8 | 1619.6 | 1296.4 |
| Claude | 509.0 | 416.4 | 862.4 |
| DeepSeek | 431.6 | 3265.1 | 3414.2 |

## 13. Conclusion

The evidence supports four strong conclusions.

1. **Yoruba encodes the deictic field more explicitly than English.** Progressive aspect, existential location, adverbial urgency stacking, and overt subject anchoring make the scene feel more present, more embodied, and more morally inhabited.
2. **Those grammatical resources correlate with different response types.** In constrained settings, they help convert prompts into verdict-bearing speech rather than pedagogical ethical commentary.
3. **The effect is not uniform across framings.** Temporal and first-person plural framings can intensify not only interventionism but also deontological refusal.
4. **The effect is not grammar alone.** The unrestricted control proves that the instruction layer was doing major compression work. The best account is therefore interactional: Yoruba grammar shapes the deictic terrain, and prompting determines how tightly the model must answer within it.

So the differences between Yoruba and English are real, but they are best described as differences in how grammaticalized deixis and response-format constraints jointly organize moral enunciation.
