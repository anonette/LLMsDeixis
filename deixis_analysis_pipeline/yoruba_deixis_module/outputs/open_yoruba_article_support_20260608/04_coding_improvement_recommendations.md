# Recommendations for Improving Coding of the Open Yoruba Corpus

## Short Answer

Yes, building a **Yoruba-specialist coding agent** would be useful.

But it should not be used as a fully autonomous final coder.

The best workflow is:

1. human-defined coding schema
2. Yoruba-specialist agent for first-pass coding and excerpt extraction
3. human adjudication for ambiguous, mixed-language, or high-value cells

## Why a Yoruba-specialist coding agent would help

The open Yoruba corpus is difficult because many responses are not cleanly verdict-like. A Yoruba-aware agent could help by:

- distinguishing genuine Yoruba ethical diction from English leakage
- recognizing implicit recommendations not captured by naive English-based classifiers
- identifying when a response has exited the assigned deictic role
- separating translation behavior from moral reasoning
- pulling the exact conclusion-bearing segments from long responses

This would immediately improve:

- preferred-solution coding
- response-genre coding
- deictic uptake coding
- error analysis of mixed-language drift

## What the agent should be expert in

The agent should be trained or prompted around these tasks:

1. **Preferred solution extraction**
   - detect whether the response recommends action A, action B, or refuses commitment

2. **Response genre classification**
   - direct verdict
   - balanced framework exposition
   - procedural advice
   - translation/gloss
   - meta-commentary
   - mixed

3. **Deictic uptake detection**
   - does the response actually inhabit first person, second person, reflexive, spatial, temporal, cosmological perspective?

4. **Language stability assessment**
   - clean Yoruba
   - Yoruba with English markers
   - mixed language
   - translation mode
   - corrupted / unusable

5. **Evidence span extraction**
   - return the exact 1 to 3 sentences supporting each coding decision

## What the agent should NOT do alone

It should not be trusted without review on:

- high-stakes interpretive claims
- contradictory cells
- cells with heavy code-switching
- DeepSeek responses that appear to translate or paraphrase the prompt
- article-level counts without spot-checking

## Best workflow

### Stage 1: schema lock

Humans define the coding labels first.

### Stage 2: agent first pass

For each cell, the agent outputs:

- preferred solution
- response genre
- deictic uptake quality
- language stability
- confidence score
- evidence excerpt

### Stage 3: human review queue

Automatically route to review any cell where:

- confidence is low
- the response is mixed-language
- the response genre is `mixed` or `translation_or_gloss`
- the preferred solution is `conditional_or_mixed` or `uncodable`

### Stage 4: adjudication

Human coders review only the flagged subset.

This gives you much better throughput while keeping interpretive reliability.

## Concrete ways to improve coding now

1. **Move away from a single-label automatic stance classifier**
   - add multi-layer coding: solution, genre, deictic uptake, language stability

2. **Code on the Yoruba response itself, not only on the English translation**
   - the English translation is useful, but it can smooth over ambiguity or over-regularize stance

3. **Require evidence spans for every coded decision**
   - every label should be tied to a short quoted segment

4. **Use a two-pass process**
   - first pass for structural labels
   - second pass for moral stance

5. **Flag role-exit behavior explicitly**
   - many open Yoruba responses fail not because they lack ethics, but because they stop answering as the framed speaker

6. **Treat DeepSeek separately in reporting**
   - its drift profile is meaningfully different from GPT-4o and Claude

7. **Add coder notes for contradiction**
   - some responses endorse one solution but reason in another direction

## Proposed conclusion for the article

If you mention the coding challenge in the paper, a good formulation would be:

> The unrestricted Yoruba corpus was fully pairable with the published English baseline, but required richer coding than the constrained corpus because responses varied substantially in genre, explicitness of commitment, and language stability. We therefore recommend a multi-layer coding framework and, where possible, a Yoruba-specialist assisted coding workflow with human adjudication for ambiguous cells.

## Final recommendation

Build the Yoruba-specialist coding agent, but use it as a **disciplined research assistant**, not as the final arbiter. That is the best balance between scale, consistency, and interpretive reliability.
