# 🔬 Deixis Analysis Pipeline

**Complete system for analyzing deictic effects on AI ethical reasoning**

## 📁 Directory Structure

```
deixis_analysis_pipeline/
├── 📋 README.md                           # This documentation
├── 🚀 run_complete_pipeline.py            # ONE-COMMAND EXECUTION
├── 🎯 input_questions/                    # Ethical dilemma questions
│   └── academic_integrity_deictic_questions.json
├── 🤖 generation_scripts/                 # LLM response generation
│   └── generate_responses_only.py
├── 🔍 analysis_scripts/                   # Comprehensive analysis
│   └── run_complete_deixis_analysis.py
├── 🤖 llm_agents/                         # LLM-based report writers & analyzers
│   ├── expert_analysis_agent.py           # Expert interpretation agent
│   ├── critical_expert_analysis.py        # Critical evaluation analyzer
│   ├── evidence_based_expert_analysis.py  # Evidence synthesis expert
│   ├── pronoun_agency_expert.py           # Pronoun/agency specialist
│   ├── detailed_report_generator.py       # Detailed report writer
│   └── final_report_generator.py          # Executive summary generator
└── 🛠️ utilities/                          # Helper scripts
    ├── generate_missing_reports.py
    └── run_expert_analysis.py
```

## 🚀 Quick Start Guide

### Step 1: Generate LLM Responses
```bash
cd generation_scripts
python generate_responses_only.py
```
**Output:** 9 GPT-4o responses saved to `../generation_logs/`

### Step 2: Run Complete Analysis
```bash
cd ../analysis_scripts  
python run_complete_deixis_analysis.py
```
**Output:** Complete research dataset in `../automated_analysis_results/`

### Step 3: Generate Missing Reports (if needed)
```bash
cd ../utilities
python generate_missing_reports.py
```

### Step 4: Run Advanced LLM Agent Analysis (optional)
```bash
cd ../utilities
python run_expert_analysis.py
```
**Output:** Sophisticated qualitative interpretation by expert LLM agents

## 📊 What You Get

### Research Data Files:
- **📊 `comprehensive_research_data.csv`** - 50+ analysis dimensions for statistical analysis
- **💾 `complete_analysis_results.json`** - Complete raw analysis data (74KB+)
- **📄 `detailed_analysis_report.md`** - Human-readable comprehensive analysis
- **🎯 `FINAL_DEIXIS_RESEARCH_REPORT.md`** - Executive summary and key findings
- **🔬 `research_framework_analysis.md`** - Methodology documentation

### Advanced LLM Agent Reports:
- **🤖 `expert_analysis_report.json`** - Claude-3.5-Sonnet expert interpretation
- **🔍 `critical_expert_analysis.json`** - Rigorous methodological evaluation
- **📊 `evidence_based_expert_analysis.json`** - Evidence synthesis across framings
- **👤 `pronoun_agency_expert_analysis.json`** - Specialized linguistic analysis
- **📄 `pronoun_agency_expert_report.md`** - Human-readable linguistic insights
- **💾 `complete_expert_analysis_results.json`** - All expert agent outputs combined

### Analysis Dimensions:
- **Moral Reasoning Structure:** consequentialist, deontological, relational, suspended
- **Affective Stance:** assertive, deliberative, hesitant, exposed, detached
- **Indexical Coherence:** How well responses match their deictic frames
- **Agency Distribution:** Individual vs collective vs institutional focus
- **Lexical Features:** Temporal anchoring, spatial metaphors, ontological register

## 🤖 LLM Agent Analysis Suite

The pipeline includes sophisticated LLM-based agents that provide qualitative interpretation beyond quantitative metrics:

### **Expert Analysis Agents:**
- **`expert_analysis_agent.py`** - High-level interpretation using Claude-3.5-Sonnet
  - Generates comprehensive ethical reasoning analysis
  - Identifies cross-framing patterns and insights
  - Produces structured research reports

- **`critical_expert_analysis.py`** - Rigorous methodological evaluation
  - Extracts critical evidence from analysis data
  - Applies rigorous research standards
  - Generates critical insights for research questions

- **`evidence_based_expert_analysis.py`** - Evidence synthesis specialist  
  - Extracts logged evidence from analysis results
  - Synthesizes findings across multiple framings
  - Produces evidence-based research insights

- **`pronoun_agency_expert.py`** - Linguistic agency specialist
  - Deep analysis of pronoun usage patterns
  - Agency distribution interpretation
  - Specialized linguistic mechanism analysis

### **Report Generation Agents:**
- **`detailed_report_generator.py`** - Comprehensive report writer
  - Generates detailed markdown, HTML, and JSON reports
  - Integrates all analysis dimensions
  - Produces publication-ready documentation

- **`final_report_generator.py`** - Executive summary generator
  - Creates concise research summaries
  - Highlights key findings and implications
  - Generates executive-level insights

### **How LLM Agents Enhance Analysis:**
✅ **Qualitative Interpretation** - Goes beyond counting to understanding meaning  
✅ **Pattern Recognition** - Identifies subtle cross-framing relationships  
✅ **Research Insights** - Generates hypothesis and theoretical implications  
✅ **Professional Reports** - Creates publication-ready documentation  
✅ **Evidence Synthesis** - Combines quantitative and qualitative findings

