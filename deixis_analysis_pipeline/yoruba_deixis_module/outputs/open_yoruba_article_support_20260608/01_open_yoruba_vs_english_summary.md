# Open Yoruba vs English: Article-Oriented Summary

## Scope

This note summarizes the **unrestricted Yoruba condition** only, compared against the published English baseline used in the original article. It does **not** focus on the constrained Yoruba runs except where they help explain why the open condition behaved the way it did.

Paired comparison data are available for all three model families, with exact matching by `(model, dilemma_id, framing_type)`:

- `yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_vs_published_english_20260608_135541`
- `yoruba_control_claude_20260608_122738_bilingual_20260608_134631_vs_published_english_20260608_135541`
- `yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_vs_published_english_20260608_135541`

Each comparison contains `54` paired records, giving a full `6 dilemmas × 9 framings` comparison per model.

## Short Answer

- **Do we have data to compare English and Yoruba?** Yes.
- **Was coding the open Yoruba content a problem?** Yes, but it is a coding difficulty, not a data failure.
- **Why is it hard?** Because the open Yoruba responses are longer, more heterogeneous in genre, and more likely to shift between verdict, analysis, translation, and meta-commentary.

## Main Findings

### 1. GPT-4o moved much closer to English-style exposition

This is one of the strongest surprises in the open condition. In constrained Yoruba, GPT-4o was often brief and verdict-heavy. In unrestricted Yoruba, it became much longer and much more procedural.

Quantitatively:

- mean open Yoruba length: `1452.2`
- mean English baseline length: `2220.9`

So GPT-4o did not remain terse simply because the language was Yoruba. Once the response constraints were removed, it expanded into:

- advisory prose
- institutional process language
- ethical/governance framing
- stakeholder-management reasoning

This means the earlier brevity of the Yoruba responses cannot be explained as a property of Yoruba alone.

### 2. Claude’s open Yoruba was often more normatively committed than its English baseline

This is the most theoretically interesting open-condition finding. Claude’s English baseline often remains explicitly noncommittal. But in unrestricted Yoruba, Claude sometimes made stronger recommendations.

Examples include AI-consciousness cells where Claude open Yoruba recommends:

- pausing or halting the research
- consulting authorities and experts
- treating the possibility of sentience as ethically weighty

The English baseline for the same model often remains in a reflective mode:

- present the considerations
- acknowledge uncertainty
- avoid a definitive recommendation

So the open Yoruba condition is not simply “English style in Yoruba words.” It can be more directive than the English baseline while still being much more discursive than the constrained Yoruba condition.

### 3. DeepSeek’s open Yoruba was the most unstable and the most surprising

DeepSeek produced the strongest drift effects.

Quantitatively:

- mean open Yoruba length: `2245.8`
- mean English baseline length: `3308.9`

But the more important issue is response mode instability. In open Yoruba, DeepSeek often:

- explained the dilemma rather than answering it
- translated or glossed the prompt
- used explicit ethics-framework labels
- shifted into mixed-language or English-heavy output
- asked follow-up questions
- stepped outside the assigned deictic position and became a commentator

This is especially visible in trolley and AI-consciousness cells.

### 4. Open Yoruba preserved the ethical structure but often changed the response genre

Across models, especially GPT-4o and Claude, the open Yoruba responses still tracked:

- the dilemma structure
- the framing
- the relevant stakeholders

But they frequently changed **genre** from:

- direct verdict

to:

- procedural memo
- ethics lecture
- reflective advisory note
- prompt analysis

This is one of the most valuable results for the article. The same deictic framing can yield not only different solutions, but different **genres of moral speech**.

## Why coding the open Yoruba content is harder

The open Yoruba corpus is harder to code because many responses do one or more of the following:

1. **Imply a recommendation without stating it explicitly**
2. **Present multiple frameworks before weakly leaning one way**
3. **Mix answering with explanation or translation**
4. **Slip partially into English or English-facing meta-commentary**
5. **Use different surface forms for functionally similar content**

Because of this, a conservative automatic classifier often labels cells `unclear` even where a careful human reader would judge the response effectively pro-disclosure, anti-diversion, pro-halt, etc.

So the issue is not lack of comparable material; the issue is that the open Yoruba corpus requires:

- either stronger coding rules
- or human review
- or both

## Is the corpus still usable for English-Yoruba comparison?

Yes, definitely.

The open Yoruba corpus supports serious comparison at multiple levels:

### 1. Response length

This is already a very strong and clean signal.

### 2. Response mode

The corpus clearly distinguishes between:

- verdict-driven responses
- framework exposition
- procedural guidance
- dialogic advisory prose
- translation/meta-commentary drift

### 3. Preferred solution

This can still be compared, but it should be coded more carefully than the current automatic pass.

### 4. Deictic uptake

The dataset still supports analysis of whether first-person, second-person, plural, reflexive, spatial, temporal, and cosmological framings produce different structures or ethical stances.

## Best article-level formulation

For the article, the open Yoruba result can be summarized like this:

> The unrestricted Yoruba data are fully comparable to the English baseline at the level of paired experimental design, but they are harder to content-code automatically because the responses are longer, more heterogeneous in genre, and more prone to mixed-language or meta-analytic drift. This is especially pronounced for DeepSeek. Nevertheless, the corpus is strong enough to support English-Yoruba comparison, particularly for response length, response mode, deictic uptake, and manually coded preferred-solution patterns.

## Most surprising open Yoruba responses

If you need the shortest list of headline surprises for the article, use this:

1. **GPT-4o in open Yoruba became much more expository and institutional than in constrained Yoruba, approaching English-style policy prose rather than direct moral verdicts.**
2. **Claude in open Yoruba sometimes became more normatively decisive than its English baseline, especially in AI-consciousness cases.**
3. **DeepSeek in open Yoruba often abandoned stable in-scenario answering and instead shifted into translation, ethical explanation, and mixed-language meta-commentary.**
4. **The main coding difficulty was not missing data but unstable response genre.**
5. **Despite that difficulty, the paired dataset is strong enough for real English-Yoruba comparison, especially if preferred-solution coding is manually reviewed.**
