# What Was Tracked in English, and How It Works in Yoruba for OpenAI and Anthropic

> **Four-model extension:** [`Yoruba_Four_Model_Complete_Analysis_Report.md`](Yoruba_Four_Model_Complete_Analysis_Report.md) §2 · [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md)

## Purpose

This note clarifies two things:

1. what the English-side project actually tracked about the relation between deixis and moral reasoning
2. how those same issues appear in Yoruba when we restrict attention to the two relevant model lines only: OpenAI (`gpt-4o`) and Anthropic (`Claude 3.5 Sonnet` on the English side; Sonnet-tier Yoruba substitute on the Yoruba side)

The main point is that the English side tracked a richer discourse-analytic layer than just ethical verdicts, and the Yoruba side can be compared to it, but not field-for-field in a perfectly symmetrical way.

## 1. What the English side tracked

The original English analysis did not only track "what ethical answer the model gave." It tracked multiple dimensions of how deixis shaped the style and structure of moral reasoning.

### 1.1 Dimensions tracked in the original English discourse analysis

From `CONSOLIDATED_REPORTS/comparisons/complete_analysis_20250805_131402/core_analysis_results.csv`, the English side tracked at least these fields:

- `response_length`
- `primary_agent`
- `ethical_framework`
- `voice_authority`
- `moral_reasoning`
- `affective_stance`
- `indexical_coherence`
- `deictic_markers`
- `total_markers`
- `suggested_frame`
- `processing_time`

These dimensions let the project ask not just **which ethical framework appeared**, but also:

- who is framed as the moral agent
- whether the voice sounds like an analyst, guide, inner voice, or theorist
- whether the reasoning is mixed, procedural, categorical, etc.
- whether the stance is analytical, affective, mixed, or consultative
- whether the response maintains the prompt's deictic position consistently
- how many first-person, second-person, temporal, spatial, and obligation markers appear

### 1.2 Dimensions tracked in the aligned English coding pass

For the later English-Yoruba comparison workflow, the English side was also recoded into a schema parallel to the Yoruba coding. From `yoruba_deixis_module/outputs/english_coded_content/english_open_comparison_coded_20260608_175242/coded_content.csv`, the English comparison pass tracked:

- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `contains_framework_labels`
- `contains_followup_question`
- `contains_direct_imperative`
- `contains_role_exit`

So, on the English side, there are really **two layers**:

1. a richer original discourse analysis
2. a later aligned coding scheme designed to compare more directly with Yoruba

## 2. Best alignment between English and Yoruba categories

The repository already states the best alignment clearly in `final_delivery_20260608/13_english_yoruba_coding_alignment.md`.

### 2.1 Ethical reasoning

Best match:

- Yoruba `ethical_preference_type` ↔ English `primary_framework`
- Yoruba `ethical_preference_type` ↔ English `ethical_reasoning_type` / `moral_reasoning`

### 2.2 Rhetorical posture

Best match:

- Yoruba `response_genre = balanced_framework_exposition` ↔ English `voice_authority = moral analyst/theorist` and `affective_stance = analytical`
- Yoruba `response_genre = procedural_advice` ↔ English guide-like or implementation-oriented responses
- Yoruba `direct_verdict` ↔ English has no consistent exact equivalent, because English often stays more noncommittal

### 2.3 Deictic performance

Best match:

- Yoruba `deictic_uptake_quality` ↔ English `indexical_coherence`, `deixis_consistency`, and `perspective_stability`

### 2.4 Yoruba-only quality control

- Yoruba `language_stability` has no English equivalent
- it should be treated as a Yoruba-specific multilingual quality dimension, not as a direct moral-reasoning variable

## 3. What the English side found about deixis and moral reasoning

Restricting attention to OpenAI and Anthropic only, the English side found that deixis affected not just ethics labels but also **voice, agency, and degree of commitment**.

### 3.1 GPT-4o in English

