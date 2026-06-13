# Yoruba Content Coding Agent

Script:

- `yoruba_content_coding_agent.py`

Purpose:

- code the ethical content of Yoruba responses
- infer the preferred ethical action in each response
- classify the ethical preference type
- classify response genre, deictic uptake, and language stability
- return evidence spans for auditability

Outputs:

- `coded_content.json`
- `coded_content.csv`
- `coding_summary.json`

Recommended use:

```bash
python deixis_analysis_pipeline/yoruba_deixis_module/yoruba_content_coding_agent.py \
  "path\to\bilingual_session" \
  --coding-model gpt-4o
```

Important research recommendation:

- use this agent for **first-pass coding**
- review all rows with `needs_second_coder_review = true`
- do not treat the agent as the final adjudicator on ambiguous cells

Good starting datasets:

- open Yoruba full GPT-4o:
  `outputs/bilingual_sessions/yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926`
- open Yoruba full Claude:
  `outputs/bilingual_sessions/yoruba_control_claude_20260608_122738_bilingual_20260608_134631`
- open Yoruba full DeepSeek:
  `outputs/bilingual_sessions/yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525`
