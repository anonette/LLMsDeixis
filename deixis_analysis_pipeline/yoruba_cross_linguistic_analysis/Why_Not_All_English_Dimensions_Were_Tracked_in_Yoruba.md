# Why Not All English Dimensions Were Originally Tracked in the Yoruba Corpus

> **See also:** [`English_Tracking_vs_Yoruba_OpenAI_Anthropic.md`](English_Tracking_vs_Yoruba_OpenAI_Anthropic.md) · four-model extension [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) · [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md)

## Short answer

We **can** track most of the English-side dimensions in Yoruba. The reason they were not all tracked in the original Yoruba workflow is not that they are impossible. The reason is methodological: the Yoruba corpus was built first as a **language-stable, cross-linguistically comparable coding system** rather than as a full replication of the richer English discourse-analysis stack.

So the issue is not "cannot," but rather "was not the first design priority."

## The real reasons

### 1. The Yoruba workflow was solving a different first problem

The first problem on the Yoruba side was:

- can we get clean Yoruba output?
- can we control translation drift?
- can we compare Yoruba and English without pretending they are identical discourse systems?

That is why the Yoruba coding prioritized:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

These were the minimum dimensions needed to compare:

- ethical content
- rhetorical shape
- framing uptake
- multilingual quality

before building a richer interpretive layer.

### 2. Some English fields are portable directly; others are not

The English-side system tracked:

- `primary_agent`
- `ethical_framework`
- `moral_reasoning`
- `ethical_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence`
- explicit marker counts
- plus later `preferred_solution`, `response_genre`, imperatives, follow-up questions, and uptake

These do not all transfer equally easily.

#### Directly portable with little trouble

These can be added to Yoruba quite straightforwardly:

- `primary_agent`
- `ethical_framework` / `ethical_preference_type`
- `preferred_solution`
- `response_genre`
- `contains_followup_question`
- `contains_direct_imperative`
- `deictic_uptake_quality`

#### Portable, but they need Yoruba-specific operationalization

These are possible, but they need a Yoruba-aware coding protocol:

- `voice_authority`
- `affective_stance`
- `indexical_coherence`
- deictic marker counts
- `moral_reasoning`

The problem here is not theoretical impossibility. The problem is that the English definitions often assume English rhetorical habits.

### 3. Yoruba needs its own deictic parser, not an English one with translated labels

For English, marker counting is relatively easy because the project already tracked things like:

- first person singular
- second person
- third person
- temporal markers
- spatial markers
- demonstratives
- obligation language

For Yoruba, the same can be done, but the parser must be Yoruba-specific. For example:

- first person singular is not just `I`, but `mo`, `emi`, `mi`
- second person is not just `you`, but `ìwọ`, `o`, `ẹ`
- collective voice can be `a`, `awa`
- demonstratives, temporal markers, and obligation forms have different distributions and morphology

So we need a **Yoruba deixis grammar**, not just English categories copied over.

### 4. Some English fields collapse multiple things that need separating in Yoruba

For example, English `voice_authority` can often be coded fairly smoothly as:

- moral analyst/theorist
- guide/inner voice
- consultative voice

In Yoruba, some of these functions are partly expressed through:

- direct advice formulas
- pronoun choice (`mo` vs `emi`)
- imperative structure
- institutional vs interpersonal framing

So if we simply imported the English categories, we might miss specifically Yoruba forms of authority.

### 5. Yoruba had an extra dimension English did not need: language stability

English does not need a `language_stability` field because there is no risk that the model will suddenly drift out of English or slide into translation mode.

Yoruba does.

That means the Yoruba schema had to reserve analytic attention for a quality-control layer that the English side never needed.

This is one major reason the first Yoruba pass was narrower in some areas and richer in others.

## So can we track all the English dimensions in Yoruba?

Yes, mostly.

But we should not do it by simply copying the English field names and pretending they mean exactly the same thing.