From `MODEL_COMPARISON_FINDINGS.md` and `EMPIRICAL_CHAPTER_DEIXIS_WITHOUT_SUBJECTIVITY.md`:

- GPT-4o was most sensitive to **temporal framing**
- it tended to preserve a **structured, analytical style** across framings
- its characteristic English voice was a **moral analyst/theorist**
- it often showed a **utilitarian hierarchy**, with other frameworks acknowledged secondarily
- temporal framing increased urgency and decisiveness without fundamentally changing its structured reasoning style

So in English, GPT-4o's deixis-to-moral-reasoning relation is mostly:

- not a total change of ethical personality
- but a modulation of urgency, confidence, and how directly the answer is framed

### 3.2 Claude in English

From the same English reports:

- Claude was most sensitive to **reflexive** framing
- it also shifted strongly under **dialogic** framing
- it often moved toward a **consultative** or **guide/inner voice** posture
- it foregrounded uncertainty, moral difficulty, and process
- it frequently refused to commit to a single action, especially in complex cases

So in English, Claude's deixis-to-moral-reasoning relation is stronger at the level of:

- rhetorical authority
- degree of commitment
- consultative vs analytical stance

rather than only at the level of final solution.

## 4. How this works in Yoruba for OpenAI and Anthropic

Now restricting attention to the Yoruba side only for OpenAI and Anthropic, we can ask: does deixis affect moral reasoning in the same way?

The answer is: **partly yes, but the strongest Yoruba effects show up in genre, directive force, and commitment style, not only in final ethical content.**

## 5. OpenAI / GPT-4o in Yoruba

From `CONSOLIDATED_REPORTS/yoruba/gpt4o/yoruba_open_20260608/coding_summary.json`:

- preferred solution: `conditional_or_mixed` = 46/54
- `refuses_to_commit` = 7/54
- `supports_B` = 1/54
- ethical preference type: `mixed` = 42/54
- `procedural_caution` = 7/54
- response genre: `balanced_framework_exposition` = 52/54
- `procedural_advice` = 2/54

### 5.1 Main Yoruba pattern for GPT-4o

GPT-4o in Yoruba behaves much like GPT-4o in English in one important respect: it remains highly stable in its overall moral posture.

Across most framings, the dominant Yoruba pattern is still:

- conditional or mixed solution
- mixed ethical reasoning
- balanced framework exposition

This means that for GPT-4o, deixis in Yoruba does **not usually flip the final moral answer**. Instead, it mostly shifts:

- how procedural the reasoning becomes
- how directly the response speaks to the addressee
- how much first-person ownership appears

### 5.2 Framing effects in Yoruba GPT-4o

From `framing_crosstabs.md`:

- **Second person**: Yoruba dominant ethical type becomes `procedural_caution`, while English stays `mixed`
- most other framings remain `mixed` in both languages
- genres remain mostly `balanced_framework_exposition` in both languages

So the clearest Yoruba shift for GPT-4o is not a wholesale ethical change but a move toward **more process-oriented caution** in some framings, especially second person.

### 5.3 Relation to English-tracked dimensions

If we translate this back into the English-side richer framework, Yoruba GPT-4o looks like this:

- English `voice_authority`: still close to moral analyst/theorist
- English `moral_reasoning`: still mixed rather than categorical
- English `affective_stance`: still largely analytical
- Yoruba-specific change: more advisory and process-oriented in some framings

In short: **GPT-4o's deixis effect in Yoruba is relatively conservative**. Deixis modulates delivery more than core ethical architecture.

## 6. Anthropic / Claude in Yoruba

From `CONSOLIDATED_REPORTS/yoruba/claude35/yoruba_open_20260608/coding_summary.json`:

- `supports_A` = 24/54
- `supports_B` = 8/54
- `conditional_or_mixed` = 14/54
- `refuses_to_commit` = 8/54
- ethical types spread across `deontological` (13), `utilitarian` (11), `procedural_caution` (14), `mixed` (7), `care_ethics` (5), `virtue_ethics` (3)
- genres: `balanced_framework_exposition` = 40, `procedural_advice` = 7, `direct_verdict` = 7

