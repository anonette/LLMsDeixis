# GitHub Setup Instructions

## Overview
This document provides step-by-step instructions for pushing the Deixis Analysis Pipeline to GitHub.

## Files Prepared for GitHub

### 1. Documentation Files
- **README_GITHUB.md** - Main repository README (rename to README.md before pushing)
- **CHANGELOG.md** - Complete changelog of the project
- **LICENSE** - MIT License
- **requirements.txt** - Python dependencies
- **.gitignore** - Excludes sensitive data and large files

### 2. Key Directories to Include
- **CONSOLIDATED_REPORTS/** - All analysis findings and visualizations
- **generation_scripts/** - Scripts for generating model responses
- **analysis_scripts/** - Scripts for analyzing responses
- **llm_agents/** - Analysis agent implementations
- **input_questions/** - Ethical dilemmas and deictic framings

### 3. Excluded from Git (via .gitignore)
- **generation_logs/** - Raw model responses (too large)
- **automated_analysis_results/** - Intermediate analysis files
- **venv/** - Python virtual environment
- **.env** - API keys and secrets

## Step-by-Step GitHub Setup

### 1. Prepare the Repository
```bash
cd deixis_analysis_pipeline
mv README_GITHUB.md README.md
```

### 2. Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: Deixis Analysis Pipeline - Multi-Model Ethical Reasoning Study"
```

### 3. Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name it: `deixis-analysis-pipeline`
4. Description: "Analysis pipeline studying how LLMs respond to ethical dilemmas across deictic framings"
5. Keep it public (or private if preferred)
6. Don't initialize with README (we have one)

### 4. Connect and Push
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/deixis-analysis-pipeline.git
git branch -M main
git push -u origin main
```

### 5. Add Topics/Tags on GitHub
After pushing, add these topics to your repository:
- `llm`
- `ethics`
- `ai-ethics`
- `gpt-4`
- `claude`
- `deepseek`
- `deixis`
- `nlp`
- `research`

## Important Notes

### API Keys
- Never commit API keys
- Users should create their own `.env` file with:
```
OPENAI_API_KEY=their-key
OPENROUTER_API_KEY=their-key
```

### Large Files
- Generation logs are excluded (too large for GitHub)
- Only consolidated reports and analysis results are included
- Users can regenerate responses using the provided scripts

### Citation
Encourage users to cite the repository:
```bibtex
@software{deixis_analysis_pipeline,
  title = {Deixis Analysis Pipeline: Multi-Model Ethical Reasoning Study},
  year = {2025},
  url = {https://github.com/YOUR_USERNAME/deixis-analysis-pipeline}
}
```

## Repository Structure Summary
```
deixis-analysis-pipeline/
├── README.md                      # Main documentation
├── CHANGELOG.md                   # Version history
├── LICENSE                        # MIT License
├── requirements.txt               # Dependencies
├── .gitignore                     # Git exclusions
├── CONSOLIDATED_REPORTS/          # All findings
│   ├── MODEL_COMPARISON_FINDINGS.md
│   ├── TROLLEY_PROBLEM_COMPLETE_SUMMARY.md
│   └── visualizations/
├── generation_scripts/            # Response generation
├── analysis_scripts/              # Analysis tools
├── llm_agents/                    # Analysis agents
└── input_questions/               # Dilemmas & framings
```

## Next Steps After GitHub Push

1. **Add a Release**
   - Tag: v1.0.0
   - Title: "Initial Release - Multi-Model Deixis Analysis"
   - Attach key findings PDF if desired

2. **Update README if needed**
   - Add your contact information
   - Update citation with your username
   - Add any additional acknowledgments

3. **Consider GitHub Pages**
   - Host the consolidated reports as a website
   - Create visualizations dashboard

4. **Enable Issues**
   - Allow community feedback
   - Track feature requests

## Contact
For questions about the setup process, please open an issue on the repository.