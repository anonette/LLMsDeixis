# 📋 Deixis Analysis Pipeline - Setup TODO List

## Prerequisites Check
- [ ] Verify Python 3.8+ is installed
- [ ] Confirm virtual environment is activated (venv)
- [ ] Check if .env file exists with API keys

## Core Dependencies Setup
- [ ] Copy core modules from ARCHIVE to root directory:
  - [ ] `cp ARCHIVE/deixis_ethical_analyzer.py .`
  - [ ] `cp ARCHIVE/transformer.py .`
  - [ ] `cp ARCHIVE/pronoun_agency_analyzer.py .`
  - [ ] `cp ARCHIVE/analysis_logger.py .`
  - [ ] `cp ARCHIVE/llm_client.py .`
  - [ ] `cp ARCHIVE/research_framework_system.py .` (optional)

## Fix File Path Issues
- [ ] Copy JSON questions to generation scripts directory:
  ```bash
  cp deixis_analysis_pipeline/input_questions/academic_integrity_deictic_questions.json \
     deixis_analysis_pipeline/generation_scripts/
  ```
  OR
- [ ] Update generate_responses_only.py line 15 to use correct path

## Environment Configuration
- [ ] Create .env file in root if not exists
- [ ] Add OPENAI_API_KEY (required for GPT-4o)
- [ ] Add OPENROUTER_API_KEY (optional)
- [ ] Verify API keys have sufficient credits

## Install Dependencies
- [ ] Run: `pip install -r ARCHIVE/requirements.txt`
- [ ] Verify key packages installed:
  - [ ] openai
  - [ ] pandas
  - [ ] numpy
  - [ ] rich
  - [ ] python-dotenv

## Test Pipeline Components
- [ ] Test imports: `python -c "import deixis_ethical_analyzer"`
- [ ] Test generation script can find JSON file
- [ ] Verify output directories exist or will be created

## Run Pipeline
- [ ] Option 1: Run complete pipeline
  ```bash
  cd deixis_analysis_pipeline
  python run_complete_pipeline.py
  ```
- [ ] Option 2: Run phases separately
  ```bash
  python deixis_analysis_pipeline/generation_scripts/generate_responses_only.py
  python deixis_analysis_pipeline/analysis_scripts/run_complete_deixis_analysis.py
  ```

## Verify Outputs
- [ ] Check generation_logs/ for response files
- [ ] Check automated_analysis_results/ for analysis outputs
- [ ] Review generated CSV, JSON, and markdown reports

## Optional: Run Expert Analysis
- [ ] Run expert analysis for deeper insights:
  ```bash
  python deixis_analysis_pipeline/utilities/run_expert_analysis.py