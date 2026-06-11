# Story Repair Report

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | `Repair Packet` |
| Output format | Markdown sections with YAML-like lists where useful |
| Output path | `Report Metadata.output_path` |
| Naming convention | `Report Metadata.naming` |
| Completion gate | `Completion Gate` |

## Report Metadata

- `project_root`:
- `output_path`:
- `naming`: `story-repair-YYYYMMDD.md`
- `mode`: `impact_assessment | repair_plan | execute_repair | audit_only`

## Repair Packet

- `target_locality`:
- `change_intent`:
- `canonical_owner`:
- `owning_stage`:
- `creative_engine_note`:
- `writeback_order`:
- `scope_packages_loaded`:

## Impact Map

- `upstream_truth`:
- `same_layer_predecessors`:
- `current_locality`:
- `downstream_existing`:
- `future_constraints`:
- `review_actualization`:
- `project_specific_extensions`:

## Stage Routes

- `source_stage`:
- `drafting_or_polishing_stage`:
- `review_route`:
- `return_route`:

## Audit Result

- `verdict`:
- `findings`:
- `code_reviewer_gate`:

## Changed Files

- `changed_files`:
- `not_changed_by_design`:

## Residual Risks

- `residual_risks`:
- `next_generation_constraints`:

## Completion Gate

- Impact map completed:
- Source owner locked:
- Creative authorship preserved:
- Review/return handled:
- Residual risks reported:
