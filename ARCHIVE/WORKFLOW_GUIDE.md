# 🔄 Deixis Machines Workflow Guide

This guide provides step-by-step workflows for different use cases of the Deixis Ethical Analyzer system.

## 📋 Table of Contents
1. [Initial Setup Workflow](#initial-setup-workflow)
2. [Running Full Analysis](#running-full-analysis)
3. [Analyzing Results](#analyzing-results)
4. [Custom Analysis Workflow](#custom-analysis-workflow)
5. [Research Publication Workflow](#research-publication-workflow)
6. [Troubleshooting Workflow](#troubleshooting-workflow)

---

## 🚀 Initial Setup Workflow

### Step 1: Environment Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd deixisAugust2025

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys
```bash
# Create .env file
echo "OPENROUTER_API_KEY=sk-or-v1-your-key-here" > .env
echo "OPENAI_API_KEY=sk-proj-your-key-here" >> .env  # Optional
```

### Step 3: Verify Installation
```bash
python quick_demo.py
# Should complete without errors
```

---

## 📊 Running Full Analysis

### Option A: Command Line Analysis (Recommended)
```bash
# 1. Ensure virtual environment is active
venv\Scripts\activate

# 2. Run complete analysis
python run_analysis.py

# 3. Monitor progress (15-30 minutes)
# Watch for:
# - "Analyzing: [dilemma name]"
# - "✓ Completed N dilemmas"
# - "✓ Analysis complete!"

# 4. Find results
# Look in: automated_analysis_results/session_YYYYMMDD_HHMMSS/
```

### Option B: Web Interface
```bash
# 1. Start Streamlit
streamlit run app.py

# 2. Open browser to http://localhost:8501

# 3. Click "Run Analysis" button

# 4. Download results when complete
```

### Option C: Complete 10x8 Analysis
```bash
# For full research dataset
python run_complete_analysis.py
# Results in: complete_analysis_results/
```

---

## 📈 Analyzing Results

### Step 1: Locate Your Session
```bash
# List all sessions
ls automated_analysis_results/

# Navigate to latest session
cd automated_analysis_results/session_YYYYMMDD_HHMMSS/
```

### Step 2: Review Key Files

#### For Quick Overview:
1. Open `README.md` - Session summary
2. Read `FINAL_RESEARCH_REPORT.md` - Complete findings

#### For Detailed Analysis:
1. **Patterns**: Open `comparative_reports.json`
   - Look for agency_patterns
   - Check ethical_patterns
   - Review deictic_comparison

2. **Statistics**: Open `analysis_report_TIMESTAMP.json`
   - Session summary metrics
   - Deictic marker totals
   - Frame confidence scores

3. **Evidence**: Read `evidence_based_findings.md`
   - Concrete examples
   - Specific LLM responses

4. **Critique**: Read `critical_analysis_report.md`
   - Methodological limitations
   - Validity concerns

### Step 3: Data Analysis

#### Excel/Spreadsheet Analysis:
```bash
# Open CSV in Excel
deictic_analysis_TIMESTAMP.csv
```

#### Python Analysis:
```python
import pickle
import pandas as pd

# Load pickle file
with open('for_python_analysis_TIMESTAMP.pkl', 'rb') as f:
    data = pickle.load(f)

# Or load CSV
df = pd.read_csv('deictic_analysis_TIMESTAMP.csv')
```

#### R Analysis:
```r
# Load data
data <- read.csv("for_R_analysis_TIMESTAMP.csv")
```

---

## 🔧 Custom Analysis Workflow

### Step 1: Add Custom Dilemma
```python
# In your script:
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemma

# Create custom dilemma
custom_dilemma = EthicalDilemma(
    id="custom_1",
    title="Your Dilemma",
    description="Detailed description...",
    domain="ethics_domain",
    complexity_score=7.5,
    source="custom",
    tags=["tag1", "tag2"]
)

# Add to analyzer
analyzer = DeicticEthicalAnalyzer()
analyzer.dilemma_db.add_dilemma(custom_dilemma)
```

### Step 2: Run Specific Analysis
```python
# Analyze single dilemma
results = await analyzer.analyze_dilemma_across_frameworks("custom_1")

# Or specific framework
result = await analyzer._analyze_single_framework(
    custom_dilemma, 
    DeicticFraming.FIRST_PERSON
)
```

### Step 3: Export Results
```python
# Save to custom location
analyzer.export_results("my_custom_results.json")
```

---

## 📚 Research Publication Workflow

### Step 1: Gather Publication Materials
```bash
# From your session folder, collect:
1. FINAL_RESEARCH_REPORT.md      # Main findings
2. research_report.md             # Detailed tables
3. evidence_based_findings.md     # Supporting examples
4. critical_analysis_report.md    # Limitations section
```

### Step 2: Extract Key Elements

#### For Methods Section:
- Copy methodology from `FINAL_RESEARCH_REPORT.md`
- Include temperature strategy from `temperature_analysis.md`
- Add framework descriptions from `README.md`

#### For Results Section:
- Tables from `research_report.md`
- Statistics from `analysis_report_*.json`
- Visualizations from reports

#### For Discussion:
- Insights from `evidence_based_findings.md`
- Limitations from `critical_analysis_report.md`

### Step 3: Generate Citations
```bibtex
@software{deixis_machines_2025,
  title={Deixis Machines: Exploring Distributed Agency in LLMs},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/deixis-machines}
}
```

---

## 🔍 Troubleshooting Workflow

### Issue: "Module not found"
```bash
# Solution:
venv\Scripts\activate  # Activate environment
pip install -r requirements.txt  # Reinstall
```

### Issue: "API key error"
```bash
# Check .env file
cat .env
# Should show: OPENROUTER_API_KEY=sk-or-v1-...
```

### Issue: "Analysis taking too long"
```bash
# Start with smaller test
python demo_analysis.py  # Single dilemma

# Check API credits
# Visit openrouter.ai to verify balance
```

### Issue: "JSON parsing error"
```python
# Check specific file
import json
with open('problem_file.json', 'r') as f:
    data = json.load(f)  # Will show exact error
```

---

## 📊 Understanding Output Files

### File Types and Uses:
| File Pattern | Format | Use Case |
|-------------|--------|----------|
| `*.md` | Markdown | Human reading, publications |
| `*.json` | JSON | Programmatic analysis |
| `*.csv` | CSV | Excel, statistical software |
| `*.pkl` | Pickle | Python data science |

### Processing Pipeline:
```
1. Run Analysis → 2. Generate Outputs → 3. Review Reports → 4. Analyze Data
     ↓                    ↓                    ↓                  ↓
run_analysis.py    15+ files created    Read .md files    Load .json/.csv
```

---

## 🎯 Best Practices

1. **Always activate virtual environment** before running
2. **Check API credits** before large analyses
3. **Start with demo** to verify setup
4. **Keep sessions organized** - don't modify output files
5. **Document custom changes** for reproducibility

## 📞 Getting Help

1. Check error messages carefully
2. Review relevant documentation file
3. Try quick_demo.py to isolate issues
4. Examine log files in session folder

---

This workflow guide covers the complete lifecycle from setup through publication. Each workflow is designed to be followed step-by-step for reliable results.