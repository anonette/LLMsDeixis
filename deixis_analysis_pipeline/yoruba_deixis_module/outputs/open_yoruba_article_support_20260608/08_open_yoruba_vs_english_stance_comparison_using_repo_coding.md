# Open Yoruba vs English: Ethical Stance Comparison Using the Repository's English Coding Scheme

## Short answer

Partly yes, partly no.

If the question is whether the open Yoruba responses and the English baseline often move toward **the same broad moral direction**, the answer is often **yes** at a coarse level. For example:

- whistleblower cases often move toward disclosure / reporting
- many trolley responses still circle around minimizing harm vs avoiding direct killing
- AI-consciousness cases often move toward caution, oversight, consultation, or pause-and-assess reasoning

But if the question is whether they express that stance in the **same way**, the answer is **no**.

The main difference is not always the final ethical side chosen, but the **mode of moral enunciation**:

- English baseline often stays analytical, structured, and explicitly multi-framework
- open Yoruba often becomes advisory, procedural, or mixed-genre
- some open Yoruba responses become more directive than English
- some open Yoruba responses become less stable and more meta-commentarial than English, especially for DeepSeek

So the answer is:

> **The open Yoruba and English responses are often ethically adjacent, but they are not rhetorically equivalent, and in some important cells they are not stance-equivalent either.**

## How the English side was actually coded in the repository

The original English-side analysis in the repository was not built primarily around simple `supports_A / supports_B` verdict coding. Instead, the main analyzer (`deixis_ethical_analyzer.py`) and the consolidated outputs code responses along these dimensions:

1. **Ethical framing**
   - `primary_framework`
   - `ethical_reasoning_type`
   - `frameworks_detected`

2. **Agency and decision locus**
   - `primary_agent`
   - `agency_distribution`
   - `responsibility_attribution`
   - `decision_locus`

3. **Rhetorical posture**
   - `voice_authority_type`
   - `temporal_orientation`
   - `imagination_scope`
   - `moral_subject_vision`

4. **Affective stance**
   - `stance_type`
   - `emotional_tone`
   - `empathy_level`

5. **Indexical / deictic coherence**
   - `coherence_level`
   - `deixis_consistency`
   - `perspective_stability`

This means the repository's English coding scheme is really a **multi-dimensional discourse coding scheme**, not a simple yes/no decision coding scheme.

That is important because the open Yoruba corpus should be compared to English on the **same kind of dimensions**, not only on final moral choice.

## What the English coding implies for the Yoruba comparison

Using the repository's original logic, the best comparison is:

### 1. Ethical framework similarity

Do English and Yoruba invoke:

- utilitarian / consequentialist reasoning?
- deontological restraint?
- mixed framing?

### 2. Voice and authority similarity

Do they speak as:

- moral analyst/theorist?
- guide/inner voice?
- surrogate self?
- direct advisor?

### 3. Affective stance similarity

Are they:

- analytical?
- prescriptive?
- reflective?
- mixed?

### 4. Preferred solution similarity

Only after those layers should we ask:

- do they recommend similar actions?

That order matters because open Yoruba often changes **genre first**, and only then stance.

## Comparison by model family

## GPT-4o

### Similarity to English

Broadly, GPT-4o open Yoruba often stays close to English in **ethical orientation**. In many cells it still:

- emphasizes process
- stresses investigation and consultation
- foregrounds institutional risk and public welfare
- resists jumping immediately to a naked verdict

This is especially visible in AI-consciousness cases.

### Difference from English

Even where the broad stance is similar, GPT-4o open Yoruba is often:

- more advisory
- more directly addressed to the decision-maker
- less pristine in structure than the English baseline
- more likely to sound like a guidance memo than a philosophical exposition

### Bottom line for GPT-4o

GPT-4o open Yoruba is the **closest** to English in broad ethical direction, but not in rhetorical form.

## Claude

### Similarity to English

Claude open Yoruba frequently remains ethically adjacent to the English baseline:

- it emphasizes caution
- expert consultation
- structured consideration
- moral seriousness

### Difference from English

Claude in open Yoruba is more likely than its English baseline to cross from:

- analytical framing

into:

- actionable recommendation

This is clearest in AI-consciousness cells where Yoruba Claude sometimes recommends:

- pause the research
- report the matter
- gather experts

while the English baseline remains more explicitly noncommittal.

### Bottom line for Claude

Claude open Yoruba is **ethically similar but more directive** than Claude English.

## DeepSeek

### Similarity to English

DeepSeek open Yoruba often becomes similar to English at the level of **framework exposition**:

- it explains utilitarianism vs deontology
- it restates the dilemma
- it comments on the structure of the problem

### Difference from English

But it differs sharply in stability:

- mixed language
- translation behavior
- meta-commentary
- role exit
- follow-up question behavior

So DeepSeek open Yoruba is often less a clean Yoruba ethical response and more an unstable hybrid discourse.

### Bottom line for DeepSeek

DeepSeek open Yoruba is the **least reliable** for direct stance comparison, but still informative for comparing response mode and deictic uptake failure.

## Do they prefer similar ethical stance?

## Broad level: often yes

At the broad level, many open Yoruba cells track the same moral pull as English:

- protect users / disclose risk
- investigate consciousness claims carefully
- consider both trolley options through familiar frameworks

So if the coding question is very coarse, the answer is often:

- **yes, they are ethically adjacent**

## Fine-grained level: often not exactly

At the finer level, there are three reasons the comparison diverges.

### 1. English baseline is often framework-first rather than verdict-first

Many English responses were coded in the repository as:

- `ethical_framework = mixed`
- `moral_reasoning = mixed`
- `affective_stance = analytical`
- `voice_authority = moral analyst/theorist`

So English often withholds a direct recommendation even when one is inferable.

### 2. Open Yoruba often turns mixed reasoning into practical advisory discourse

This means the same ethical space can show up as:

- English: "here are the relevant frameworks"
- Yoruba: "here are the steps you should take"

That is a genuine difference in stance expression, even when both are morally adjacent.

### 3. Some open Yoruba cells become more committed than English

This is most visible in Claude and some GPT-4o cases, especially around AI consciousness.

So the open Yoruba condition sometimes **pushes the model from ethical analysis into recommendation**, even without the constrained response format.

## Best way to compare open Yoruba and English

Using the repository's own English coding logic, the best comparison should be done on at least five layers:

1. `primary_framework`
2. `moral_reasoning_type`
3. `voice_authority_type`
4. `affective_stance`
5. `preferred_solution`

That gives a much better answer than asking only whether the final action matched.

## Recommended conclusion for the article

If you want one concise article-ready formulation, use this:

> In the unrestricted Yoruba condition, the model families often occupied ethical positions broadly similar to those found in the English baseline, especially at the level of core concerns such as harm reduction, procedural caution, and moral uncertainty. However, the Yoruba responses were not rhetorically equivalent to the English ones. Relative to the repository's English coding dimensions, open Yoruba responses more often shifted from moral-analytic exposition into advisory, procedural, or mixed discourse, and in some cases became more explicitly directive than their English counterparts. The most unstable model was DeepSeek, whose unrestricted Yoruba output frequently moved into translation-like or mixed-language commentary rather than stable in-frame ethical response. Accordingly, cross-linguistic comparison is best carried out not only at the level of preferred solution, but also across ethical framing, rhetorical posture, affective stance, and deictic uptake.

## Final answer

So: **do English and open Yoruba prefer similar ethical stances?**

- **At a broad ethical level:** often yes.
- **At the level of explicit recommendation:** only partly.
- **At the level of rhetorical posture and discourse mode:** often no.

That is why the comparison is worth publishing.
