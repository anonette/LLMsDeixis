# Deixis-Based Ethical Analysis System

A comprehensive research framework for studying how deictic framing influences moral reasoning and agency distribution in AI language models.

## Overview

This system analyzes how different linguistic framings (deixis) systematically influence ethical decision-making in LLMs. It includes:

- **Interrogative transformation** (direct questions, not instructions)
- **Multi-framing analysis** (first-person, second-person, dialogic, impersonal, cosmological)
- **Pronoun-based agency analysis** (quantifying moral responsibility distribution)
- **Expert LLM agents** (critical, evidence-based, and pronoun agency experts)
- **Comprehensive reporting** with visualizations

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone [repository-url]
cd deixisAugust2025

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
```

### 2. Run Complete Analysis Pipeline

The most comprehensive analysis with final paper-ready report:

```bash
python run_complete_deixis_analysis.py
```

This single command will:
1. Load ethical dilemmas
2. Transform them to interrogative questions for each framing
3. Generate LLM responses across 8 deictic framings
4. Analyze deixis patterns
5. Calculate pronoun agency metrics
6. Measure ethical consistency
7. Run all expert analyses
8. Generate comprehensive reports with visualizations
9. **Create final paper-ready report linking all analyses**

### Alternative Runners

```bash
# With pronoun agency but without final report
python run_analysis_with_pronoun_agency.py

# With consistency analysis
python run_analysis_with_consistency.py
```

## Step-by-Step Workflow

### Step 1: Prepare Ethical Dilemmas

Create or modify `ethical_dilemmas.json`:

```json
{
  "dilemmas": [
    {
      "id": "whistleblowing_tech",
      "title": "Tech Company Whistleblowing",
      "description": "You discover your company is secretly collecting user data...",
      "ethical_dimensions": ["privacy", "loyalty", "transparency"]
    }
  ]
}
```

### Step 2: Generate Responses and Analysis

```bash
# Run the enhanced analysis pipeline
python run_analysis_with_pronoun_agency.py
```

Output will be in: `automated_analysis_results/session_YYYYMMDD_HHMMSS/`

### Step 3: Review Results

Navigate to the session directory to find:

```
automated_analysis_results/session_20250803_093045/
├── FINAL_DEIXIS_MACHINES_REPORT.md     # 📄 Paper-ready comprehensive report
├── REPORTS_INDEX.md                    # 📄 Navigation guide to all reports
├── all_results.json                    # Raw analysis data
├── session_data_complete.json          # Enhanced with all analyses
├── research_report.md                  # Main findings
├── pronoun_agency_analysis.md          # Detailed agency analysis
├── ethical_consistency_analysis.md     # Consistency measurements
├── critical_analysis_report.md         # Critical evaluation
├── evidence_based_findings.md          # Evidence-based insights
├── pronoun_agency_analysis_*.png       # Visualizations
└── analysis_summary.json               # Quick overview
```

## Understanding the Analysis

### Pronoun Agency Metrics

Each response is analyzed for:
- **Pronoun ratios**: Distribution of I/you/we/they/one
- **Agency concentration**: How focused vs distributed (0-1 scale)
- **Agency type**: individual/reader/collective/abstract/other

### Example Results

```
First-person framing:
- Pronouns: 89% I/me/my
- Agency: Individual (concentrated on speaker)
- Concentration: 0.85

Second-person framing:
- Pronouns: 83% you/your
- Agency: Reader (transferred to decision-maker)
- Concentration: 0.68
```

## Advanced Usage

### Run Individual Components

```bash
# Test pronoun analyzer
python test_pronoun_agency.py

# Test interrogative transformation
python test_interrogative_approach.py

# Analyze existing data
python analyze_agency_in_existing_data.py

# Demonstrate research alignment
python demonstrate_research_alignment.py
```

### Custom Analysis

```python
from deixis_ethical_analyzer_enhanced import DeixisEthicalAnalyzer

# Initialize with custom settings
analyzer = DeixisEthicalAnalyzer(
    model_name="gpt-4",      # or "gpt-3.5-turbo", "claude-2"
    temperature=0.7          # 0.0-1.0, higher = more creative
)

# Analyze a single dilemma
results = analyzer.analyze_dilemma(dilemma)

# Access pronoun agency data
agency_data = results['responses']['first_person']['pronoun_agency']
print(f"Agency type: {agency_data['agency_type']}")
print(f"Concentration: {agency_data['agency_concentration']}")
```

### Batch Processing

For large-scale analysis:

```python
# Process multiple dilemma files
import glob

dilemma_files = glob.glob("dilemmas/*.json")
for file in dilemma_files:
    # Run analysis on each file
    analyzer.analyze_file(file)
```

## Research Applications

### Testing Hypotheses

The system directly tests research hypotheses such as:
- H1a: First-person deixis → personal responsibility focus
- H1b: Impersonal deixis → abstract reasoning
- H1c: Cosmological deixis → relational frameworks

### Statistical Analysis

Export data for statistical software:

```python
# Export for R
df.to_csv("pronoun_agency_data.csv")

# Export for SPSS
df.to_excel("pronoun_agency_data.xlsx")
```

### Cross-Model Comparison

```bash
# Compare different models
python compare_models.py --models gpt-4 gpt-3.5-turbo claude-2
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```bash
   # Check .env file exists and contains:
   OPENROUTER_API_KEY=your-actual-key
   ```

