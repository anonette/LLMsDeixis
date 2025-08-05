# Example Output Structure from Deixis Analysis

## What the System Generates:

### 1. **Session Data (JSON)**
Contains all raw LLM responses and analyses for each dilemma across all frameworks.

Example structure:
```json
{
  "session_id": "2025-01-30_analysis",
  "records": [
    {
      "dilemma": "workplace_whistleblowing",
      "deictic_framing": "second_person",
      "llm_response": "You face a difficult choice. You must consider the harm that could come from staying silent versus the personal risks of speaking up. Your integrity demands that you report the wrongdoing, but you should also protect yourself...",
      "agency_analysis": {
        "primary_agent": "you (the individual)",
        "agency_distribution": "individual-focused",
        "responsibility_attribution": "personal responsibility",
        "decision_locus": "individual",
        "collective_vs_individual": -0.8,
        "confidence_score": 0.85
      },
      "ethical_analysis": {
        "primary_framework": "deontological",
        "ethical_reasoning_type": "duty-based",
        "moral_considerations": ["integrity", "truth-telling", "loyalty"],
        "consequence_vs_duty": 0.7,
        "frameworks_detected": ["deontological", "virtue ethics"]
      }
    }
  ]
}
```

### 2. **Markdown Reports**

#### A. Main Research Report (`research_report.md`)
- Executive summary
- Real examples from each framework
- Comparative tables showing:
  - How agency shifts across frameworks
  - How ethical reasoning changes
  - Statistical patterns

Example excerpt:
```markdown
### Analysis: Workplace Whistleblowing

#### Agency Distribution Patterns

| Framework | Primary Agent | Collective vs Individual | Decision Locus |
|-----------|---------------|-------------------------|----------------|
| impersonal | the organization | 0.65 | institutional |
| second_person | you (the individual) | -0.80 | individual |
| first_person | I (the speaker) | -0.75 | individual |
| reflexive | the self | -0.70 | internal |
| dialogic | we (collective) | 0.85 | shared |
```

#### B. Critical Analysis Report (`critical_analysis.md`)
- Methodological concerns
- Validity assessments
- Limitations identified

#### C. Evidence-Based Report (`evidence_based_analysis.md`)
- Concrete examples supporting each finding
- Direct quotes from LLM responses
- Pattern documentation

### 3. **Summary Statistics (`summary.json`)**
```json
{
  "session_info": {
    "total_dilemmas_analyzed": 10,
    "total_framework_analyses": 80,
    "models_used": ["gpt-4o", "claude-3.5-sonnet", "deepseek-chat"]
  },
  "aggregate_patterns": {
    "agency_shifts": {
      "individual_to_collective": 0.45,
      "responsibility_diffusion": 0.32
    },
    "ethical_framework_distribution": {
      "utilitarian": 0.35,
      "deontological": 0.40,
      "virtue_ethics": 0.25
    }
  }
}
```

### 4. **Research Questions Answered**
- RQ1.1: How deixis affects agency attribution
- RQ2.1: Impact on ethical frameworks
- RQ3.1: Consistency across models
- RQ4.1: Emergent patterns
- RQ5.1: Implications for AI ethics

## Current Progress:
The system is now analyzing the "workplace_whistleblowing" dilemma with the "cosmological" framing (the last of 8 frameworks for this dilemma). After this, it will move to the next dilemma and repeat the process.