## 🎯 Input Format

Create JSON files in `input_questions/` with this structure:

```json
{
  "dilemma_id": "your_dilemma_name",
  "dilemma_title": "The Dilemma Title",
  "dilemma_description": "Detailed ethical scenario...",
  "deictic_questions": {
    "impersonal": {
      "question": "When one faces this situation...",
      "deictic_markers": ["one", "that", "such"],
      "focus": "Abstract moral reasoning"
    },
    "first_person": {
      "question": "I am facing this dilemma...",
      "deictic_markers": ["I", "my", "me"],
      "focus": "Personal moral struggle"
    }
    // ... 7 more framings
  }
}
```

## 🔧 System Requirements

### Dependencies:
- Python 3.8+
- OpenAI API key (for GPT-4o)
- Required packages: `openai`, `pandas`, `asyncio`, `pathlib`

### Core Analysis Tools:
- **DeicticEthicalAnalyzer** - Main analysis orchestrator
- **PronounAgencyAnalyzer** - Linguistic analysis
- **LLM Analysis Agent** - 6 sophisticated LLM-based analysis methods
- **Expert Analysis Suite** - Advanced interpretation using Claude-3.5-Sonnet
- **Report Generation Agents** - Professional documentation writers

## 📈 Research Applications

### Academic Use:
- **Linguistic Research:** Deictic effects on moral reasoning
- **AI Ethics:** How language framing affects AI moral judgments  
- **Cognitive Science:** Embodied cognition in ethical decision-making
- **Philosophy:** Language-ethics interaction studies

### Practical Applications:
- **AI Training:** Deictic-aware ethical training protocols
- **Policy Design:** Understanding how framing affects moral judgments
- **Educational Tools:** Teaching ethical reasoning through linguistic perspective

## 🎯 Supported Deictic Framings

1. **Impersonal** - Abstract, objective language ("one", "it")
2. **Second Person** - Direct address ("you", "your")  
3. **First Person** - Personal perspective ("I", "my")
4. **Reflexive** - Self-reflective ("imagine yourself")
5. **Dialogic** - Collective language ("we", "us")
6. **Spatial** - Embodied positioning ("standing at", "direction")
7. **Temporal** - Time-focused ("now", "then", "future") 
8. **Cosmological** - Universal perspective ("ancestors watching")
9. **First Person Plural** - Shared responsibility ("we decide")

## 🔬 Analysis Pipeline

### Phase 1: Response Generation
- **Input:** Pure deictic questions (no hints/context)
- **Model:** GPT-4o at temperature 0.9 (creative)
- **Output:** 9 ethical responses (one per framing)

### Phase 2: Multi-Tool Analysis  
- **Code Analysis:** Linguistic marker counting, pronoun analysis
- **LLM Analysis:** 6 sophisticated interpretation methods (temp 0.6)
- **Integration:** Cross-framing comparative analysis

### Phase 3: Research Output
- **Quantitative:** CSV with 50+ dimensions for statistical analysis
- **Qualitative:** Detailed reports with insights and implications
- **Raw Data:** Complete JSON for further processing

## 🎯 Success Metrics

### Quality Indicators:
- **High Indexical Coherence:** Responses match their deictic frames
- **Systematic Variation:** Clear differences across framings  
- **Consistent Analysis:** Reliable pattern detection
- **Research Readiness:** Publication-quality outputs

### Example Results:
- **Academic Integrity Dilemma:** 8/9 framings showed deontological reasoning
- **Cosmological Exception:** Unique relational reasoning pattern
- **High Coherence:** Most responses properly matched deictic frames
- **Research Value:** 74KB+ of analysis data generated

## 📚 File Dependencies

### Core System Files (must be in parent directory):
- `deixis_ethical_analyzer.py` - Main analysis engine
- `pronoun_agency_analyzer.py` - Linguistic analysis
- `transformer.py` - Deictic transformation utilities
- `llm_client.py` - LLM API interface
- `models/schemas.py` - Data structures

### Expert Analysis (optional):
- `expert_analysis_agent.py`
- `critical_expert_analysis.py` 
- `evidence_based_expert_analysis.py`
- `pronoun_agency_expert.py`

## 🚀 Next Steps

1. **Expand Dilemmas:** Create JSON questions for additional ethical scenarios
2. **Cross-Domain Analysis:** Compare deictic effects across different ethical domains
3. **Multi-Model Studies:** Test with different LLMs (Claude, Gemini, etc.)
4. **Cultural Analysis:** Examine deictic effects across languages/cultures

## 📝 Citation

When using this pipeline for research, please cite:
- **Methodology:** "Deictic Effects on AI Ethical Reasoning Analysis Pipeline"
- **Key Innovation:** Multi-tool analysis combining code-based and LLM-based interpretation
- **Research Contribution:** Systematic mapping of deixis-ethics relationships in AI

---

**🎯 Ready for immediate use with any ethical dilemma!**  
**📊 Generates publication-ready research data and analysis!**  
**🔬 Complete pipeline from questions to insights!** 