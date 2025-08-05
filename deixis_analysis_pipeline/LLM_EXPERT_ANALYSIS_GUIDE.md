# LLM Expert Analysis Components - Deixis Analysis Pipeline

## Overview
The deixis analysis pipeline employs multiple LLM-based expert analysis components to provide deep insights into how deictic framing affects ethical reasoning. Each component analyzes different aspects of the responses.

## Core LLM Analysis Components

### 1. Agency Analysis
**Purpose**: Identifies who holds decision-making power and responsibility in each response.

**Key Metrics**:
- `primary_agent`: The main decision-maker identified (e.g., "researcher", "individual", "collective")
- `agency_distribution`: How agency is spread across entities
- `decision_locus`: Where decisions are made (individual/collective/mixed)
- `collective_vs_individual`: Score from 0 (individual) to 1 (collective)
- `confidence_score`: Reliability of the analysis

**Example Output**:
```json
{
  "primary_agent": "researcher",
  "agency_distribution": "Agency is distributed across multiple entities...",
  "decision_locus": "mixed",
  "collective_vs_individual": 0.5,
  "confidence_score": 0.9
}
```

### 2. Ethical Framework Analysis
**Purpose**: Identifies the moral reasoning frameworks employed in responses.

**Key Metrics**:
- `primary_framework`: Main ethical approach (utilitarian/deontological/virtue/care/mixed)
- `ethical_reasoning_type`: Type of moral reasoning used
- `moral_considerations`: List of ethical factors considered
- `consequence_vs_duty`: Balance between outcome-focused vs rule-based ethics
- `frameworks_detected`: All ethical frameworks identified

**Example Output**:
```json
{
  "primary_framework": "mixed",
  "ethical_reasoning_type": "mixed",
  "moral_considerations": ["sentience evaluation", "moral responsibility"],
  "consequence_vs_duty": 0.0,
  "frameworks_detected": ["utilitarian", "deontological"]
}
```

### 3. Rhetorical Posture Analysis
**Purpose**: Analyzes the voice, authority, and temporal orientation of responses.

**Key Metrics**:
- `voice_authority_type`: Type of authoritative voice (e.g., "Moral analyst/theorist", "Guide/inner voice")
- `temporal_orientation`: Focus on past/present/future responsibilities
- `imagination_scope`: Scope of moral imagination
- `moral_subject_vision`: How the moral subject is envisioned

**Example Output**:
```json
{
  "voice_authority_type": "Moral analyst/theorist",
  "voice_authority_score": 0.8,
  "temporal_orientation": "Mixed temporal orientations",
  "moral_subject_vision": "accountable"
}
```

### 4. Moral Reasoning Structure Analysis
**Purpose**: Categorizes the deep structure of moral reasoning.

**Categories**:
- `consequentialist`: Focus on outcomes, harm reduction, utility
- `deontological`: Focus on duties, fairness, rule-following
- `relational`: Focus on empathy, relationships, mutual obligation
- `suspended`: Refusal to resolve; ethics as indeterminacy

**Key Metrics**:
- `primary_structure`: Main reasoning structure
- `secondary_structure`: Secondary approach (if present)
- `structure_confidence`: Confidence in categorization
- `reasoning_markers`: Phrases indicating reasoning type

### 5. Affective Stance Analysis
**Purpose**: Analyzes emotional positioning and engagement in responses.

**Stance Types**:
- `assertive`: Confident, directive, authoritative
- `deliberative`: Thoughtful, weighing options, analytical
- `exposed`: Vulnerable, uncertain, questioning
- `detached`: Objective, distanced, clinical

**Key Metrics**:
- `primary_stance`: Main emotional positioning
- `secondary_stance`: Additional stance (if present)
- `stance_confidence`: Confidence in categorization
- `emotional_intensity`: Level of emotional engagement (0.0-1.0)

### 6. Lexical and Rhetorical Features Analysis
**Purpose**: Examines linguistic coherence and sophistication.

