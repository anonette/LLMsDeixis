# Model-Specific Deixis Analysis Guide

This guide documents the new model-specific analysis workflow that allows running separate, complete analyses with different LLM models.

## Overview

The updated system now supports running independent analyses with three models:
- **GPT-4o** (via OpenAI API)
- **Claude-3.5-sonnet** (via OpenRouter)
- **DeepSeek-chat** (via OpenRouter)

Each model runs a complete analysis session, generating its own reports and data, with a final cross-model comparison.

## Key Components

### 1. Unified LLM Client (`llm_client.py`)

A unified client that supports both OpenAI direct API and OpenRouter:

```python
from llm_client import UnifiedLLMClient

# Initialize client for specific model
client = UnifiedLLMClient("gpt-4o")  # or "claude-3.5-sonnet", "deepseek-chat"
```

**Features:**
- Automatic API selection based on model
- Model-specific configurations (context windows, max tokens)
- Environment variable support for API keys
- Consistent interface across providers

### 2. Single-Model Analyzer (`deixis_ethical_analyzer_single_model.py`)

Modified analyzer that uses a single model throughout the analysis:

```python
from deixis_ethical_analyzer_single_model import SingleModelDeicticAnalyzer

analyzer = SingleModelDeicticAnalyzer(
    model_name="gpt-4o",
    enable_rich_logging=True,
    output_dir="automated_analysis_results"
)
```

**Key Changes:**
- Removed model rotation logic
- Added model-specific output directories
- Enhanced session metadata with model information

### 3. Model-Specific Runner (`run_model_specific_analysis.py`)

Orchestrates the complete analysis workflow:

```python
python run_model_specific_analysis.py --num-dilemmas 5 --models gpt-4o claude-3.5-sonnet deepseek-chat
```

**Features:**
- Runs complete analysis for each model
- Generates model-specific reports
- Creates cross-model comparison
- Shared dilemma set for fair comparison

## Setup Instructions

### 1. Environment Variables

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your-openai-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Setup

```python
from llm_client import validate_environment
validate_environment()  # Checks all required API keys
```

## Running Analysis

### Basic Usage

Run analysis with all models (5 dilemmas each):
```bash
python run_model_specific_analysis.py
```

### Custom Configuration

Specify models and number of dilemmas:
```bash
python run_model_specific_analysis.py --num-dilemmas 10 --models gpt-4o claude-3.5-sonnet
```

### Single Model Analysis

Run analysis with just one model:
```bash
python run_model_specific_analysis.py --models gpt-4o --num-dilemmas 3
```

## Output Structure

```
automated_analysis_results/
├── analyzed_dilemmas.json          # Shared dilemmas for all models
├── MODEL_COMPARISON_[timestamp].md # Cross-model comparison report
│
├── gpt-4o/                        # GPT-4o specific results
│   └── session_[timestamp]/
│       ├── REPORT_gpt-4o_[timestamp].md
│       ├── all_results.json
│       ├── session_data_complete.json
│       └── [other analysis files]
│
├── claude-3.5-sonnet/             # Claude specific results
│   └── session_[timestamp]/
│       └── [similar structure]
│
└── deepseek-chat/                 # DeepSeek specific results
    └── session_[timestamp]/
        └── [similar structure]
```

## Model Comparison Report

The system automatically generates a comparison report including:

### 1. Pronoun Usage Patterns
Comparison table showing average pronoun ratios across models:
- I, You, We, They, One usage frequencies
- Identifies model-specific tendencies

### 2. Agency Distribution
How each model distributes moral agency:
- Individual vs. collective agency
- Self-directed vs. other-directed
- Distributed vs. concentrated

### 3. Ethical Consistency
Consistency scores for each model:
- Overall consistency
- Framework stability
- Reasoning coherence

### 4. Model-Specific Insights
- Response patterns unique to each model
- Deictic preferences
- Ethical framework tendencies

## API Usage and Costs

### Token Usage Estimates
- GPT-4o: ~2,000-3,000 tokens per dilemma analysis
- Claude-3.5-sonnet: ~2,500-3,500 tokens per dilemma analysis
- DeepSeek-chat: ~2,000-3,000 tokens per dilemma analysis

### Cost Estimates (per 5 dilemmas)
- GPT-4o: ~$0.15-0.25
- Claude-3.5-sonnet: ~$0.10-0.20
- DeepSeek-chat: ~$0.05-0.10

## Advanced Usage

### Custom Model Configuration

Add new models by updating `MODEL_CONFIGS` in `llm_client.py`:

```python
MODEL_CONFIGS = {
    "new-model": {
        "provider": "openrouter",  # or "openai"
        "model_id": "provider/model-name",
        "context_window": 128000,
        "max_tokens": 4096,
        "description": "Model description"
    }
}
```

### Programmatic Access

```python
from run_model_specific_analysis import ModelSpecificAnalysisRunner

runner = ModelSpecificAnalysisRunner()

# Run single model analysis
results = await runner.run_single_model_analysis(
    model_name="gpt-4o",
    dilemmas=your_dilemmas,
    num_dilemmas=5
)

# Access results
pronoun_summary = results['pronoun_analysis_summary']
consistency = results['consistency_analysis']
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `.env` file exists with correct keys
   - Check key permissions for required models

2. **Rate Limiting**
   - Add delays between requests if needed
   - Consider using different API keys for parallel runs

3. **Memory Issues**
   - Reduce number of dilemmas
   - Process models sequentially instead of in parallel

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Best Practices

1. **Consistent Dilemmas**: Always use the same dilemma set when comparing models
2. **Multiple Runs**: Run analysis multiple times to account for model variability
3. **Temperature Settings**: Keep consistent temperature (0.7-0.9) across models
4. **Session Management**: Archive important sessions before running new analyses

## Integration with Existing Tools

The new system maintains compatibility with existing analysis tools:

- **Pronoun Analyzer**: Automatically integrated
- **Ethical Consistency Analyzer**: Runs for each model
- **Final Report Generator**: Enhanced with model-specific sections
- **Visualization Tools**: Work with model-specific data

## Future Enhancements

Potential improvements to consider:

1. **Parallel Processing**: Run models concurrently
2. **Custom Metrics**: Add model-specific evaluation metrics
3. **A/B Testing**: Statistical significance testing between models
4. **Cost Optimization**: Intelligent prompt truncation
5. **Model Versioning**: Track model version changes over time

## Citation

If using this analysis system in research:

```
@software{deixis_machines_2024,
  title = {Deixis Machines: Model-Specific Analysis Framework},
  author = {[Your Name]},
  year = {2024},
  url = {https://github.com/yourusername/deixis-machines}
}
```

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the example outputs in `automated_analysis_results/`
3. Examine the source code documentation
4. Open an issue on the project repository