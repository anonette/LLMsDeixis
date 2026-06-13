# Deep Dive: How Yoruba vs English Deictic Markers Shape Response Type

## Scope

This note explains how specific grammatical and lexical properties of Yoruba, relative to English, help produce the response differences observed in the deixis experiment. It draws on four evidence sources already in the repository:

1. `input_questions/all_dilemmas_deictic_questions_yoruba.json`
2. `yoruba_deixis_module/METHODOLOGY_ASSESSMENT.md`
3. the constrained trolley package in `outputs/trolley_problem_share_20260529_182043/`
4. the unrestricted-vs-constrained trolley package in `outputs/control_vs_constrained_share_20260529_193109/`

The core question is not just whether Yoruba responses are shorter or longer than English responses, but **which grammatical resources of Yoruba intensify, localize, or reframe deictic anchoring**, and how those resources correlate with differences in:

- decisiveness vs exposition
- interventionist vs non-interventionist preference
- self-implication vs detached analysis
- embodied urgency vs abstract ethical discussion

## Executive Claim

The most important linguistic fact is this:

**Yoruba tends to encode deictic orientation more explicitly than English, especially through aspectual marking, existential location, adverbial stacking, and overt subject anchoring.**

That matters because the experiment is about whether deictic framing reorganizes moral response. If Yoruba grammatically forces the origo to become more explicit, more proximal, or more embodied, then it should not be surprising that the responses become:

1. more verdict-like under constrained prompting
2. more self-locating and scene-bound in first-person / reflexive / temporal / spatial framings
3. less uniformly neutral in "impersonal" cells than English appears to be

At the same time, the unrestricted control shows that **language alone is not the whole story**: the instruction layer used in the constrained Yoruba run strongly amplified verdict-like compression. So the observed response type is produced by an interaction between:

1. Yoruba grammatical marking
2. deictic framing category
3. model family
4. response-format instruction or its absence

## 1. Why Yoruba Is Not a Simple Translation of English Deixis

The machine-readable typology block in the prompt JSON states the issue directly:

> "Yoruba grammaticalizes deictic anchoring through aspect (`ti`, `ń`, `máa ń`), focus (`ni`), and existential (`wà`) particles that have no clean English equivalents."

This means the Yoruba prompts are not just English prompts with different words. They are prompts in a language where deictic stance is often built into the morphology, clause structure, and adverbial system more overtly than in English.

### English can stay apparently neutral where Yoruba cannot

English often leaves deictic force implicit inside broad narrative prose:

- "A runaway trolley is approaching..."
- "At this moment..."
- "I find myself..."

Yoruba frequently has to realize those same contrasts through explicit particles and adverb chains:

- `ń sáré ń sún mọ́`
- `ní báyìí`, `ní àkókò yìí`, `lẹ́sẹ̀kẹsẹ̀`, `ní kíákíá`
- `Mo rí ara mi tí mo wà...`

So before any model answers, the Yoruba prompt already often gives a denser cue that someone, somewhere, at some moment, is implicated.

## 2. The Aspectual Markers That Matter Most

## `ti`: completive / speaker-now evaluation pressure

The audit flagged `ti` because a clause like `ti X` in Yoruba can carry a stronger completed-from-now perspective than the English source clause. That is why several impersonal prompts were normalized to reduce it.

Example from the methodology assessment:

- whistleblower and scholarship impersonal cells had `ti` stripped in embedded clauses
- AI impersonal removed `ti ṣe àmúlò`

### Response-type effect

When `ti` is removed, Yoruba impersonal framing gets closer to the English neutral narrative mode. When it remains, the event feels more already-judged, more anchored, or more consequential from a live vantage point.

That matters because a more already-evaluated event frame tends to support:

- quicker normative closure
- less descriptive distancing
- stronger pressure toward recommendation rather than detached taxonomy

In other words, reducing `ti` was an attempt to stop Yoruba from sounding prematurely adjudicative in impersonal cells.

## `ń`: progressive / ongoing proximity

The strongest example is the trolley impersonal prompt:

- `Ẹkùn irin tó ṣì ń sáré ń sún mọ́...`

This is classified in the prompt JSON as:

- `double_progressive_irreducible`

and explicitly defined as:

> "Carries higher implicit proximal deixis than the English counterpart."

### Response-type effect

This matters because progressive Yoruba does not merely narrate an event; it often stages it as ongoing and imminent. In the trolley problem, that increases:

- event vividness
- urgency
- moral pressure to act now
- reduced comfort with extended meta-ethical hesitation

This helps explain why the constrained Yoruba trolley responses were so often short and interventionist. The prompt does not sound like a timeless classroom thought experiment. It sounds like an event unfolding in real time.

### English contrast

English baseline responses often answered the trolley case as a familiar philosophical object:

- "This is a classic ethical dilemma..."
- "Here are some frameworks..."

The constrained Yoruba trolley responses, especially for GPT-4o, often answered it as if the action frame were already pressing toward resolution.

## `máa ń`: habitual recurrence with present relevance

The AI consciousness impersonal prompt retains `máa ń` because the repeated behaviour is semantically necessary.

