# Deixis Machines Project Structure

## 🏗️ Architecture Overview

The Deixis Machines project is a sophisticated research system for analyzing how deictic (context-dependent) linguistic structures influence ethical reasoning in Large Language Models (LLMs). The system uses a modular architecture with clear separation of concerns.

## 📁 Directory Structure

```
deixisAugust2025/
├── 🔧 Core System Components
│   ├── deixis_ethical_analyzer.py      # Main orchestrator and analysis engine
│   ├── transformer.py                  # Deictic transformation engine
│   ├── analysis_logger.py              # Rich logging and data collection
│   └── models/
│       ├── __init__.py
│       └── schemas.py                  # Data models and type definitions
│
├── 🚀 Entry Points & Runners
│   ├── run_analysis.py                 # Main automated analysis runner
│   ├── run_complete_analysis.py        # Full 10x8 analysis runner
│   ├── app.py                         # Streamlit web interface
│   ├── demo_analysis.py               # Quick demonstration
│   └── quick_demo.py                  # Installation verification
│
├── 🔬 Analysis & Reporting Components
│   ├── critical_expert_analysis.py     # Critical methodological assessment
│   ├── evidence_based_expert_analysis.py # Evidence-backed insights
│   ├── expert_analysis_agent.py        # Expert analysis base class
│   ├── research_framework_system.py    # Research question framework
│   ├── research_methods_analysis.py    # Methodological analysis
│   └── detailed_report_generator.py    # Report generation engine
│
├── 🧪 Test Suite
│   ├── test_system.py                 # System integration tests
│   ├── test_all_framings.py           # Framework testing
│   ├── test_complete_flow.py          # End-to-end flow tests
│   ├── test_models.py                 # Model testing
│   ├── test_pure_stateless.py         # Stateless operation tests
│   ├── test_rhetorical_posture.py     # Rhetorical analysis tests
│   └── test_fix_verification.py       # Fix verification tests
│
├── 📊 Utilities & Tools
│   ├── verify_real_responses.py       # Response verification
│   ├── show_real_responses.py         # Response display utility
│   ├── monitor_progress.py            # Progress monitoring
│   ├── configure_analysis.py          # Configuration utility
│   └── generate_multi_model_data.py   # Multi-model data generation
│
├── 📈 Visualization & Analysis
│   ├── temperature_flow_diagram.py     # Temperature flow visualization
│   ├── temperature_analysis.md         # Temperature analysis documentation
│   └── temperature_analysis_summary.md # Temperature analysis summary
│
├── 📝 Documentation
│   ├── README.md                      # Main project documentation
│   ├── FIX_DOCUMENTATION.md           # Fix history and documentation
│   ├── COMPLETE_FIX_SUMMARY.md        # Complete fix summary
│   ├── SYSTEM_VERIFICATION_SUMMARY.md  # System verification results
│   ├── STATELESS_LLM_FIX.md          # Stateless operation documentation
│   └── example_output_structure.md    # Output structure examples
│
├── 📦 Configuration
│   ├── requirements.txt               # Python dependencies
│   ├── .env                          # API keys (not in repo)
│   └── .gitignore                    # Git ignore rules
│
└── 📂 Output Directories
    ├── analysis_results/              # General analysis results
    ├── automated_analysis_results/    # Automated analysis sessions
    ├── complete_analysis_results/     # Complete analysis runs
    ├── multi_model_analysis_results/  # Multi-model analysis data
    └── test_analysis_results/         # Test run results
```

## 🔗 Component Relationships

### Core Flow Diagram
```
┌─────────────────────────┐
│  Ethical Dilemma DB     │
│  (10 dilemmas)          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Deictic Transformer    │
│  (8 frameworks)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  LLM Analysis Agent     │
│  (OpenRouter API)       │
│  • Temperature: 0.9/0.5 │
│  • Model rotation       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analysis Components    │
│  • Agency Analysis      │
│  • Ethical Framing      │
│  • Rhetorical Posture   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Rich Analysis Logger   │
│  • Session management   │
│  • Data persistence     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Report Generation      │
│  • Research reports     │
│  • Critical analysis    │
│  • Evidence-based      │
└─────────────────────────┘
```

## 🎯 Key Components Explained

### 1. **DeicticEthicalAnalyzer** (`deixis_ethical_analyzer.py`)
- **Purpose**: Main orchestrator that coordinates the entire analysis pipeline
- **Key Classes**:
  - `DeicticEthicalAnalyzer`: Main analyzer class
  - `LLMAnalysisAgent`: Handles LLM interactions with temperature management
  - `EthicalDilemmaDatabase`: Manages the 10 ethical dilemmas
