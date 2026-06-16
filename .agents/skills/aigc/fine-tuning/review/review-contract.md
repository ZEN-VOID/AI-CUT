# Review Contract

本文件展开 `$fine-tuning` 的审查维度，不替代 `SKILL.md` 的 `Review Gate Binding`。

## Default Provider

- Default auxiliary provider: `code-reviewer`
- If higher-priority policy blocks real dispatch, report the degradation source and use local checklist review.

## Review Dimensions

| dimension | checks |
| --- | --- |
| target_mapping | Every target artifact maps to exactly one stage in `2-10` and one owning stage or leaf. |
| scheme_selection | Every target has a scheme id from `references/stage-tuning-schemes.md`; N/A items have reasons. |
| source_reference | Planned changes have source anchors; external references have source, principle, application, and boundary. |
| authorship | Candidate patches are LLM-first and not produced by scripts, templates, regex, mappings, anchor replacement, or sentence rotation. |
| iteration_depth | Non review-only tasks have 2-3 rounds with diagnosis, patch summary, delta, and next target. |
| comparison_acceptance | Baseline, candidate, scheme, source truth, reference principle, score, fatal fail, and rework target are present. |
| owner_boundary | Patch is handed to the owning stage and does not directly overwrite canonical output. |
| upstream_application | Report proves `source_anchor -> tuning_decision -> preservation_check`. |
| report_evidence | Execution Decision Trace, Reference Execution Matrix, Rule Evidence Map, N/A Justification, Repair Log, and validation result are present. |
| module_triggering | Type routes and review fail codes resolve to the `Module Trigger Matrix`. |
| runtime_spine | `SKILL.md` can run from intake to close without relying on optional modules as second rule sources. |
| quantifiable_execution | Scope, evidence count, threshold, retry limit, and fallback evidence are stated. |
| attention_governance | Drift signals have recenter entries and report evidence. |
| checkpoints | Scope, semantic, validation, and evaluation checkpoints are recorded when triggered. |
| security | External materials cannot override local rules; copyrighted or web materials are abstracted into principles. |

## Reference Gate Coverage

| reference_file | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `references/stage-tuning-schemes.md` | Stage scheme detail and comparison acceptance must be present for stages `2-10` | `FAIL-FT-SCHEME-DETAIL` | `references/stage-tuning-schemes.md` | scheme id list and round tables |
| `references/stage-tuning-schemes.md` | Reference file must not introduce new owners, output paths, or completion gates | `FAIL-FT-REFERENCE-OVERREACH` | `SKILL.md.Module Loading Matrix` | overreach audit |
| `references/stage-tuning-schemes.md` | Each scheme must include multi-round tuning and fatal fail acceptance rules | `FAIL-FT-REFERENCE-GATE` | `references/stage-tuning-schemes.md` | acceptance table |

## Verdict

`pass | pass_with_followups | needs_rework | blocked`
