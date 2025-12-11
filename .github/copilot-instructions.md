# Deixis Ethics Analysis Pipeline - AI Agent Guide

## Project Overview
Research framework studying how **deictic framing** (linguistic perspective markers like "I", "you", "we") influences ethical reasoning in LLMs. Pipeline generates responses across 9 deictic framings for 6 ethical dilemmas, then performs multi-dimensional analysis revealing the "Philosophy Textbook Effect" and agency distribution patterns.

## Architecture: Dual Structure

### Root Level (Core Modules)
- **Core analyzers**: `deixis_ethical_analyzer.py`, `pronoun_agency_analyzer.py`, `transformer.py`
- **LLM infrastructure**: `llm_client.py` (unified client supporting OpenAI, Anthropic, DeepSeek via OpenRouter)
- **Expert agents**: `expert_analysis_agent.py`, `critical_expert_analysis.py`, `evidence_based_expert_analysis.py`, `pronoun_agency_expert.py`
- **Data schemas**: `models/schemas.py` (DeicticFraming enum, EthicalDilemma, AgencyAnalysis, EthicalFramingAnalysis dataclasses)

### Pipeline Directory (`deixis_analysis_pipeline/`)
- **Entry points**: `run_complete_pipeline.py` (GPT-4o), `run_complete_pipeline_anthropic.py`, `run_complete_pipeline_deepseek.py`
- **Generation**: `generation_scripts/generate_responses_multi_dilemma.py` reads from `input_questions/all_dilemmas_deictic_questions.json`
- **Analysis**: `analysis_scripts/run_complete_deixis_analysis_fixed.py` auto-discovers latest generation logs
- **Outputs**: `generation_logs/multi_dilemma_[timestamp]/` → `automated_analysis_results/complete_analysis_[timestamp]/`

**Key insight**: Root modules are imported by pipeline scripts. Don't modify imports; they expect `sys.path` manipulation.

## Critical Workflows

### Running Complete Pipeline
```bash
# From project root - this is the PRIMARY command
python deixis_analysis_pipeline/run_complete_pipeline.py

# Model-specific variants
python deixis_analysis_pipeline/run_complete_pipeline_anthropic.py
python deixis_analysis_pipeline/run_complete_pipeline_deepseek.py
```

**What happens**:
1. Generates 54 responses (6 dilemmas × 9 framings) via LLM → `generation_logs/multi_dilemma_[timestamp]/`
2. Auto-discovers latest generation session
3. Runs comprehensive analysis (core + expert agents)
4. Outputs CSV, JSON, and markdown reports → `automated_analysis_results/complete_analysis_[timestamp]/`

### Manual Step-by-Step
```bash
# 1. Generate (from root)
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py

# 2. Analyze (from root) - automatically finds latest generation
python deixis_analysis_pipeline/analysis_scripts/run_complete_deixis_analysis_fixed.py

# 3. Expert analysis only (if responses exist)
python deixis_analysis_pipeline/analysis_scripts/run_expert_analysis_only.py
```

