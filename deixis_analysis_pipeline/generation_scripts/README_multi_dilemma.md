# Multi-Dilemma Response Generation Script

This script (`generate_responses_multi_dilemma.py`) processes multiple ethical dilemmas from a comprehensive JSON file, generating responses for each dilemma across all 9 deictic framings.

## Features

- **Batch Processing**: Process multiple dilemmas in a single run
- **Selective Processing**: Choose specific dilemmas by ID
- **Comprehensive Output**: Generates individual response files for each dilemma
- **Session Management**: Creates complete session data with statistics
- **Rate Limiting Protection**: Built-in delays between API calls
- **Error Handling**: Continues processing even if individual responses fail

## Usage

### Process All Dilemmas
```bash
python generate_responses_multi_dilemma.py
```

### Process Specific Dilemmas
```bash
python generate_responses_multi_dilemma.py --dilemmas whistleblower_risk icu_bed_allocation
```

### Use Custom JSON File
```bash
python generate_responses_multi_dilemma.py --json-path ../input_questions/all_dilemmas_deictic_questions.json
```

## Input Format

The script expects a JSON file with the following structure:
```json
{
  "dilemmas": [
    {
      "dilemma_id": "unique_id",
      "dilemma_title": "Title",
      "dilemma_description": "Full description...",
      "ethical_dimensions": {
        "trade_offs": [...],
        "moral_theory_tensions": [...]
      },
      "deictic_questions": {
        "impersonal": {
          "question": "...",
          "deictic_markers": [...],
          "focus": "..."
        },
        // ... other framings
      }
    }
  ]
}
```

## Output Structure

```
generation_logs/
└── multi_dilemma_YYYYMMDD_HHMMSS/
    ├── whistleblower_risk_responses.json
    ├── scholarship_fraud_responses.json
    ├── icu_bed_allocation_responses.json
    ├── trolley_problem_responses.json
    ├── ai_consciousness_responses.json
    ├── memory_modification_responses.json
    ├── complete_session_data.json
    └── generation_summary.json
```

## Output Files

### Individual Dilemma Response Files
Each `{dilemma_id}_responses.json` contains:
- Dilemma metadata (id, title, description)
- Ethical dimensions (if provided)
- All 9 deictic responses with:
  - The deictic question asked
  - Deictic markers identified
  - Framing focus
  - Generated response
  - Generation time and metadata

### Session Data File
`complete_session_data.json` contains:
- Session metadata
- List of all dilemmas processed
- Complete responses for all dilemmas
- Aggregate statistics

### Summary File
`generation_summary.json` contains:
- Session information
- Summary of each dilemma processed
- Overall statistics
- Research design information

## Requirements

- Python 3.8+
- OpenAI API key (for GPT-4o)
- Required modules in parent directory:
  - `deixis_ethical_analyzer.py`
  - `transformer.py`
  - Related dependencies

## Configuration

- **Model**: GPT-4o (OpenAI direct)
- **Temperature**: 0.9 (high for diverse responses)
- **Rate Limiting**: 
  - 1 second between framings
  - 2 seconds between dilemmas

## Example Commands

### Process All 6 Dilemmas
```bash
cd deixis_analysis_pipeline/generation_scripts
python generate_responses_multi_dilemma.py --json-path ../input_questions/all_dilemmas_deictic_questions.json
```

### Process Only Trolley Problem and AI Consciousness
```bash
python generate_responses_multi_dilemma.py --dilemmas trolley_problem ai_consciousness
```

### Estimated Time and Cost
- **Time**: ~2-3 minutes per dilemma (9 framings × 10-15 seconds each)
- **Cost**: ~$0.10-0.20 per dilemma (depending on response length)
- **Total for 6 dilemmas**: ~15-20 minutes, $0.60-1.20

## Troubleshooting

### Module Import Errors
If you get import errors, ensure:
1. You're running from the correct directory
2. Parent directory modules are copied from ARCHIVE
3. Virtual environment is activated

### API Key Errors
Ensure your `.env` file contains:
```
OPENAI_API_KEY=your-key-here
```

### Rate Limiting
If you encounter rate limit errors:
- Increase delays in the script
- Process fewer dilemmas at once
- Check your OpenAI API usage limits