2. **Import Errors**
   ```bash
   # Ensure all dependencies installed:
   pip install -r requirements.txt
   ```

3. **Memory Issues**
   - Process dilemmas in smaller batches
   - Reduce number of concurrent API calls

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Project Structure

```
deixisAugust2025/
├── Core Analysis
│   ├── deixis_ethical_analyzer.py          # Original analyzer
│   ├── deixis_ethical_analyzer_enhanced.py # With pronoun analysis
│   ├── pronoun_agency_analyzer.py          # Pronoun ratio analysis
│   └── transformer_interrogative.py        # Question transformation
│
├── Expert Agents
│   ├── expert_analysis_agent.py            # Base expert class
│   ├── pronoun_agency_expert.py            # Pronoun analysis expert
│   ├── critical_expert_analysis.py         # Critical evaluation
│   └── evidence_based_expert_analysis.py   # Evidence analysis
│
├── Runners
│   ├── run_analysis.py                     # Original runner
│   ├── run_analysis_with_pronoun_agency.py # Enhanced runner
│   └── analyze_agency_in_existing_data.py  # Batch processor
│
├── Tests & Demos
│   ├── test_pronoun_agency.py              # Test pronoun analyzer
│   ├── test_interrogative_approach.py      # Test transformations
│   └── demonstrate_research_alignment.py   # Research demo
│
└── Documentation
    ├── README.md                           # This file
    ├── INTEGRATED_WORKFLOW_GUIDE.md        # Detailed workflow
    ├── PRONOUN_AGENCY_ANALYSIS_DOCUMENTATION.md
    └── INTERROGATIVE_APPROACH_DOCUMENTATION.md
```

## Key Features

- **Zero-hardcoding approach**: Patterns emerge from data, not predefined rules
- **Interrogative transformation**: Direct questions instead of instructions
- **Pronoun-based agency analysis**: Quantifies moral responsibility distribution
- **Ethical consistency measurement**: Tracks coherence across framings
- **Multi-expert analysis**: Critical, evidence-based, and pronoun agency perspectives
- **Statistical readiness**: Data formatted for ANOVA, regression, chi-square tests
- **Publication-ready**: Final report synthesizes all analyses for academic papers
- **"Deixis Machines" framework**: Theoretical contribution to AI ethics

## Final Report

After running the complete analysis, the system generates:

**`FINAL_DEIXIS_MACHINES_REPORT.md`** - A comprehensive paper-ready document that:
- Synthesizes all component analyses
- Presents the "deixis machines" theoretical framework
- Shows how LLMs produce coherence through enunciative recalibration
- Discusses ethical implications (simulated empathy, misattributed authority)
- Positions humans as "machine shamans" navigating epistemic uncertainty
- Links to all supporting reports and data

**`REPORTS_INDEX.md`** - Navigation guide to all generated reports

## Citation

If you use this system in your research, please cite:

```bibtex
@software{deixis_ethical_analysis,
  title = {Deixis-Based Ethical Analysis System},
  author = {[Your Name]},
  year = {2025},
  url = {[repository-url]}
}
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

[Your chosen license]

## Contact

For questions or collaboration: [your-email]

---

## 📚 Complete Analysis System with Final Report

### The "Deixis Machines" Paper Generator

The system now includes a comprehensive final report generator that synthesizes all analyses into a paper-ready document demonstrating how LLMs function as "deixis machines."

#### Running the Complete Pipeline with Final Report

```bash
python run_complete_deixis_analysis.py
```

This enhanced runner adds to the existing analyses:
- **Final paper generation** linking all reports
- **Theoretical framework** presentation
- **Research synthesis** ready for publication

#### What the Final Report Contains

The **`FINAL_DEIXIS_MACHINES_REPORT.md`** includes:

1. **Abstract & Introduction**
   - Research questions and key contributions
   - The "deixis machines" concept

2. **Theoretical Framework**
   - Deixis and enunciation theory (Benveniste)
   - Cosmological perspectivism (Viveiros de Castro)
   - LLMs as systems that produce coherence through coordinate recalibration

3. **Empirical Results**
   - Pronoun distribution patterns by framing
   - Agency concentration metrics
   - Consistency scores and their implications

4. **Discussion**
   - How LLMs maintain coherence without comprehension
   - Agency as a linguistic effect, not genuine moral commitment
   - The influence of framing on ethical conclusions

5. **Ethical Implications**
   - **Simulated empathy**: First-person pronouns create false intimacy
   - **Misattributed authority**: Second-person framings suggest expertise
   - **Moral reasoning without accountability**: No consequences for AI advice
   - **The human as "machine shaman"**: Navigating meaning under radical uncertainty

6. **Appendices**
   - Links to all component reports
   - Raw data files for further analysis
   - Example responses demonstrating effects

### Reports Index

The system also generates **`REPORTS_INDEX.md`** providing:
- Navigation guide to all reports
- Summary of key findings
- Quick access to data files
- Citation information

### Research Impact

This complete system provides:
- **Quantifiable evidence** of how deixis shapes AI moral reasoning
- **Theoretical innovation** in understanding LLMs as deixis machines
- **Practical implications** for AI ethics and deployment
- **Publication-ready** documentation and analysis

The final report synthesizes months of research into a coherent narrative showing that "changes in deictic framing significantly affect how agency and responsibility are articulated" in LLM responses, with profound implications for AI ethics and human-AI interaction.
