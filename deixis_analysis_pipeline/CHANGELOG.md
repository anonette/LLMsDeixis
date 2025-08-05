# Changelog

All notable changes to the Deixis Analysis Pipeline project are documented here.

## [1.0.0] - 2025-08-05

### Added
- Initial release of the Deixis Analysis Pipeline
- Multi-model support for GPT-4o, Claude 3.5 Sonnet, and DeepSeek
- Generation scripts for all three models via OpenRouter API
- Comprehensive analysis framework with core and expert analysis components
- Trolley problem comparative analysis across all models
- Consolidated reporting system with visualization summaries
- Complete documentation suite including workflow guides and research design

### Key Features
- **Generation Pipeline**
  - `generate_responses_multi_dilemma.py` - GPT-4o response generation
  - `generate_responses_anthropic.py` - Claude 3.5 Sonnet via OpenRouter
  - `generate_responses_deepseek.py` - DeepSeek via OpenRouter
  - Support for 6 ethical dilemmas across 9 deictic framings

- **Analysis Pipeline**
  - `run_complete_deixis_analysis.py` - Full analysis with core and expert components
  - `analyze_trolley_all_models.py` - Specialized trolley problem comparison
  - `run_deepseek_analysis_simple.py` - Simplified analysis for DeepSeek
  - `consolidate_all_reports.py` - Report consolidation and organization

- **Analysis Components**
  - Core analysis: agency, ethics, voice, reasoning, affect, coherence
  - Expert analysis: pattern detection, critical assessment, evidence quality
  - Pronoun agency analysis
  - Comparative framework analysis

### Discovered
- **Philosophy Textbook Effect**: All models show dramatic increases in philosophical references for well-known dilemmas
  - GPT-4o: +1,471% increase
  - Claude 3.5: +233% increase
  - DeepSeek: +460% increase
- Models switch from genuine reasoning to academic recitation for familiar problems
- Novel dilemmas elicit more authentic ethical reasoning

### Fixed
- JSON structure compatibility between different model outputs
- Method name mismatches in analysis agents
- Data serialization issues with numpy types
- Response parsing for nested JSON structures

### Documentation
- Comprehensive README with quick start guide
- Complete workflow documentation
- Research design documentation
- Model comparison findings
- Trolley problem analysis summary
- Visualization summaries

### Technical Details
- Temperature settings: 0.9 for generation, 0.6 for analysis
- Async processing for efficient API calls
- Robust error handling and retry logic
- Comprehensive logging system

## Contributors
- Initial development and research design
- Multi-model implementation
- Analysis framework development
- Documentation and reporting

---

For detailed commit history, see the git log.