- **Temperature Strategy**:
  - 0.9 for creative response generation
  - 0.5 for structured analysis tasks

### 2. **DeicticTransformer** (`transformer.py`)
- **Purpose**: Transforms ethical dilemmas using 8 deictic frameworks
- **Frameworks**: IMPERSONAL, SECOND_PERSON, FIRST_PERSON, REFLEXIVE, DIALOGIC, SPATIAL, TEMPORAL, COSMOLOGICAL
- **Design**: Minimal hardcoding, maximum LLM generation

### 3. **Data Models** (`models/schemas.py`)
- **DeicticFraming**: Enum for 8 framework types
- **EthicalDilemma**: Dilemma data structure
- **AgencyAnalysis**: Agency attribution analysis
- **EthicalFramingAnalysis**: Ethical framework analysis
- **DeicticAnalysisResult**: Complete analysis result

### 4. **Analysis Logger** (`analysis_logger.py`)
- **Purpose**: Comprehensive logging and data collection
- **Features**:
  - Session management with unique IDs
  - Multiple export formats (JSON, CSV, PKL)
  - Rich metadata collection
  - Research-grade data persistence

### 5. **Expert Analysis Components**
- **CriticalExpertAnalyzer**: Methodological assessment
- **EvidenceBasedExpertAnalyzer**: Concrete evidence extraction
- **ResearchFrameworkSystem**: Research question analysis
- **DetailedReportGenerator**: Publication-ready reports

## 🔄 Data Flow

1. **Input**: Ethical dilemma selected from database
2. **Transformation**: Deictic transformer applies framework
3. **Generation**: LLM generates response (temp 0.9)
4. **Analysis**: Three analysis passes (temp 0.5):
   - Agency distribution analysis
   - Ethical framework analysis
   - Rhetorical posture analysis
5. **Logging**: Rich logger captures all data
6. **Reporting**: Expert analyzers generate insights
7. **Output**: Multiple formats for different uses

## 🛠️ Configuration & Setup

### Required Environment Variables (.env)
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here  # Optional
```

### Key Dependencies
- **LLM/API**: openai, requests
- **Data**: pandas, numpy
- **NLP**: nltk, spacy
- **Web**: streamlit
- **Visualization**: matplotlib, seaborn, plotly

## 📊 Output Structure

### Session Directory Format
```
automated_analysis_results/session_YYYYMMDD_HHMMSS/
├── Reports (Markdown)
│   ├── FINAL_RESEARCH_REPORT.md
│   ├── research_report.md
│   ├── critical_analysis_report.md
│   └── evidence_based_findings.md
├── Data Files (JSON/CSV)
│   ├── raw_analysis_results.json
│   ├── comparative_reports.json
│   ├── session_data.json
│   └── deictic_analysis_*.csv
└── Metadata
    └── README_RESULTS.json
```

## 🚀 Usage Patterns

### 1. Full Research Analysis
```bash
python run_analysis.py  # Automated 10x8 analysis
```

### 2. Interactive Exploration
```bash
streamlit run app.py  # Web interface
```

### 3. Quick Testing
```bash
python quick_demo.py  # Verify installation
python demo_analysis.py  # Single analysis demo
```

### 4. Custom Analysis
```python
analyzer = DeicticEthicalAnalyzer(
    api_key="your-key",
    enable_rich_logging=True,
    output_dir="custom_results"
)
results = await analyzer.analyze_dilemma_across_frameworks("dilemma_id")
```

## 🔬 Research Design Features

1. **Zero Hardcoding**: All transformations generated by LLMs
2. **High Variability**: Temperature 0.9, model rotation, no system prompts
3. **Stateless Operation**: Each call independent for unbiased results
4. **Evidence-Based**: All insights backed by logged data
5. **Methodological Transparency**: Clear documentation of limitations

## 📈 Performance Characteristics

- **Processing Time**: ~15-30 minutes for full 10x8 analysis
- **API Calls**: 4 per dilemma-framework combination (1 generation + 3 analyses)
- **Data Volume**: ~5-10MB per complete session
- **Model Rotation**: Cycles through GPT-4, Claude 3.5, DeepSeek

## 🔍 Testing & Verification

The project includes comprehensive test coverage:
- Unit tests for individual components
- Integration tests for system flow
- Verification scripts for fixes
- Performance benchmarks
- Output validation

## 🎯 Key Innovation: Temperature Management

The dual-temperature strategy (0.9/0.5) represents a key innovation:
- **Creative tasks** (response generation) use high temperature
- **Analytical tasks** (JSON extraction) use moderate temperature
- This ensures both creative diversity and reliable analysis

See `temperature_analysis.md` for detailed analysis of this approach.