### Path Conventions
- **Always run from project root** (`c:\dev\deixisAugust2025\`)
- Generation logs: `deixis_analysis_pipeline/generation_logs/multi_dilemma_[timestamp]/`
- Analysis results: `automated_analysis_results/complete_analysis_[timestamp]/`
- Scripts use `Path(__file__).parent` to compute relative paths

## Key Components

### LLM Client (`llm_client.py`)
```python
from llm_client import UnifiedLLMClient, MODEL_CONFIGS

# Supports: gpt-4o (OpenAI), claude-3.5-sonnet, deepseek-chat (OpenRouter)
client = UnifiedLLMClient("gpt-4o")
response = await client.generate_completion(prompt, temperature=0.7)
```

### Transformer (`transformer.py`)
Converts ethical dilemmas into 9 deictic framings using `DeicticTransformer`:
- **Framings**: IMPERSONAL, SECOND_PERSON, FIRST_PERSON, REFLEXIVE, DIALOGIC, SPATIAL, TEMPORAL, COSMOLOGICAL
- **Method**: `transform_to_question(dilemma, framing)` returns interrogative question (not instruction)
- **Pattern-based**: Uses `_extract_dilemma_elements()` to pull `{actor}`, `{situation}`, `{stakes}` from description

### Pronoun Agency Analyzer (`pronoun_agency_analyzer.py`)
Quantifies agency distribution through pronoun usage:
```python
from pronoun_agency_analyzer import PronounAgencyAnalyzer

analyzer = PronounAgencyAnalyzer()
analysis = analyzer.analyze_text(response_text, text_id="fp_trolley", framing="first_person")
# Returns: pronoun_ratios, agency_concentration (Gini coefficient 0-1), agency_type
```

### Expert Analysis Agents
Multi-agent LLM-based interpretation system:
- **ExpertAnalysisAgent**: Base class, comprehensive ethical framework analysis
- **CriticalExpertAnalyzer**: Rigorous evidence quality assessment, high-confidence insights
- **EvidenceBasedExpert**: Large-scale pattern extraction, statistical significance
- **PronounAgencyExpert**: Quantitative pronoun distribution and linguistic mechanisms

## Data Flow

### Input Structure (`input_questions/all_dilemmas_deictic_questions.json`)
```json
{
  "dilemmas": [
    {
      "id": "trolley_problem",
      "title": "The Trolley Problem",
      "framings": {
        "impersonal": "What should be done when...",
        "first_person": "What should I do when I discover...",
        "second_person": "What would you do if you found...",
        // ... 6 more framings
      }
    }
  ]
}
```

### Output Structure (`automated_analysis_results/complete_analysis_[timestamp]/`)
- **comprehensive_research_data.csv**: Flat structure for statistical analysis (ANOVA, regression)
- **complete_analysis_results.json**: Full nested analysis data
- **detailed_analysis_report.md**: Human-readable findings
- **FINAL_DEIXIS_RESEARCH_REPORT.md**: Executive summary with "deixis machines" framework

## Project-Specific Conventions

### Naming Patterns
- Scripts: `run_complete_*` = full pipeline, `generate_responses_*` = LLM generation only, `run_*_analysis*` = analysis only
- Timestamps: `YYYYMMDD_HHMMSS` format consistently used across outputs
- Framings: Snake_case (`first_person`, `second_person`) matches enum values

### Error Handling
- Generation scripts: Rate limiting via `asyncio_throttle`, retry logic for API failures
- Analysis scripts: Auto-discovery of latest session, graceful degradation if expert analysis unavailable
- Unicode handling: All file I/O uses `encoding='utf-8'` explicitly (Windows PowerShell fix)

### Environment Configuration
```bash
# Required in .env
OPENAI_API_KEY=sk-...                    # For GPT-4o direct
OPENROUTER_API_KEY=sk-or-...             # For Claude/DeepSeek via OpenRouter

# Optional defaults
GENERATION_MODEL=gpt-4o                  # Model for response generation
ANALYSIS_MODEL=gpt-4o                    # Model for expert analysis
GENERATION_TEMPERATURE=0.9               # Higher creativity for responses
ANALYSIS_TEMPERATURE=0.6                 # Lower for consistent analysis
```

## Common Debugging Scenarios

### "No response files found"
Check `deixis_analysis_pipeline/generation_logs/` for directories matching `multi_dilemma_*` or `academic_integrity_*`. Analysis scripts auto-discover by timestamp.

### Import errors
Ensure running from project root. Scripts use `sys.path.append(str(Path(__file__).parent.parent))` to import root modules.

### Path issues on Windows
All paths use `Path` objects. PowerShell requires `encoding='utf-8'` for file operations with markdown/JSON.

### API rate limits
Default: 50 requests/min with 1s delay. Generating 54 responses takes ~15-30 minutes. Cost: ~$0.30-0.60 per full run.

## Key Research Findings (Context for Analysis Code)

### Philosophy Textbook Effect
Models switch from genuine reasoning (novel dilemmas) to academic recitation (trolley problem):
- GPT-4o: +1,471% philosophical references
- Claude 3.5: +233% references, 63% shorter responses
- DeepSeek: +460% references, maintains depth

**Implication**: Analysis code differentiates `philosophical_references` count and `reasoning_depth` score.

### Agency Concentration Patterns
Measured via Gini coefficient in `pronoun_agency_analyzer.py`:
- First-person: 0.8+ (concentrated individual agency)
- Cosmological: 0.3-0.4 (distributed across entities)
- Impersonal: Abstract agency, low pronoun concentration

**Implication**: `agency_concentration` metric is central to comparative analysis.

## Documentation Hierarchy
1. **Start here**: Root `README.md` (overview, quick start)
2. **Pipeline specifics**: `deixis_analysis_pipeline/COMPLETE_WORKFLOW_GUIDE.md`
3. **API setup**: `deixis_analysis_pipeline/QUICK_START_GUIDE.md`
4. **Methodology**: `ARCHIVE/PRONOUN_AGENCY_ANALYSIS_DOCUMENTATION.md`, `ARCHIVE/INTERROGATIVE_APPROACH_DOCUMENTATION.md`
5. **Troubleshooting**: `deixis_analysis_pipeline/CORRECT_COMMANDS.md`, `deixis_analysis_pipeline/PATH_VERIFICATION.md`

## When Adding Features

### New Dilemma
1. Add to `deixis_analysis_pipeline/input_questions/all_dilemmas_deictic_questions.json` with all 9 framings
2. Follow existing JSON structure: `id`, `title`, `framings` dict
3. No code changes needed—generation script reads JSON dynamically

### New Deictic Framing
1. Add to `DeicticFraming` enum in `models/schemas.py`
2. Update `transformer.py`: Add to `_initialize_question_patterns()` with pattern templates
3. Add extraction methods (e.g., `_extract_cosmic_perspective()`) if framing needs custom elements
4. Update all dilemmas in JSON with new framing

### New Analysis Metric
1. Add to appropriate analyzer class (`PronounAgencyAnalyzer`, `ExpertAnalysisAgent`, etc.)
2. Update schemas in `models/schemas.py` (e.g., add field to `AgencyAnalysis`)
3. Modify `run_complete_deixis_analysis_fixed.py` to include new metric in CSV generation
4. Document metric calculation in docstring

### New Expert Agent
1. Inherit from `ExpertAnalysisAgent` in `expert_analysis_agent.py`
2. Override `analyze_response()` with specialized prompts
3. Add to pipeline in `run_complete_deixis_analysis_fixed.py` expert analysis section
4. Export findings to JSON and integrate into final report

## Performance Notes
- Full pipeline (54 responses + analysis): 20-40 minutes, ~$0.50-0.80
- Expert analysis (LLM-based): Adds 10-15 minutes, ~$0.15-0.25
- CSV generation: Instant, no API calls (processes saved JSON)
- Bottleneck: API rate limits during generation phase
