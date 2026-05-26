# AIGC Repair Report

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
- `naming`: `aigc-repair-YYYYMMDD.md`
- `mode`: `impact_assessment | repair_plan | execute_repair | polish_and_inspire | asset_repair_route | audit_only`

## Repair Packet

- `target_locality`:
- `change_intent`:
- `scope_packages_loaded`:
- `source_rules_reviewed`:
- `canonical_owner`:
- `writeback_order`:
- `stage_routes`:

## Impact Map

- `upstream_truth`:
- `same_layer_neighbors`:
- `current_locality`:
- `downstream_existing`:
- `generated_assets`:
- `future_constraints`:
- `review_state`:

## Doubao Execution

- `doubao_task_packet`:
- `provider_evidence`:
- `provider_status`: `executed | degraded | not_required`
- `polish_scope`:
- `creative_candidates`:

## Asset Actions

- `preserve`:
- `invalidate`:
- `regenerate`:
- `review_only`:

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

- Source rules reviewed:
- Impact map completed:
- Source owner locked:
- Doubao evidence or degradation recorded:
- Asset action explicit:
- Review gate passed:
- Residual risks reported:
