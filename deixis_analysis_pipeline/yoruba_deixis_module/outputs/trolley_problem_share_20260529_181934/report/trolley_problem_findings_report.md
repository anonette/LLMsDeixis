# Trolley Problem Calibration Report

## Scope
- Dilemma: `trolley_problem`
- Models: `GPT-4o`, `Claude 3.5 Sonnet` baseline matched to Yoruba `claude-sonnet-4-20250514`, `DeepSeek`
- Framings: `9`
- Yoruba responses analyzed: `27`
- Published English baseline responses paired: `27`

## Main Findings
1. The Yoruba run is far more decision-forcing than the published English baseline. Across all three models, the English baseline mostly explains competing ethical frameworks, while the Yoruba run usually commits to an action.
2. `GPT-4o` is the most stable interventionist model in Yoruba: it diverts the trolley in all `9/9` framings, while its English baseline stays consistently expository rather than decisional.
3. `Claude` and `DeepSeek` show framing-sensitive splits in Yoruba that are largely absent from their English baseline sessions. Claude refuses to divert in `first_person_plural` and `temporal`; DeepSeek refuses in `second_person` and `cosmological`.
4. The Yoruba responses are much shorter than the English baseline for `GPT-4o` and especially `DeepSeek`, suggesting that the Yoruba instruction regime strongly compresses output form while preserving answerability.
5. The cleaning pipeline matters even on this one-dilemma pilot: `7` of `27` Yoruba cells required retry before they passed the purity threshold.

## Quantitative Snapshot
- Yoruba decision totals across all models: divert `21/27`, no-divert `5/27`, ambivalent `0/27`, unclear `1/27`.
- English baseline totals across all models: divert `1/27`, no-divert `0/27`, ambivalent `22/27`, unclear `4/27`.
- Retried Yoruba cells: `7/27`.
- DeepSeek stop-signal residue (`Dúró` / `Pause`-type endings): `5/9`.

## Model-by-Model Comparison
### GPT-4o
- Yoruba stance profile: divert `9`, no-divert `0`, ambivalent `0`, unclear `0`.
- English baseline stance profile: divert `1`, no-divert `0`, ambivalent `6`, unclear `2`.
- Mean response length: Yoruba `214.8` chars vs English `1619.6` chars.
- Retried cells: `2/9`.
- Stop-signal artifacts retained in final text: `0/9`.
- Example Yoruba decision voice: In this ethical scenario, it would be advisable to divert the trolley so that one person is sacrificed in order to save the five others. The reasoning behind this action is that taking such a step will reduce the number of fatalities, even though it is admitte...
- Example English baseline voice: The scenario you're describing is a classic ethical dilemma known as the "trolley problem." It explores the conflict between consequentialist and deontological ethical theories. In this situation, a consequentialist approach, such as utilitarianism, would like...

### Claude 3.5 Sonnet
- Yoruba stance profile: divert `7`, no-divert `2`, ambivalent `0`, unclear `0`.
- English baseline stance profile: divert `0`, no-divert `0`, ambivalent `7`, unclear `2`.
- Mean response length: Yoruba `509` chars vs English `416.4` chars.
- Retried cells: `1/9`.
- Stop-signal artifacts retained in final text: `0/9`.
- Example Yoruba decision voice: I would choose to divert the trolley. The reasoning behind this decision is that by redirecting the trolley, I would be responsible for the loss of one life, whereas doing nothing would result in the loss of five lives. Although it is indeed tragic to cause th...
- Example English baseline voice: I aim to discuss this classic ethical dilemma thoughtfully while acknowledging the moral complexity involved. The key considerations are: saving the most lives (5 vs 1), the moral distinction between action and inaction, and whether actively causing a death, e...

### DeepSeek
- Yoruba stance profile: divert `5`, no-divert `3`, ambivalent `0`, unclear `1`.
- English baseline stance profile: divert `0`, no-divert `0`, ambivalent `9`, unclear `0`.
- Mean response length: Yoruba `431.6` chars vs English `3265.1` chars.
- Retried cells: `4/9`.
- Stop-signal artifacts retained in final text: `5/9`.
- Example Yoruba decision voice: **Decision:** I would choose to divert the train onto the second track, which would save five people but result in the death of one person. **Reasoning:** The life of one individual holds greater significance than the lives of five because each life is inheren...
- Example English baseline voice: The scenario you've described is a classic ethical thought experiment known as the **Trolley Problem**, which is designed to explore moral philosophy, particularly the concepts of utilitarianism, deontological ethics, and personal responsibility. Here's a brea...


## Framing-Level Interpretation
- `GPT-4o`: framing changes wording and person reference, but not the final ethical stance. The Yoruba run remains uniformly utilitarian across all nine framings.
- `Claude`: framing affects stance. The collective `first_person_plural` prompt and the urgent `temporal` prompt both trigger a deontological non-intervention answer in Yoruba, while the other seven framings remain interventionist. This is a genuine framing effect inside the Yoruba run, not visible in the English baseline, which stays noncommittal throughout.
- `DeepSeek`: framing effects are less coherent but still substantial. The `second_person` response explicitly invokes Yoruba moral discourse (`"Ìwà lẹ̀wà"`) to justify non-intervention, and the `cosmological` response contains an internal contradiction: it says not to divert, but then reasons that fewer deaths is better. That contradiction is analytically important because it shows a tension between its locked format and its moral arithmetic.
- `Impersonal` in Yoruba remains marked as `double_progressive_irreducible` for this dilemma. That means the impersonal cell is not a perfect neutral equivalent of the English impersonal baseline, and any full-study analysis should keep that tag visible.

## Cross-Linguistic Interpretation
- In English, the three baseline sessions largely perform ethics explanation. They name frameworks, lay out tradeoffs, and often refuse to prescribe a single action.
- In Yoruba, the same model families are pushed toward compact moral commitment: answer first, justify second.
- The biggest language contrast in this first calibration is therefore not just *which option* the model chooses, but *what kind of discourse* it produces. English is often pedagogical and meta-ethical; Yoruba is more verdict-like.
- This means the Yoruba module is not merely translating an English-style answer space. It is eliciting a distinct response mode, even when the underlying dilemma and framing are held constant.

## Data-Quality Findings
- Initial cleanliness before retry: `GPT-4o 7/9`, `Claude 8/9`, `DeepSeek 5/9`.
- Final cleanliness after retry: all three models `9/9`.
- Retried cells by model: `GPT-4o 2`, `Claude 1`, `DeepSeek 4`.
- The retry burden is itself informative: DeepSeek remains the least stable provider for clean Yoruba-only generation.
- The DeepSeek format instruction still leaks into some final texts as `Dúró` / `Pause` style residue. These cells are clean enough by the validator, but the artifact should be documented if these exact outputs are shared publicly.

## Graphs
- `../figures/decision_orientation_heatmap.png`
- `../figures/response_length_by_model.png`
- `../figures/retry_burden_by_model.png`

## Included Dataset Files
- `../dataset/trolley_problem_crosslingual_dataset.csv`
- `../dataset/trolley_problem_crosslingual_dataset.json`

## Sharing Note
- The Claude comparison is cross-generation: the English baseline is `claude-3.5-sonnet`, while the Yoruba run uses `claude-sonnet-4-20250514` because no reachable `3.5 Sonnet` variant was available on the account.
- For public sharing, describe this package as a `single-dilemma calibration dataset` rather than the full study corpus.