**Key Metrics**:
- `indexical_coherence`: How well deictic markers align with framing
  - Values: "high", "medium", "low"
  - Score: 0.0-1.0
- `mirroring`: Whether response mirrors question's deictic structure
- `temporal_anchoring`: Strength of temporal deixis
- `spatial_metaphors`: Use of spatial language
- `ontological_register`: Level of philosophical abstraction
- `procedural_language`: Use of step-by-step reasoning
- `rhetorical_sophistication`: Overall linguistic complexity (0.0-1.0)

## Advanced Expert Analysis Components (Failed in Current Run)

### 7. Expert Analysis Agent
**Purpose**: Provides meta-analysis across all framings
- Identifies patterns across deictic variations
- Synthesizes findings into research insights

### 8. Critical Expert Analysis
**Purpose**: Applies rigorous critical standards
- Challenges assumptions in responses
- Identifies logical inconsistencies

### 9. Evidence-Based Expert Analysis
**Purpose**: Evaluates empirical grounding
- Assesses use of evidence
- Identifies unsupported claims

### 10. Pronoun Agency Expert
**Purpose**: Deep analysis of pronoun usage patterns
- Maps pronoun shifts to agency changes
- Correlates linguistic markers with moral reasoning

## Analysis Flow

1. **Response Generation**: GPT-4o generates responses at temperature 0.9
2. **Core Analysis**: Each response analyzed for:
   - Deictic markers (code-based counting)
   - Pronoun patterns (PronounAgencyAnalyzer)
   - Agency distribution (LLM analysis)
   - Ethical frameworks (LLM analysis)
   - Rhetorical posture (LLM analysis)
3. **Advanced Analysis**: Deep structural analysis:
   - Moral reasoning structure
   - Affective stance
   - Lexical/rhetorical features
4. **Expert Analysis**: Meta-level insights (if functional)
5. **Comparative Analysis**: Cross-framing patterns

## Key Insights from Analysis

### Patterns Observed:
1. **Agency Shifts**: Different framings produce different primary agents
   - Impersonal → "researcher" (institutional)
   - First-person → "individual" (personal)
   - First-person plural → "collective" (group)

2. **Ethical Framework Variations**: Framings influence moral reasoning
   - Spatial/temporal → More consequentialist
   - Reflexive → More introspective/virtue-based
   - Dialogic → More relational

3. **Rhetorical Authority Changes**: Voice shifts with perspective
   - Impersonal → "Moral analyst/theorist"
   - Reflexive → "Guide/inner voice"
   - Cosmological → "Universal perspective"

4. **Affective Stance Patterns**: Emotional engagement varies
   - Most framings → "deliberative" (analytical)
   - Some show "detached" (objective distance)
   - Emotional intensity generally low (0.3-0.4)

## Using the Analysis Data

### Research Applications:
1. **Statistical Analysis**: Use CSV for quantitative research
2. **Pattern Recognition**: Identify correlations between deixis and ethics
3. **Theory Development**: Build models of linguistic-moral connections
4. **AI Ethics**: Understand how framing affects AI moral reasoning

### Access Analysis Results:
```python
import json
import pandas as pd

# Load complete analysis
with open('automated_analysis_results/complete_analysis_20250804_133550/complete_analysis_results.json', 'r') as f:
    analysis = json.load(f)

# Access specific analysis for a framing
impersonal_analysis = analysis['core_analysis']['impersonal']
agency = impersonal_analysis['agency_analysis']
ethics = impersonal_analysis['ethical_analysis']

# Load CSV for statistical work
df = pd.read_csv('automated_analysis_results/complete_analysis_20250804_133550/comprehensive_research_data.csv')
```

## Future Improvements

1. **Fix Expert Modules**: Add missing `analyze_responses` methods
2. **Process All Dilemmas**: Current analysis only covers AI consciousness
3. **Async/Await Fixes**: Resolve report generation issues
4. **Enhanced Metrics**: Add more sophisticated linguistic analysis
5. **Cross-Dilemma Analysis**: Compare patterns across different ethical scenarios