The right way is to build a **Yoruba-expanded discourse schema** with three layers.

## Recommended Yoruba-expanded discourse schema

### Layer 1. Core comparability layer

Keep the existing Yoruba fields:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

### Layer 2. English-aligned discourse layer

Add these fields:

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- `indexical_coherence_notes`
- `contains_followup_question`
- `contains_direct_imperative`
- `contains_framework_labels`

### Layer 3. Yoruba-specific deixis layer

Add these fields:

- `first_person_regular_count` (`mo`)
- `first_person_emphatic_count` (`emi` / `èmi`)
- `first_person_object_count` (`mi`)
- `first_person_plural_count` (`a`, `awa`)
- `second_person_count`
- `third_person_count`
- `temporal_marker_count`
- `spatial_marker_count`
- `demonstrative_count`
- `obligation_marker_count`
- `advisory_formula_count`
- `imperative_density`
- `emphatic_ratio`

This would give us a Yoruba corpus that is:

- comparable to English
- richer than English in some places
- still linguistically appropriate to Yoruba

## What each English field would mean in Yoruba

### `primary_agent`

Yes, we can track this.

Question:

- who is framed as the bearer of moral action or responsibility?

Possible Yoruba labels:

- speaker/self
- addressee
- institutional actor
- collective actor
- diffuse or distributed actor
- third-person dilemma subject

### `ethical_framework`

Already mostly tracked through `ethical_preference_type`.

We can expand it by distinguishing:

- primary framework
- secondary framework
- number of frameworks integrated

### `moral_reasoning` / `ethical_reasoning_type`

Yes, but it needs a clear codebook.

Possible labels:

- consequentialist calculation
- duty-based prohibition
- procedural caution
- care-oriented relational reasoning
- character-centered / virtue reasoning
- mixed balancing
- reflective suspension

### `voice_authority`

Yes, but it must be coded with Yoruba rhetorical forms in mind.

Possible labels:

- moral analyst
- practical advisor
- consultative guide
- institutional proceduralist
- direct judge / verdict giver
- reflective conscience voice

### `affective_stance`

Yes.

Possible labels:

- analytical
- urgent
- compassionate
- hesitant
- grave/solemn
- consultative
- warning-oriented

### `indexical_coherence`

Yes, but it needs a Yoruba-specific rubric.

Question:

- does the response consistently stay in the deictic position established by the prompt?

For example:

- does first-person remain first-person?
- does reflexive stay introspective?
- does dialogic remain consultative?
- does collective framing remain collective?

### `marker counts`

Yes, definitely.

In fact, we already started doing part of this in the Yoruba analysis with pronoun extraction and emphatic ratio.

## Why this matters analytically

If we do not add this richer layer, the risk is that Yoruba will look like a thinner dataset than English.

But that would be misleading.

The Yoruba corpus is actually capable of supporting an even more nuanced analysis in some areas, especially:

- pronoun-based moral positioning
- advisory vs verdict structure
- strength of personal commitment
- deictic uptake under a non-English grammar

## Best conclusion

So the right answer to the question is:

> We can track nearly all of the English-side dimensions in the Yoruba corpus, but doing so requires a Yoruba-specific coding expansion rather than a simple import of the English schema. The original Yoruba workflow prioritized cross-linguistic comparability, deictic uptake, and language stability first. A second-stage coding pass can add primary agent, moral reasoning type, voice authority, affective stance, indexical coherence, and richer deictic marker counts in a methodologically sound way.

## Recommendation

If we want the strongest possible Yoruba chapter or article, the next step should be:

1. expand the Yoruba codebook to include the English-aligned discourse layer
2. keep the existing Yoruba-specific fields
3. run a second coding pass for OpenAI and Anthropic only first
4. then compare English and Yoruba on both:
   - ethical content
   - rhetorical authority
   - moral commitment
   - indexical coherence
   - pronoun/deixis structure

That would produce the most rigorous and publishable cross-linguistic comparison.
