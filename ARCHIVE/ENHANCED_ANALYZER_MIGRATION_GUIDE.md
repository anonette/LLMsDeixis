# Migrating to Enhanced Deixis Analyzer

## Overview
The enhanced analyzer adds pronoun agency analysis to track how different deictic framings redistribute moral agency through pronoun usage patterns.

## New Features

### 1. Pronoun Agency Metrics
Each response now includes:
- `total_pronouns`: Total pronoun count
- `agency_concentration`: Gini coefficient measuring concentration (0-1)
- `agency_type`: Classification (individual/collective/reader/abstract/other)
- `pronoun_ratios`: Distribution of pronoun types
- `dominant_pronoun`: Most frequent pronoun category

### 2. Comparative Analysis
The analyzer now provides:
- Cross-framing agency comparisons
- Visualization of agency distribution patterns
- Statistical analysis of pronoun usage

### 3. Enhanced Reports
Reports now include:
- Agency analysis section
- Pronoun distribution visualizations
- Research insights on agency attribution

## Migration Steps

1. **Import the enhanced analyzer:**
```python
from deixis_ethical_analyzer_enhanced import DeixisEthicalAnalyzer, analyze_deictic_markers
```

2. **Use as before - it's backward compatible:**
```python
analyzer = DeixisEthicalAnalyzer()
results = analyzer.analyze_dilemma(dilemma)
```

3. **Access new metrics:**
```python
# In response data
agency_type = results['responses']['first_person']['pronoun_agency']['agency_type']
concentration = results['responses']['first_person']['pronoun_agency']['agency_concentration']

# In comparative analysis
comparison = results.get('agency_comparison', {})
```

## Example Usage

```python
# Analyze with enhanced metrics
analyzer = DeixisEthicalAnalyzer()
results = analyzer.analyze_dilemma(dilemma)

# Generate enhanced report
analyzer.generate_enhanced_report([results], "output_dir")

# Access pronoun agency data
for framing, response_data in results['responses'].items():
    agency = response_data.get('pronoun_agency', {})
    print(f"{framing}: {agency.get('agency_type')} ({agency.get('agency_concentration', 0):.3f})")
```

## Research Applications

The enhanced analyzer directly supports research questions about:
- How deixis influences agency distribution in LLM responses
- Patterns of moral responsibility attribution across framings
- Linguistic mechanisms of agency construction in AI ethics

## Backward Compatibility

The enhanced analyzer is fully backward compatible. Existing code will continue to work, with new metrics added as optional fields.