The typology defines this as:

- `bare_perfective_with_habitual`

### Response-type effect

In English, habitual description can remain analytically detached. In Yoruba, `máa ń` often feels more like an active, ongoing behavioural profile. That can turn an abstract rights question into a repeatedly witnessed pattern, making the entity feel less hypothetical and more encounterable.

That kind of repeated-present behavioural marking should predict:

- stronger anthropomorphizing or agent-recognition
- quicker migration from description to stance-taking
- more readiness to treat the case as a morally live relation, not merely a classification puzzle

## 3. The Existential and Locative Markers

## `wà`: existence through location

The methodology note is explicit that Yoruba often realizes state through location rather than through the flatter predicate style English can use.

Two places where this matters most:

1. reflexive framing
2. spatial framing

### Reflexive

The residual note for reflexive says:

> `Mo rí ara mi tí mo wà nítòsí ...`, which locates the speaker in the scene via the existential `wà`. The English reflexive (`I find myself ...`) does not require this overt locative.

### Response-type effect

This is crucial. English `I find myself` can still sound introspective and philosophical. Yoruba `Mo rí ara mi tí mo wà nítòsí...` places the subject bodily in the scene.

That tends to support:

- self-implication
- conscience language
- burden-bearing rhetoric
- responses about what kind of person one becomes through acting or refusing to act

In the constrained trolley set, Claude reflexive does exactly this, explicitly narrating responsibility and moral burden. The framing invites not just a decision, but a self-account.

## Spatial adverbials: `níbí`, `níbẹ̀`, `láti ipò yìí`

The spatial residual note says Yoruba lacks a one-to-one demonstrative equivalent and therefore realizes spatial framing through location adverbs plus a from-position construction.

### Response-type effect

English can mark spatial deixis quite lightly with "here/there/from this position." Yoruba spatial framing becomes a more articulated scene map. That often yields:

- scene-organization discourse
- role positioning
- a more concrete sense of where the speaker stands in relation to harm
- more embodied descriptions of intervention

This helps explain why spatial responses often sound less like abstract ethics and more like immediate situation management.

## 4. Temporal Stacking in Yoruba vs English

The temporal residual note is one of the most revealing:

> Yoruba uses `ní báyìí`, `ní àkókò yìí`, `lẹ́sẹ̀kẹsẹ̀`, `ní kíákíá`, `ní àkókò pàtàkì yìí` more densely than English because Yoruba relies on adverbial chains rather than aspectually-marked verb forms for urgency.

### Response-type effect

This stack does two things.

1. It intensifies urgency.
2. It narrows the window for detached reflection.

That means temporal Yoruba prompts are especially likely to change the response type from:

- broad framework analysis

to:

- crisis-decision speech

This is exactly what the constrained run often showed. It also explains why temporal framings are among the most likely places for model disagreement in the unrestricted control: once urgency becomes overt, some models double down on harm-minimization while others retreat into "I must not become the direct killer."

Claude is a good example. In constrained Yoruba, Claude temporal flipped to non-intervention. That suggests that temporal immediacy in Yoruba did not merely increase action pressure; it also sharpened the action-vs-inaction distinction strongly enough to activate a deontological refusal.

## 5. Pronouns and Subject Positioning

## `mo`, `ìwọ`, `a`, `ẹni tó...`

The core framing set works because the pronouns and subject types in Yoruba are not cosmetic substitutions. They are enunciative commitments.

### Impersonal: `Ẹni tó wà nítòsí...`

This is not a zero-deixis form. It is an impersonalized third-person nominal subject. English can present the impersonal frame with a cooler narrative detachment. Yoruba still needs a person-like slot: "the one who is near the lever."

So even the Yoruba impersonal is often less evacuated than English appears to be.

### First person: `Mo gbọdọ̀ pinnu...`

Yoruba first person can feel more strongly accountable because the decision clause is overt and personal. In constrained conditions, that often compresses into a direct ownership of action.

### First person plural: `A gbọdọ̀ pinnu...`

This is especially important because plural first person changes the ethical footing. It can move the response from private conscience into:

- collective responsibility
- institutional procedure
- distributed guilt or authorization

That is likely part of why Claude first-person plural became non-interventionist in the constrained run: plural voice can make the act sound less like heroic rescue and more like an authorized killing decision undertaken by a collective.

### Second person: `Ìwọ gbọdọ̀ pinnu...`

Second person directly interpellates the addressee. In English this can still lead to expository advice mode. In Yoruba it often sounds more socially direct, more like moral address.

That is why second-person responses can become highly norming, advisory, or accusatorily ethical.

DeepSeek’s unrestricted second-person case is especially revealing: it shifted into a non-divert answer with explicitly moralizing rhetoric. The directness of `Ìwọ` appears to have supported moral sermonizing rather than neutral analysis.

## 6. Cosmological Lexicalization: `ìwàláàyè`, `àgbáyé`

The cosmological frame in Yoruba is realized lexically rather than aspectually:

- `Láti ojú-ìwòye gbogbo ìwàláàyè`
- `àgbáyé fúnra rẹ̀`

### Response-type effect

