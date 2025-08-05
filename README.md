# Deixis Ethics Analysis Pipeline

> A comprehensive research framework for analyzing how deictic linguistic framing affects ethical reasoning in Large Language Models

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-412991.svg)](https://openai.com/)

## 🔬 Research Overview

This pipeline investigates how **deictic framing** (linguistic perspective markers like "I", "you", "we", "here", "now") systematically influences ethical reasoning patterns in AI systems. Through controlled experiments across 9 different framings and 6 ethical dilemmas, we reveal how perspective shifts moral judgment, agency attribution, and reasoning frameworks.

### Key Research Questions
- How do deictic framings affect moral reasoning patterns?
- What is the relationship between linguistic perspective and agency attribution?
- How does framing influence emotional engagement and voice authority?
- Can we predict ethical framework preferences based on deictic markers?

## 🎯 Key Features

### **Multi-Framework Analysis**
- **9 Deictic Framings**: Impersonal, second-person, first-person, first-person plural, reflexive, dialogic, spatial, temporal, cosmological
- **6 Ethical Dilemmas**: Trolley problem, ICU allocation, AI consciousness, memory modification, scholarship fraud, whistleblowing
- **40+ Metrics**: Agency patterns, ethical frameworks, rhetorical features, pronoun distributions

### **Advanced Expert Analysis**
- **LLM-Powered Expert Agents**: Multi-perspective analysis from ethics, linguistics, and philosophy
- **Critical Evidence Assessment**: Rigorous evidence classification and insight generation  
- **Pronoun Agency Analysis**: Quantitative analysis of agency distribution through pronoun usage
- **Cross-Framing Comparisons**: Statistical analysis of patterns across perspectives

### **Research-Ready Outputs**
- Structured CSV datasets for statistical analysis
- Comprehensive JSON reports with full analysis data
- Expert insights and research recommendations
- Visualization-ready data formats

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (or OpenRouter for alternative models)
- ~$0.50-0.60 for a complete analysis run

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/anonette/LLMsDeixis.git
cd LLMsDeixis
```

2. **Set up Python environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API access**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
OPENAI_API_KEY=your_actual_api_key_here
# OR for OpenRouter
OPENROUTER_API_KEY=your_openrouter_key_here
```

### Running the Analysis

#### **Option 1: Complete Pipeline (Recommended)**
```bash
python deixis_analysis_pipeline/run_complete_pipeline.py
```
This runs the full pipeline from response generation through expert analysis.

#### **Option 2: Step-by-Step Execution**

**Generate responses:**
```bash
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py
```

**Run core analysis:**
```bash
python deixis_analysis_pipeline/analysis_scripts/run_complete_deixis_analysis_fixed.py
```

**Run expert analysis:**
```bash
python deixis_analysis_pipeline/analysis_scripts/run_expert_analysis_only.py
```

#### **Option 3: Analyze Existing Data**
We include pre-generated data for immediate analysis:
```bash
python deixis_analysis_pipeline/analysis_scripts/run_expert_analysis_only.py
```

## 📁 Project Structure

```
deixis-ethics-analysis/
├── 📂 deixis_analysis_pipeline/        # Main pipeline
│   ├── 📂 input_questions/             # Deictic framing templates
│   ├── 📂 generation_scripts/          # Response generation
│   ├── 📂 analysis_scripts/            # Core & expert analysis
│   ├── 📂 llm_agents/                  # Expert analysis agents
│   ├── 📂 utilities/                   # Helper functions
│   └── 📂 automated_analysis_results/  # Analysis outputs
├── 📂 ARCHIVE/                         # Core analysis modules
├── 📂 generation_logs/                 # Generated responses (runtime)
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .env.example                     # Environment template
├── 📄 .gitignore                       # Git ignore rules
└── 📄 README.md                        # This file
```

## 📊 Sample Data & Results

### Included Sample Analysis
We provide a complete analysis session (`complete_analysis_20250804_214222`) with:
- **54 analyzed responses** across all deictic framings
- **Expert analysis results** with comprehensive insights
- **Research-ready datasets** for immediate exploration

### Key Findings from Sample Data
- **Agency Attribution**: First-person framings concentrate agency (0.8+ concentration), while cosmological framings distribute it (0.3-0.4)
- **Ethical Frameworks**: Impersonal framings favor utilitarian reasoning, reflexive framings increase deontological patterns
- **Voice Authority**: Systematic shifts from "analyst" (impersonal) to "inner voice" (reflexive) to "moral theorist" (cosmological)
- **Pronoun Patterns**: Predictable distributions correlate with agency concentration and responsibility attribution

## 🔍 Analysis Outputs

### **Generation Phase**
**Location:** `generation_logs/multi_dilemma_YYYYMMDD_HHMMSS/`
- Individual JSON files for each dilemma-framing combination
- Session summary with generation metadata
- Cost tracking and performance metrics

### **Core Analysis Phase**  
**Location:** `automated_analysis_results/complete_analysis_YYYYMMDD_HHMMSS/`
- `comprehensive_research_data.csv` - Quantitative metrics for statistical analysis
- `core_analysis_results.json` - Full structured analysis data
- Individual detailed reports per response

### **Expert Analysis Phase**
**Location:** `automated_analysis_results/expert_analysis_only_YYYYMMDD_HHMMSS/`
- `expert_analysis_results.json` - Multi-agent expert insights
- Evidence-based insights with confidence scoring
- Research recommendations and methodological notes
- Cross-framing comparative analysis

## 🧠 Expert Analysis System

Our multi-agent expert analysis system provides sophisticated interpretation:

### **Expert Analysis Agent**
- Comprehensive ethical framework analysis
- Responsibility and agency pattern identification
- Linguistic mechanism analysis
- Philosophical implications assessment

### **Critical Expert Analyzer**
- Rigorous evidence quality assessment
- High-confidence insight generation
- Research question specific analysis
- Methodological validation

### **Evidence-Based Expert**
- Large-scale evidence extraction and indexing
- Statistical significance testing
- Pattern correlation analysis
- Reproducibility assessment

### **Pronoun Agency Expert**
- Quantitative pronoun distribution analysis
- Agency concentration scoring (Gini coefficient)
- Linguistic mechanism identification
- Cross-framing comparative metrics

## 💰 Cost Estimation

### **Complete Pipeline Run**
- **Response Generation**: ~$0.30 (54 responses across 6 dilemmas × 9 framings)
- **Core Analysis**: ~$0.10 (pattern analysis and classification)
- **Expert Analysis**: ~$0.15 (multi-agent expert interpretation)
- **Total**: ~$0.55 per complete analysis session

### **Cost Optimization**
- Use existing sample data for immediate analysis ($0)
- Run expert analysis only on pre-generated responses (~$0.15)
- Selective dilemma analysis for targeted research (~$0.10 per dilemma)

## 🔬 Research Applications

### **Academic Research**
- Computational linguistics and deixis studies
- AI ethics and moral reasoning research
- Psychology of perspective-taking
- Philosophy of language and ethics

### **AI Development**
- Bias detection in language models
- Prompt engineering optimization
- Multi-perspective reasoning systems
- Ethical AI evaluation frameworks

### **Industry Applications**
- Content moderation system evaluation
- Customer service AI assessment  
- Legal AI bias analysis
- Educational AI fairness testing

## 📈 Extending the Pipeline

### **Adding New Dilemmas**
1. Create framing templates in `input_questions/`
2. Update generation scripts to include new scenarios
3. Run generation and analysis pipeline

### **Custom Deictic Framings**
1. Design new perspective transformations
2. Add to framing templates
3. Update analysis metrics as needed

### **Additional Expert Agents**
1. Implement new expert analysis agents in `llm_agents/`
2. Add to analysis pipeline workflow
3. Configure output integration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black . --line-length 88
```

### **Research Collaboration**
Interested in collaborative research? We're open to:
- Joint publications and studies
- Dataset sharing and validation
- Methodological improvements
- Cross-institutional research projects

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Citation

If you use this pipeline in your research, please cite:

```bibtex
@software{deixis_ethics_analysis,
  title={Deixis Ethics Analysis Pipeline: A Framework for Studying Linguistic Framing Effects on AI Moral Reasoning},
  author={[Your Name]},
  year={2025},
  url={https://github.com/anonette/LLMsDeixis}
}
```

## 📞 Contact & Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for research questions
- **Email**: [your.email@institution.edu] for collaboration inquiries

## 🙏 Acknowledgments

- Built on OpenAI's GPT models for response generation and analysis
- Inspired by research in computational ethics and deixis theory
- Developed for advancing understanding of linguistic framing in AI systems

---

> **Ready to explore how language shapes AI ethics?** Start with our sample data or run your own analysis today!
