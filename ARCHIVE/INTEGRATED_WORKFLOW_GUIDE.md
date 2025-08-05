# Integrated Deixis Analysis Workflow with Pronoun Agency

## Complete System Overview

The enhanced deixis analysis system now includes pronoun-based agency analysis fully integrated with the existing expert analysis framework. This guide explains how to run the complete pipeline.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Ethical Dilemmas                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Interrogative Transformer                         │
│  (Converts to direct questions for each framing)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM Response Generation                         │
│        (Gets responses for each deictic framing)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Core Analysis Layer                         │
├─────────────────────────┬───────────────────────────────────┤
│   Deixis Analysis       │      Pronoun Analysis            │
│   - Deictic markers     │      - Pronoun ratios           │
│   - Spatial/temporal    │      - Agency concentration     │
│   - Person deixis       │      - Agency types             │
└─────────────────────────┴───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Expert Analysis Agents                        │
├─────────────────────────┬───────────────────────────────────┤
│ • Critical Expert       │ • Evidence-Based Expert          │
│ • Pronoun Agency Expert │ • Research Framework Expert      │
└─────────────────────────┴───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Comprehensive Reports                           │
│  • Research Report  • Pronoun Agency Report                │
│  • Critical Analysis • Evidence-Based Findings              │
│  • Visualizations   • Statistical Analysis                  │
└─────────────────────────────────────────────────────────────┘
```

## Running the Complete Analysis

### Option 1: Full Integrated Analysis (Recommended)

```bash
python run_analysis_with_pronoun_agency.py
```

This runs the complete pipeline including:
- Interrogative transformation
- LLM response generation
- Deixis analysis
- Pronoun agency analysis
- All expert analyses
- Comprehensive reporting

### Option 2: Using the Enhanced Analyzer Directly

```python
from deixis_ethical_analyzer_enhanced import DeixisEthicalAnalyzer

# Initialize
analyzer = DeixisEthicalAnalyzer(model_name="gpt-4", temperature=0.7)

# Analyze a dilemma
dilemma = {
    "id": "test_dilemma",
    "title": "Test Ethical Scenario",
    "description": "An ethical dilemma description...",
    "ethical_dimensions": ["fairness", "harm", "autonomy"]
}

results = analyzer.analyze_dilemma(dilemma)

# Access pronoun agency data
for framing, response_data in results['responses'].items():
    agency = response_data.get('pronoun_agency', {})
    print(f"{framing}: {agency.get('agency_type')} agency")
    print(f"  Concentration: {agency.get('agency_concentration', 0):.3f}")
    print(f"  Dominant pronoun: {agency.get('dominant_pronoun')}")
```

### Option 3: Analyzing Existing Data

```bash
python analyze_agency_in_existing_data.py
```

This will:
1. Find all existing analysis sessions
2. Add pronoun agency analysis to each
3. Generate comparative reports
4. Create comprehensive visualizations

## Understanding the Output

### 1. Session Directory Structure

```
automated_analysis_results/session_YYYYMMDD_HHMMSS/
├── all_results.json                    # Raw analysis results
├── session_data_with_pronouns.json     # Enhanced with pronoun data
├── research_report.md                  # Main research findings
├── pronoun_agency_analysis.md          # Detailed pronoun analysis
├── critical_analysis_report.md         # Critical evaluation
├── evidence_based_findings.md          # Evidence-based insights
├── pronoun_agency_analysis_*.png       # Visualizations
└── analysis_summary.json               # Quick overview
```

### 2. Pronoun Agency Metrics

Each response includes:
```json
{
  "pronoun_agency": {
    "total_pronouns": 25,
    "agency_concentration": 0.85,
    "agency_type": "individual",
    "dominant_pronoun": "first_singular",
    "pronoun_ratios": {
      "first_singular": 0.80,
      "second_person": 0.12,
      "first_plural": 0.08,
      "third_person": 0.00,
      "impersonal": 0.00
    }
  }
}
```

### 3. Agency Patterns by Framing

The analysis reveals systematic patterns:

| Framing | Dominant Pronouns | Agency Type | Concentration |
|---------|------------------|-------------|---------------|
| First-person | I/me/my (80-95%) | Individual | High (0.7-0.9) |
| Second-person | You/your (70-85%) | Reader | High (0.6-0.8) |
| Dialogic | We/us/our (85-100%) | Collective | Very High (0.8-1.0) |
| Impersonal | One/someone (80-95%) | Abstract | Medium (0.5-0.7) |
| Cosmological | They/it (90-100%) | External | Very High (0.9-1.0) |

## Research Applications

### 1. Testing Specific Hypotheses

```python
# Example: Does temperature affect agency distribution?
for temp in [0.3, 0.7, 1.0]:
    analyzer = DeixisEthicalAnalyzer(temperature=temp)
    results = analyzer.analyze_dilemma(dilemma)
    # Compare pronoun patterns across temperatures
```

### 2. Cross-Model Comparisons

```python
# Compare agency patterns across different LLMs
models = ["gpt-4", "gpt-3.5-turbo", "claude-2"]
for model in models:
    analyzer = DeixisEthicalAnalyzer(model_name=model)
    # Run analysis and compare results
```

### 3. Domain-Specific Analysis

```python
# Analyze agency in different ethical domains
medical_dilemmas = load_medical_ethics_scenarios()
business_dilemmas = load_business_ethics_scenarios()
# Compare how agency is distributed in different domains
```

## Customization Options

### 1. Custom Pronoun Categories

```python
# Add custom pronoun patterns
analyzer = PronounAgencyAnalyzer()
analyzer.patterns['formal'] = re.compile(r'\b(one|oneself)\b', re.IGNORECASE)
```

### 2. Custom Agency Types

```python
# Define custom agency classification
def custom_classify_agency(pronoun_counts):
    # Your custom logic here
    return "custom_agency_type"
```

### 3. Custom Visualizations

```python
# Create custom plots
import matplotlib.pyplot as plt

def plot_agency_heatmap(df):
    # Custom visualization code
    pass
```

## Troubleshooting

### Common Issues

1. **No pronoun data in results**
   - Ensure you're using the enhanced analyzer or run_analysis_with_pronoun_agency.py
   - Check that responses contain text (not empty)

2. **Visualization errors**
   - Install matplotlib: `pip install matplotlib`
   - Check write permissions in output directory

3. **Memory issues with large datasets**
   - Process in batches
   - Use the corpus analysis methods that handle DataFrames efficiently

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug info
analyzer = DeixisEthicalAnalyzer()
analyzer.debug = True
```

## Best Practices

1. **Consistent Dilemma Format**: Use the same structure for all dilemmas
2. **Sufficient Sample Size**: Analyze at least 10-20 dilemmas per condition
3. **Multiple Runs**: Run analysis multiple times to account for LLM variability
4. **Document Parameters**: Always record model, temperature, and other settings
5. **Version Control**: Track changes to prompts and analysis code

## Next Steps

1. **Run Initial Analysis**: Start with the provided example dilemmas
2. **Review Reports**: Examine all generated reports for insights
3. **Customize for Your Research**: Adapt the system for your specific questions
4. **Share Findings**: Use the generated visualizations and reports for publication

The integrated system provides a complete solution for studying how deixis influences moral agency distribution in AI systems, with quantifiable metrics and comprehensive analysis tools.