# Complete Deixis Analysis Workflow with Pronoun Agency

This guide explains how to run the full analysis pipeline: question transformation, response generation, deixis analysis, and pronoun agency reporting.

## Overview of the Complete Pipeline

```
1. Ethical Dilemmas → 2. Interrogative Transformation → 3. LLM Response Generation
→ 4. Deixis Analysis → 5. Pronoun Agency Analysis → 6. Comprehensive Reporting
```

## Step-by-Step Instructions

### Step 1: Prepare Your Ethical Dilemmas

Create a JSON file with your ethical dilemmas:

```json
{
  "dilemmas": [
    {
      "id": "whistleblowing_tech",
      "title": "Tech Company Whistleblowing",
      "description": "You discover your company is secretly collecting user data beyond what users consented to. Reporting this would likely end your career but protect millions of users.",
      "ethical_dimensions": ["privacy", "loyalty", "transparency", "personal_cost"]
    }
  ]
}
```

### Step 2: Run the Complete Analysis

Use the enhanced analyzer that includes pronoun agency:

```python
# run_complete_analysis_enhanced.py
from deixis_ethical_analyzer_enhanced import DeixisEthicalAnalyzer
import json
from datetime import datetime
import os

def run_full_analysis():
    """Run complete analysis with all enhancements."""
    
    # Initialize enhanced analyzer
    analyzer = DeixisEthicalAnalyzer(
        model_name="gpt-4",  # or your preferred model
        temperature=0.7
    )
    
    # Load dilemmas
    with open('ethical_dilemmas.json', 'r') as f:
        dilemmas_data = json.load(f)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"analysis_results/session_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Analyze each dilemma
    all_results = []
    
    for dilemma in dilemmas_data['dilemmas']:
        print(f"\nAnalyzing: {dilemma['title']}")
        print("="*60)
        
        # This will:
        # 1. Transform to interrogative questions for each framing
        # 2. Generate LLM responses
        # 3. Analyze deixis patterns
        # 4. Calculate pronoun agency metrics
        results = analyzer.analyze_dilemma(dilemma)
        
        # Show pronoun agency results
        if 'responses' in results:
            print("\nPronoun Agency Analysis:")
            for framing, data in results['responses'].items():
                if 'pronoun_agency' in data:
                    agency = data['pronoun_agency']
                    print(f"\n{framing.upper()}:")
                    print(f"  Question: {data.get('transformed_prompt', 'N/A')[:50]}...")
                    print(f"  Agency Type: {agency['agency_type']}")
                    print(f"  Concentration: {agency['agency_concentration']:.3f}")
                    print(f"  Dominant Pronoun: {agency['dominant_pronoun']}")
                    print(f"  Total Pronouns: {agency['total_pronouns']}")
        
        all_results.append(results)
    
    # Save raw results
    with open(f"{output_dir}/all_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Generate comprehensive reports
    print("\n\nGenerating Reports...")
    print("="*60)
    
    # This creates multiple report files including agency analysis
    analyzer.generate_enhanced_report(all_results, output_dir)
    
    print(f"\nAnalysis complete! Results saved to: {output_dir}/")
    print("\nGenerated files:")
    print(f"  - {output_dir}/all_results.json (raw data)")
    print(f"  - {output_dir}/research_report.md (main report)")
    print(f"  - {output_dir}/agency_analysis_report.md (pronoun agency report)")
    print(f"  - {output_dir}/agency_distribution.png (visualization)")
    
    return output_dir, all_results

if __name__ == "__main__":
    output_dir, results = run_full_analysis()
```

### Step 3: Run Batch Analysis on Existing Data

If you have existing analysis results without pronoun metrics:

```python
# batch_analyze_existing.py
from analyze_agency_in_existing_data import main as analyze_existing

# This will:
# 1. Find all existing analysis sessions
# 2. Add pronoun agency analysis to each
# 3. Generate comparative reports
# 4. Create comprehensive visualizations

analyze_existing()
```

### Step 4: Understanding the Output

#### A. Main Research Report (`research_report.md`)
Contains:
- Deixis analysis results
- Response patterns by framing
- Ethical reasoning characteristics
- **NEW**: Pronoun agency summary

