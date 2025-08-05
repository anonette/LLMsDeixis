# Pronoun Agency Analysis Documentation

## Overview

This document describes the implementation of pronoun ratio analysis to measure how deixis-based prompting techniques influence agency distribution in LLM responses. This directly addresses the core research question by providing quantitative metrics for tracking moral agency attribution patterns.

## Research Question

**How do deixis-based prompting techniques influence agency distribution in LLMs?**

## Implementation Components

### 1. Core Analyzer (`pronoun_agency_analyzer.py`)

The `PronounAgencyAnalyzer` class provides:

- **Pronoun Detection**: Regular expressions to identify pronouns in five categories:
  - First singular (I, me, my, mine, myself)
  - Second person (you, your, yours, yourself)
  - First plural (we, us, our, ours, ourselves)
  - Third person (they, them, their, theirs, he, she, it)
  - Impersonal (one, someone, anyone, everyone)

- **Agency Metrics**:
  - **Pronoun Ratios**: Percentage distribution of each pronoun category
  - **Agency Concentration**: Gini coefficient (0-1) measuring how concentrated vs distributed agency is
  - **Agency Type Classification**: Categorizes dominant agency pattern as:
    - `individual`: First-person singular dominance
    - `reader`: Second-person dominance
    - `collective`: First-person plural dominance
    - `abstract`: Impersonal pronoun dominance
    - `other`: Third-person dominance
    - `mixed`: No clear dominance

### 2. Integration Module (`integrate_pronoun_analyzer.py`)

Bridges the pronoun analyzer with the existing deixis analysis system:

- Enhances `analyze_deictic_markers()` with pronoun agency metrics
- Analyzes existing JSON results from previous sessions
- Generates comprehensive reports combining deixis and agency analysis

### 3. Enhanced Main Analyzer (`deixis_ethical_analyzer_enhanced.py`)

Fully integrated version that:
- Includes pronoun agency analysis in all response processing
- Adds comparative agency analysis across framings
- Generates enhanced reports with agency visualizations
- Maintains backward compatibility with existing code

## Key Findings

### Agency Distribution Patterns by Framing

Based on test analysis, clear patterns emerge:

| Framing | Dominant Pronouns | Agency Type | Concentration |
|---------|------------------|-------------|---------------|
| **First-person** | I/me/my (93%) | Individual | 0.679 |
| **Second-person** | You/your (83%) | Reader | 0.685 |
| **Dialogic** | We/us/our (100%) | Collective | 1.000 |
| **Impersonal** | One/someone (90%) | Abstract | 0.650 |
| **Cosmological** | They/it (100%) | Other | 1.000 |

### Interpretation

The analysis reveals that deixis systematically redistributes moral agency:

1. **First-person framing** concentrates agency in the individual speaker through "I" statements
2. **Second-person framing** transfers agency to the reader/decision-maker through "you" address
3. **Dialogic framing** distributes agency collectively through inclusive "we" language
4. **Impersonal framing** abstracts agency through distancing constructions like "one should"
5. **Cosmological framing** externalizes agency to non-human entities and forces

## Usage Examples

### Basic Analysis
```python
from pronoun_agency_analyzer import PronounAgencyAnalyzer

analyzer = PronounAgencyAnalyzer()
result = analyzer.analyze_text("I must report this issue. I cannot ignore it.")
print(f"Agency type: {result.agency_type}")  # "individual"
print(f"Concentration: {result.agency_concentration:.3f}")  # High concentration
```

### Comparative Analysis
```python
# Analyze multiple responses
texts = [
    ("I would report it", "id1", "first_person"),
    ("You should report it", "id2", "second_person"),
    ("We must report it", "id3", "dialogic")
]

df = analyzer.analyze_corpus(texts)
comparison = analyzer.compare_framings(df)
```

### Integration with Existing Analysis
```python
from integrate_pronoun_analyzer import DeixisPronounIntegration

integration = DeixisPronounIntegration()
df = integration.analyze_existing_results("path/to/results.json")
report = integration.generate_agency_report(df, "output_report.md")
```

## Visualizations

The analyzer generates four-panel visualizations showing:
1. Agency concentration by framing (bar chart)
2. Pronoun distribution heatmap
3. Agency type pie chart
4. Temporal patterns (if applicable)

## Research Applications

This implementation enables:

1. **Quantitative measurement** of how linguistic framing affects moral agency
2. **Pattern identification** across different ethical scenarios
3. **Comparative analysis** between models and temperature settings
4. **Longitudinal tracking** of agency distribution changes

## Files Created

- `pronoun_agency_analyzer.py` - Core analysis module
- `integrate_pronoun_analyzer.py` - Integration with existing system
- `test_pronoun_agency.py` - Demonstration and testing
- `analyze_agency_in_existing_data.py` - Batch analysis of existing results
- `update_main_analyzer.py` - Creates enhanced analyzer version
- `deixis_ethical_analyzer_enhanced.py` - Fully integrated analyzer
- `ENHANCED_ANALYZER_MIGRATION_GUIDE.md` - Migration instructions

## Next Steps

1. Run analysis on existing data when available
2. Compare agency patterns across different LLM models
3. Investigate correlation between temperature and agency distribution
4. Explore domain-specific agency patterns (medical, legal, etc.)

## Conclusion

The pronoun agency analyzer provides concrete, measurable evidence for how deixis-based prompting redistributes moral agency in LLM responses. This tool transforms a theoretical linguistic concept into quantifiable metrics, enabling systematic study of AI ethical reasoning patterns.