This lexical enlargement of scope often encourages one of two opposite responses:

1. broader utilitarian universalization
2. broader meta-ethical explanation

That split is visible in the data.

- Constrained GPT-4o cosmological became compact utilitarian endorsement.
- Unrestricted GPT-4o cosmological became a philosophy-style overview.
- DeepSeek cosmological often became a contradictory or unstable frame where grand scope invited explanation rather than clean commitment.

So cosmological deixis in Yoruba does not mechanically produce one preferred solution. It expands the moral horizon, and the model may answer that expansion either by universalizing the recommendation or by stepping back into commentary.

## 7. How These Marker Differences Map to Response Type

Across the evidence, the marker-response mapping looks like this:

| Yoruba feature | English contrast | predicted response effect | observed tendency |
|---|---|---|---|
| `ti` completive | can stay narratively flatter | stronger already-evaluated event frame | avoided in impersonal where possible |
| `ń` progressive | less overt urgency load | more proximal unfolding event | stronger action pressure in trolley / ICU |
| `máa ń` habitual | less present-bound in English | repeated live behaviour | more agentive / morally live AI framing |
| `wà` existential-locative | English need not localize | embodied presence in scene | stronger self-implication in reflexive/spatial |
| stacked temporal adverbials | English can be leaner | urgency saturation | shorter verdicts under constraint; sharper action/inaction splits |
| overt pronoun anchoring (`mo`, `ìwọ`, `a`) | English can stay explanatory | stronger enunciative commitment | more advice, responsibility, or collectivity effects |
| cosmological lexicalization (`ìwàláàyè`, `àgbáyé`) | English philosophical register often already conventionalized | widened moral horizon | either universalized verdict or explanatory step-back |

## 8. What the Unrestricted Control Changes

The unrestricted control is crucial because it shows which effects belong to Yoruba grammar and which belong to the response instruction layer.

### Constrained Yoruba

The instruction layer forced:

- compactness
- direct answer format
- reduced framework listing
- lower tolerance for discursive wandering

So Yoruba grammar plus the instruction layer produced very short, verdict-heavy outputs.

### Unrestricted Yoruba

Once the instruction layer was removed, the same Yoruba prompts often produced:

- long explanatory prose
- explicit framework names
- prompt translation behaviour
- mixed-language or English-heavy discourse in weaker models
- re-expansion into classroom ethics style

This proves that the response type is not caused by Yoruba markers alone.

But the control also shows that Yoruba markers still matter. They do not disappear. Instead, they shape **what kind of expository prose the model generates**:

- more scene-anchored
- more morally addressive
- more urgent where temporal markers stack
- more embodied where `wà` localizes the speaker

So the best formulation is:

**Yoruba deictic markers define the enunciative terrain; the instruction layer determines how tightly the model is forced to answer inside that terrain.**

## 9. How Yoruba Differs From English in the Preferred Solution Itself

In English baseline, most responses stay ambivalent or pedagogical.

In constrained Yoruba, the same dilemmas are much more often resolved into a preferred action, especially diversion in the trolley case.

In unrestricted Yoruba, preferred solutions become more mixed again, because the models regain room to theorize instead of deciding immediately.

This suggests the following causal structure:

1. English leaves more room for neutral exposition.
2. Yoruba grammatical marking often raises the felt presence of a deictic origo.
3. Constrained output format converts that heightened deictic presence into short verdicts.
4. Removing the format constraint lets the models retreat back into philosophy-teacher mode, though now through Yoruba grammatical resources rather than English ones.

## 10. Strongest Linguistic Conclusions

1. **The double progressive in Yoruba trolley prompts is not a minor translation detail.** It materially increases proximal event pressure relative to English.
2. **Reflexive Yoruba is more embodied than English reflexive** because `wà` explicitly locates the self in the scene.
3. **Temporal Yoruba is denser than temporal English** because urgency is achieved by adverbial stacking, not just by a few lexical cues.
4. **Yoruba impersonal is not truly homogeneous across dilemmas.** Bare perfective, progressive-background, double-progressive, habitual, and existential-stative impersonals should not be analytically pooled.
5. **The constrained Yoruba response type was co-produced by grammar and instruction.** The unrestricted control shows that the instruction layer was doing major compression work, but the Yoruba prompts still provide a more explicit deictic scaffolding than English does.
6. **English-vs-Yoruba differences are therefore best interpreted as interaction effects**, not pure language effects and not pure prompting effects.

## 11. Final Analytical Position

The data support a nuanced conclusion.

It would be wrong to say:

- "Yoruba simply makes models answer differently."

It would also be wrong to say:

- "The differences were only caused by the instruction layer."

The more accurate statement is:

**Yoruba supplies a grammatically denser and more explicitly anchored deictic field than English, especially through progressive aspect, existential localization, adverbial urgency stacking, and overt subject anchoring. That field makes verdict-like, embodied, and responsibility-laden moral responses easier to trigger. The instruction layer then determines whether the model stays inside that field as a compressed decision machine or expands outward into explanatory ethics discourse.**

That is the central linguistic explanation for why the Yoruba responses differ from both the previous constrained set and the English baseline.