#### B. Agency Analysis Report (`agency_analysis_report.md`)
Contains:
- Pronoun distribution statistics
- Agency concentration scores
- Agency type classifications
- Comparative analysis across framings

#### C. Visualizations (`agency_distribution.png`)
Four-panel visualization showing:
1. Agency concentration by framing
2. Pronoun usage heatmap
3. Agency type distribution
4. Temporal patterns

#### D. Raw Data (`all_results.json`)
Complete data including:
```json
{
  "dilemma_id": "whistleblowing_tech",
  "responses": {
    "first_person": {
      "transformed_prompt": "You discover... What do you do?",
      "response": "I would have to report this...",
      "deixis_analysis": { ... },
      "pronoun_agency": {
        "total_pronouns": 15,
        "agency_concentration": 0.85,
        "agency_type": "individual",
        "dominant_pronoun": "first_singular",
        "pronoun_ratios": {
          "first_singular": 0.80,
          "second_person": 0.13,
          "first_plural": 0.07,
          "third_person": 0.0,
          "impersonal": 0.0
        }
      }
    }
  }
}
```

## Quick Start Commands

### 1. Test the System
```bash
# Test pronoun analyzer
python test_pronoun_agency.py

# Test interrogative transformation
python test_interrogative_approach.py
```

### 2. Run Full Analysis
```bash
# Create your dilemmas file
echo '{"dilemmas": [{"id": "test", "title": "Test Dilemma", "description": "A test ethical scenario"}]}' > ethical_dilemmas.json

# Run analysis
python run_complete_analysis_enhanced.py
```

### 3. Analyze Existing Data
```bash
python analyze_agency_in_existing_data.py
```

## Integration Points

### Using Individual Components

1. **Just Pronoun Analysis**:
```python
from pronoun_agency_analyzer import PronounAgencyAnalyzer
analyzer = PronounAgencyAnalyzer()
result = analyzer.analyze_text("I must act on this.")
```

2. **Just Interrogative Transformation**:
```python
from transformer_interrogative import InterrogativeTransformer
transformer = InterrogativeTransformer()
question = transformer.transform("Consider the implications", "first_person")
```

3. **Enhanced Deixis Analysis**:
```python
from integrate_pronoun_analyzer import analyze_deictic_markers_with_agency
analysis = analyze_deictic_markers_with_agency("I believe we should...")
```

## Customization Options

### Model Selection
```python
analyzer = DeixisEthicalAnalyzer(
    model_name="gpt-4",  # or "gpt-3.5-turbo", "claude-2", etc.
    temperature=0.7      # 0.0-1.0, higher = more creative
)
```

### Framing Selection
Modify which framings to analyze:
```python
analyzer.framings = ["first_person", "second_person", "dialogic"]  # Skip others
```

### Custom Dilemma Sources
```python
# From CSV
dilemmas = load_dilemmas_from_csv("dilemmas.csv")

# From database
dilemmas = load_dilemmas_from_db(connection)

# Programmatically
dilemma = {
    "id": f"generated_{timestamp}",
    "title": "Dynamic Dilemma",
    "description": generate_scenario()
}
```

## Troubleshooting

### No API Key Error
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Or create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Memory Issues with Large Datasets
Use batch processing:
```python
for batch in chunks(dilemmas, size=10):
    results = analyzer.analyze_batch(batch)
    save_intermediate_results(results)
```

## Research Applications

This integrated system enables:

1. **Quantitative Analysis**: Measure how linguistic framing affects moral agency
2. **Comparative Studies**: Compare agency patterns across models/temperatures
3. **Pattern Discovery**: Identify systematic biases in AI ethical reasoning
4. **Hypothesis Testing**: Test specific predictions about deixis and agency

## Next Steps

1. Run analysis on your ethical dilemmas
2. Review the agency distribution patterns
3. Compare results across different models
4. Generate publication-ready visualizations
5. Export data for statistical analysis

The complete integration provides end-to-end analysis from ethical scenarios to quantified agency metrics, directly answering how deixis influences moral responsibility attribution in AI systems.