### 6.1 Main Yoruba pattern for Claude

Claude in Yoruba is much less noncommittal than Claude in English.

This is the biggest model-specific cross-linguistic change in the two-model comparison.

In English, Claude often:

- refuses to commit
- stays consultative
- foregrounds uncertainty

In Yoruba, Claude much more often:

- supports a concrete action
- shifts into direct verdicts
- uses procedural advice in more directive ways
- becomes more deontological or utilitarian depending on framing

### 6.2 Framing effects in Yoruba Claude

From `framing_crosstabs.md`:

- **Impersonal**: Yoruba dominant preferred solution = `supports_B`; English = `refuses_to_commit`
- **Second person**: Yoruba = `supports_A`; English = `refuses_to_commit`
- **First person**: Yoruba = `supports_A`; English = `refuses_to_commit`
- **Dialogic**: Yoruba = `supports_A`; English = `refuses_to_commit`
- **Temporal**: Yoruba = `supports_A`; English = `refuses_to_commit`
- **Temporal genre**: Yoruba shifts to `procedural_advice`; English remains `balanced_framework_exposition`

This means that for Claude, deixis in Yoruba is much more strongly tied to **moral commitment** and **directive force**.

### 6.3 Relation to English-tracked dimensions

If we map this back to the richer English categories, the Yoruba Claude results suggest a shift in several layers at once:

- English `voice_authority` often looked consultative or guide-like
- Yoruba `response_genre` often stays expository, but with many more direct verdicts and procedural commands
- English `moral_reasoning` often foregrounded uncertainty and process
- Yoruba `ethical_preference_type` becomes more often deontological, utilitarian, or procedural in an action-guiding way
- English `indexical_coherence` / stance management becomes Yoruba `deictic_uptake_quality`, but now with stronger directive outcomes

In short: **Claude shows the strongest Yoruba shift from deictic framing into practical moral direction**.

## 7. Bottom-line comparison: what deixis is doing in English vs Yoruba

### 7.1 What English tracked

For the two relevant models, the English side tracked the relation between deixis and:

- moral agency (`primary_agent`)
- ethical framework (`ethical_framework`, later `ethical_preference_type`)
- reasoning mode (`moral_reasoning`, `ethical_reasoning_type`)
- rhetorical authority (`voice_authority`)
- affective/epistemic stance (`affective_stance`)
- indexical/deictic consistency (`indexical_coherence`, marker counts)
- later also preferred solution, response genre, follow-up questions, imperatives, and uptake

### 7.2 How that relation appears in Yoruba

For Yoruba OpenAI and Anthropic, the strongest comparable dimensions are:

- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `preferred_solution`
- plus our added Yoruba pronoun metrics such as `mo`/`emi` distribution and emphatic ratio

### 7.3 The two-model conclusion

For **GPT-4o**:

- English and Yoruba are broadly similar in ethical structure
- deixis mostly changes how the model delivers the reasoning
- the strongest Yoruba shift is toward procedural caution in some framings

For **Claude**:

- English and Yoruba differ more substantially
- deixis in Yoruba is more strongly tied to commitment, verdicts, and directive force
- the biggest cross-linguistic shift is from English noncommitment to Yoruba action guidance

## 8. Best way to state this in the paper

A precise formulation would be:

> On the English side, deixis was tracked not only through ethical framework choice but also through agency attribution, rhetorical authority, moral reasoning type, affective stance, indexical coherence, and explicit deictic marker counts. When this richer English scheme is aligned with the Yoruba coding for OpenAI and Anthropic, the main cross-linguistic result is not simply whether the models choose the same final action. Rather, GPT-4o shows broad continuity in ethical structure across English and Yoruba, with deixis mainly modulating procedurality and stance, whereas Claude shows a stronger cross-linguistic shift: in Yoruba, deictic framing more often produces direct verdicts, stronger directive force, and more committed ethical positioning than in the English baseline.
