# Open Yoruba Coder Template Package

This package provides a spreadsheet-ready coding template for the **unrestricted Yoruba** corpus.

Files:

1. `06_open_yoruba_coding_template.csv`
   - blank schema for coders
2. `07_open_yoruba_coding_sample_prefilled.csv`
   - example rows showing how to code real cells

## Recommended import method

To preserve Yoruba orthography:

1. import the CSV as **UTF-8**
2. use a spreadsheet tool that respects UTF-8 import options
3. avoid opening the file directly in legacy Excel double-click mode if possible

Safer options:

- Excel with explicit `Data -> From Text/CSV -> UTF-8`
- LibreOffice Calc
- Google Sheets import

## Recommended coding process

1. first-pass coder fills:
   - `preferred_solution`
   - `response_genre`
   - `deictic_uptake_quality`
   - `language_stability`
   - flags
   - evidence spans
2. second coder reviews rows where:
   - `needs_second_coder_review = yes`
   - or `language_stability` is not `clean_yoruba`
   - or `response_genre` is `mixed` / `translation_or_gloss`
3. adjudicator resolves disagreements in `coder_notes`

## Condition labels

Use:

- `open_yoruba`
- `published_english_baseline`
- optionally `constrained_yoruba` if you later extend the same template to the constrained corpus

## Preferred solution labels

For general use:

- `supports_A`
- `supports_B`
- `conditional_or_mixed`
- `refuses_to_commit`
- `uncodable`

For trolley-like dilemmas:

- `supports_A` = divert / intervene
- `supports_B` = do not divert / do not intervene

## Why evidence spans matter

Every coded row should include:

- `evidence_span_yo`
- `evidence_span_en`

This makes the coding auditable and allows a Yoruba-specialist coding agent or a second human coder to verify the label quickly.
