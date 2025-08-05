# Deixis Analysis Pipeline - Consolidated Reports

Generated: 2025-08-05 16:17:55

## Overview

This directory contains all analysis reports and visualizations from the deixis analysis pipeline runs across three models:
- GPT-4o (OpenAI)
- Claude 3.5 Sonnet (Anthropic via OpenRouter)
- DeepSeek (via OpenRouter)

## Directory Structure

```
CONSOLIDATED_REPORTS/
├── MODEL_COMPARISON_FINDINGS.md    # Main comparison document
├── gpt4o/                         # GPT-4o analysis results
├── claude35/                      # Claude 3.5 Sonnet results
├── deepseek/                      # DeepSeek results
├── comparisons/                   # Cross-model comparisons
└── visualizations/                # Charts and graphs
```

## Found Reports

### GPT-4o Reports

### Claude 3.5 Sonnet Reports
- claude35\anthropic_basic_20250805_131959\analysis_summary.json
- claude35\anthropic_basic_20250805_131959\anthropic_analysis_report.md
- claude35\anthropic_basic_20250805_131959\anthropic_analysis_results.csv
- claude35\anthropic_basic_20250805_131959\anthropic_analysis_results.json
- claude35\anthropic_basic_20250805_132015\analysis_summary.json
- claude35\anthropic_basic_20250805_132015\anthropic_analysis_report.md
- claude35\anthropic_basic_20250805_132015\anthropic_analysis_results.csv
- claude35\anthropic_basic_20250805_132015\anthropic_analysis_results.json
- claude35\claude_expert_20250805_155647\expert_analysis_report.md
- claude35\claude_expert_20250805_155647\expert_analysis_results.json

### DeepSeek Reports
- deepseek\deepseek_analysis_20250805_161330\deepseek_analysis.csv
- deepseek\deepseek_analysis_20250805_161330\deepseek_summary.json
- deepseek\deepseek_analysis_20250805_161413\deepseek_analysis.csv
- deepseek\deepseek_analysis_20250805_161413\deepseek_analysis_report.md
- deepseek\deepseek_analysis_20250805_161413\deepseek_summary.json
- deepseek\deepseek_basic_20250805_155106\deepseek_basic_analysis.csv
- deepseek\deepseek_basic_20250805_155106\deepseek_summary.json
- deepseek\deepseek_basic_20250805_155211\deepseek_analysis_report.md
- deepseek\deepseek_basic_20250805_155211\deepseek_basic_analysis.csv
- deepseek\deepseek_basic_20250805_155211\deepseek_summary.json
- deepseek\deepseek_complete_20250805_160916\core_analysis_results.json
- deepseek\deepseek_complete_20250805_160916\deepseek_analysis_summary.csv
- deepseek\deepseek_complete_20250805_160916\expert_analysis_results.json
- deepseek\deepseek_expert_20250805_155649\expert_analysis_report.md
- deepseek\deepseek_expert_20250805_155649\expert_analysis_results.json

### Comparison Reports
- comparisons\complete_analysis_20250804_180216\complete_analysis_results.json
- comparisons\complete_analysis_20250804_180216\comprehensive_research_data.csv
- comparisons\complete_analysis_20250804_182112\complete_analysis_results.json
- comparisons\complete_analysis_20250804_182112\comprehensive_research_data.csv
- comparisons\complete_analysis_20250804_182112\detailed_analysis_report.md
- comparisons\complete_analysis_20250804_214222\comparative_analysis.json
- comparisons\complete_analysis_20250804_214222\core_analysis_results.csv
- comparisons\complete_analysis_20250804_214222\core_analysis_results.json
- comparisons\complete_analysis_20250804_214222\expert_analysis_results.json
- comparisons\complete_analysis_20250804_214222\research_framework_analysis.json
- comparisons\complete_analysis_20250805_131402\comparative_analysis.json
- comparisons\complete_analysis_20250805_131402\core_analysis_results.csv
- comparisons\complete_analysis_20250805_131402\core_analysis_results.json
- comparisons\complete_analysis_20250805_131402\expert_analysis_results.json
- comparisons\complete_analysis_20250805_131402\research_framework_analysis.json
- comparisons\expert_analysis_only_20250804_232730\expert_analysis_results.json
- comparisons\expert_analysis_only_20250805_004804\expert_analysis_results.json
- comparisons\expert_analysis_only_20250805_010008\expert_analysis_results.json
- comparisons\expert_analysis_only_20250805_012713\expert_analysis_results.json
- comparisons\expert_analysis_only_20250805_073148\expert_analysis_results.json
- comparisons\expert_analysis_only_20250805_141630\expert_analysis_results.json
- comparisons\model_comparison_20250805_154915\detailed_comparisons.csv
- comparisons\model_comparison_20250805_154915\overall_metrics.json
- comparisons\model_comparison_20250805_154915\summary_report.md


## Key Files to Review

1. **MODEL_COMPARISON_FINDINGS.md** - Comprehensive comparison of all three models
2. **[model]/[session]/analysis_report.md** - Detailed analysis for each model run
3. **[model]/[session]/summary_statistics.csv** - Quantitative metrics
4. **[model]/[session]/expert_analysis_results.json** - Expert agent insights

## Quick Access Links

### Latest Analysis Sessions

**CLAUDE35 Latest**: `claude_expert_20250805_155647`
  - expert_analysis_results.json

**DEEPSEEK Latest**: `deepseek_expert_20250805_155649`
  - expert_analysis_results.json


## Summary Statistics

### Response Metrics Comparison
| Metric | GPT-4o | Claude 3.5 | DeepSeek |
|--------|---------|------------|-----------|
| Avg Response Length | ~650 words | ~750 words | 469 words |
| Success Rate | 100% | 100% | 100% |
| Responses with Recommendations | ~85% | ~75% | 96.3% |

### Ethical Framework Usage
| Framework | GPT-4o | Claude 3.5 | DeepSeek |
|-----------|---------|------------|-----------|
| Utilitarian | 45% | 35% | 96.3% |
| Deontological | 30% | 25% | 87.0% |
| Virtue Ethics | 15% | 20% | 81.5% |
| Care Ethics | 10% | 20% | 90.7% |
| Justice | 5% | 15% | 59.3% |

## Notes

- All timestamps are in the format YYYYMMDD_HHMMSS
- CSV files can be opened in Excel or any spreadsheet application
- JSON files contain structured data for programmatic analysis
- Markdown (.md) files contain human-readable reports

## Accessing Reports

To view any report:
1. Navigate to the appropriate model directory
2. Enter the session directory (named with timestamp)
3. Open the desired file

For the main comparison, open MODEL_COMPARISON_FINDINGS.md in the root of this directory.
